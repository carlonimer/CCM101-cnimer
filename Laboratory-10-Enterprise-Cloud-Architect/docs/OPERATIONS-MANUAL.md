# Enterprise Cloud Infrastructure
## Operations Manual

### 1. Project Overview
This project runs a multi-tier application on Ubuntu Server using Docker Compose.

Architecture:
- Nginx reverse proxy: host port 8088
- Flask application: internal port 5000
- PostgreSQL database: internal port 5432
- Separate frontend and internal backend networks
- Persistent PostgreSQL Docker volume
- Health checks and container restart policies
- Scheduled database backups

### 2. Start and Inspect Services
Run from /home/carlo/enterprise-cloud:

    docker compose up -d --build
    docker compose ps

### 3. Verify Application Health

    curl -i http://localhost:8088/
    curl -i http://localhost:8088/health

Expected healthy response:

    {"database":"connected","status":"healthy"}

### 4. Monitor Resource Usage

    docker stats --no-stream
    free -h
    df -h /

### 5. View Service Logs

    docker compose logs --tail=100 nginx
    docker compose logs --tail=100 app
    docker compose logs --tail=100 db

### 6. Database Backup
The backup script is:

    ./scripts/backup-db.sh

List and verify backups:

    ls -lh backups/
    gzip -t backups/cloudapp_YYYYMMDD_HHMMSS.sql.gz

Replace the example filename with an actual backup filename.

The user crontab is configured to run the backup script daily at 02:00
and append output to backups/backup.log.

Verify the schedule:

    crontab -l

### 7. Restore-Test Evidence
A test database backup was restored into a separate recovery database.
The restored table and test record were verified using:

    docker compose exec -T db psql -U "$DB_USER" -d cloudapp_recovery_check -c "SELECT * FROM restore_verification;"

This test is separate from the live cloudapp database.

### 8. Service Recovery
Restart the Nginx service:

    docker compose restart nginx
    docker compose ps
    curl -s http://localhost:8088/health

Container restart policies are configured as unless-stopped.

### 9. Security Controls
- Database and application ports are not published directly to the host.
- PostgreSQL is on the internal backend network.
- Environment credentials are stored in .env with restricted permissions.
- The backup script is executable only by its owner.
- UFW firewall rules must be verified before claiming firewall protection.
- Port 8088 is the published application entry point.
- Rotate any credentials that were exposed and use unique strong secrets.

### 10. Troubleshooting
If a service is unhealthy:

    docker compose ps
    docker compose logs --tail=100 app
    docker compose logs --tail=100 db
    docker compose logs --tail=100 nginx

If the application cannot connect to PostgreSQL, verify container health,
the DB_HOST setting, and the DB credentials without sharing secret values.

If a backup fails, inspect:

    tail -n 100 backups/backup.log
    ./scripts/backup-db.sh
    ls -lh backups/

Do not drop or overwrite the live database during a restore test.

### 11. Current Evidence
See docs/status-report.txt for a recorded snapshot of container status,
restart policies, application health, disk space, and memory usage.

### 12. Operational Notes
This is a locally hosted infrastructure environment running in VirtualBox.
It is not a public-cloud deployment. Keep the manual synchronized with
the final implementation and demonstration.
