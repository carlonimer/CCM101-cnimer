#!/usr/bin/env bash
set -Eeuo pipefail

cd /home/carlo/enterprise-cloud
umask 077

BACKUP_DIR="/home/carlo/enterprise-cloud/backups"
mkdir -p "$BACKUP_DIR"

set -a
source .env
set +a

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_FILE="$BACKUP_DIR/cloudapp_${TIMESTAMP}.sql.gz"
TEMP_FILE="${BACKUP_FILE}.tmp"

cleanup() {
    rm -f "$TEMP_FILE"
}
trap cleanup EXIT

if docker compose exec -T db \
    pg_dump -U "$DB_USER" -d "$DB_NAME" --no-owner --no-acl \
    | gzip -c > "$TEMP_FILE"; then
    gzip -t "$TEMP_FILE"
    mv "$TEMP_FILE" "$BACKUP_FILE"
    echo "Backup successful: $BACKUP_FILE"
else
    echo "ERROR: Database backup failed." >&2
    exit 1
fi

find "$BACKUP_DIR" -maxdepth 1 -type f \
    -name 'cloudapp_*.sql.gz' -mtime +7 -delete
