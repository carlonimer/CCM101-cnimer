#!/usr/bin/env bash
set -Eeuo pipefail

# Dynamic project directory resolution (supports both local Ubuntu VM and KillerCoda defense)
PROJECT_DIR="${PROJECT_DIR:-/home/carlo/enterprise-cloud}"
if [ ! -d "$PROJECT_DIR" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/docker-compose.yml" ]; then
        PROJECT_DIR="$SCRIPT_DIR"
    elif [ -f "$SCRIPT_DIR/../docker-compose.yml" ]; then
        PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
    else
        PROJECT_DIR="$(pwd)"
    fi
fi

cd "$PROJECT_DIR"
umask 077

BACKUP_DIR="$PROJECT_DIR/backups"
mkdir -p "$BACKUP_DIR"

if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi

DB_USER="${DB_USER:-clouduser}"
DB_NAME="${DB_NAME:-cloudapp}"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_FILE="$BACKUP_DIR/cloudapp_${TIMESTAMP}.sql.gz"
TEMP_FILE="${BACKUP_FILE}.tmp"

cleanup() {
    rm -f "$TEMP_FILE"
}
trap cleanup EXIT

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting automated database backup..."

if docker compose exec -T db \
    pg_dump -U "$DB_USER" -d "$DB_NAME" --no-owner --no-acl \
    | gzip -c > "$TEMP_FILE"; then
    gzip -t "$TEMP_FILE"
    mv "$TEMP_FILE" "$BACKUP_FILE"
    echo "Backup successful: $BACKUP_FILE"
    echo "Backup size: $(du -h "$BACKUP_FILE" | cut -f1)"
else
    echo "ERROR: Database backup failed." >&2
    exit 1
fi

find "$BACKUP_DIR" -maxdepth 1 -type f \
    -name 'cloudapp_*.sql.gz' -mtime +7 -delete
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup cycle completed successfully."
