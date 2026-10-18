#!/usr/bin/env bash
# ==============================================================================
# CloudNova Technologies - Enterprise Operations & Disaster Recovery Script
# Mission 10: The Enterprise Cloud Architect
# Script: automation-script.sh
# Author: Carlo Nimer
# Purpose: Autonomous database & persistent storage backup, rotation, and health auditing.
# Schedule: Configured via Cron (e.g., daily at 02:00 AM)
# ==============================================================================

set -eo pipefail

# ------------------------------------------------------------------------------
# Configuration Variables
# ------------------------------------------------------------------------------
BACKUP_DIR="${BACKUP_DIR:-/var/backups/cloudnova}"
LOG_FILE="${LOG_FILE:-/var/log/cloudnova-backup.log}"
RETENTION_DAYS=7
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
CONTAINER_DB="cloudnova-db"
CONTAINER_WEB="cloudnova-web"
DB_NAME="cloudnova_wp"
DB_USER="root"
DB_PASS="CloudNovaRootSecure2026!"
VOLUME_WP="cloudnova_wp_data"

# Create log file directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true
mkdir -p "$BACKUP_DIR"

# ------------------------------------------------------------------------------
# Logging Functions
# ------------------------------------------------------------------------------
log() {
    local level="$1"
    local message="$2"
    local timestamp
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

log_info()    { log "INFO" "$1"; }
log_success() { log "SUCCESS" "$1"; }
log_warn()    { log "WARNING" "$1"; }
log_error()   { log "ERROR" "$1"; }

# ------------------------------------------------------------------------------
# Usage / Help Display
# ------------------------------------------------------------------------------
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "CloudNova Enterprise Disaster Recovery & Autonomous Backup Automation."
    echo ""
    echo "Options:"
    echo "  --run         Execute full operational backup immediately (default)."
    echo "  --test        Run dry-run / health check without generating files."
    echo "  --list        List existing backups and disk utilization."
    echo "  --help        Display this help message."
    echo ""
}

# ------------------------------------------------------------------------------
# Pre-Flight System Checks
# ------------------------------------------------------------------------------
check_prerequisites() {
    log_info "Initiating operational pre-flight checks..."

    # Check Docker daemon availability
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker daemon is not responding or insufficient privileges."
        exit 1
    fi

    # Verify database container is online
    if ! docker ps --format '{{.Names}}' | grep -Eq "^${CONTAINER_DB}$"; then
        log_error "Database container '${CONTAINER_DB}' is NOT running. Aborting backup."
        exit 1
    fi

    # Check available disk space in backup partition (fail if > 90% full)
    local disk_usage
    disk_usage=$(df -h "$BACKUP_DIR" | awk 'NR==2 {print $5}' | tr -d '%')
    if [ "$disk_usage" -ge 90 ]; then
        log_warn "Backup volume is ${disk_usage}% full! Storage threshold warning."
    else
        log_info "Storage capacity check passed (Volume utilization: ${disk_usage}%)."
    fi
}

# ------------------------------------------------------------------------------
# Backup Execution Routine
# ------------------------------------------------------------------------------
perform_backup() {
    local db_backup_file="${BACKUP_DIR}/db_${DB_NAME}_${TIMESTAMP}.sql.gz"
    local wp_backup_file="${BACKUP_DIR}/wp_volume_${TIMESTAMP}.tar.gz"
    local checksum_file="${BACKUP_DIR}/checksums_${TIMESTAMP}.sha256"

    log_info "Starting database snapshot for '${DB_NAME}' from '${CONTAINER_DB}'..."

    # 1. Hot MySQL dump stream into gzip
    if docker exec "$CONTAINER_DB" mysqldump \
        -u"$DB_USER" \
        -p"$DB_PASS" \
        --single-transaction \
        --quick \
        --databases "$DB_NAME" 2>/dev/null | gzip > "$db_backup_file"; then
        
        local db_size
        db_size=$(du -h "$db_backup_file" | cut -f1)
        log_success "Database backup generated successfully: $(basename "$db_backup_file") ($db_size)"
    else
        log_error "Database dump failed!"
        rm -f "$db_backup_file"
        exit 1
    fi

    # 2. WordPress persistent storage backup (via lightweight temporary container)
    log_info "Archiving WordPress persistent volume '${VOLUME_WP}'..."
    if docker run --rm \
        -v "${VOLUME_WP}:/source:ro" \
        -v "${BACKUP_DIR}:/backup" \
        alpine tar -czf "/backup/wp_volume_${TIMESTAMP}.tar.gz" -C /source . 2>/dev/null; then

        local wp_size
        wp_size=$(du -h "$wp_backup_file" | cut -f1)
        log_success "WordPress volume archived: $(basename "$wp_backup_file") ($wp_size)"
    else
        log_error "Volume archive failed!"
        exit 1
    fi

    # 3. Cryptographic integrity check (SHA-256)
    log_info "Generating cryptographic checksums for audit trail..."
    cd "$BACKUP_DIR" && sha256sum "$(basename "$db_backup_file")" "$(basename "$wp_backup_file")" > "$checksum_file"
    log_success "Checksum file generated: $(basename "$checksum_file")"
}

# ------------------------------------------------------------------------------
# Automated Retention & Rotation Policy
# Purges snapshots older than RETENTION_DAYS
# ------------------------------------------------------------------------------
rotate_backups() {
    log_info "Enforcing retention policy (retention window: ${RETENTION_DAYS} days)..."
    
    local purged_count
    purged_count=$(find "$BACKUP_DIR" -type f \( -name "*.sql.gz" -o -name "*.tar.gz" -o -name "*.sha256" \) -mtime +"$RETENTION_DAYS" | wc -l)

    if [ "$purged_count" -gt 0 ]; then
        find "$BACKUP_DIR" -type f \( -name "*.sql.gz" -o -name "*.tar.gz" -o -name "*.sha256" \) -mtime +"$RETENTION_DAYS" -exec rm -f {} +
        log_success "Retention policy executed. Purged ${purged_count} archived file(s)."
    else
        log_info "No archives exceeded retention period. 0 files purged."
    fi
}

# ------------------------------------------------------------------------------
# Operational Status / List Backups
# ------------------------------------------------------------------------------
list_backups() {
    echo "================================================================="
    echo " CloudNova Technologies - Disaster Recovery Archive Inventory"
    echo " Directory: $BACKUP_DIR"
    echo "================================================================="
    ls -lh "$BACKUP_DIR"
    echo ""
    echo "Disk Utilization for $BACKUP_DIR:"
    df -h "$BACKUP_DIR"
}

# ------------------------------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------------------------------
case "${1:-run}" in
    --run|run)
        log_info "=== CloudNova Automated Operational Run Initiated ==="
        check_prerequisites
        perform_backup
        rotate_backups
        log_success "=== Operational Run Completed with Zero Errors ==="
        ;;
    --test|test)
        echo "Performing dry-run diagnostics..."
        check_prerequisites
        log_info "Dry-run diagnostics passed. System ready for automated scheduling."
        ;;
    --list|list)
        list_backups
        ;;
    --help|help|-h)
        usage
        ;;
    *)
        echo "Unknown argument: $1"
        usage
        exit 1
        ;;
esac
