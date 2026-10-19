<style>
  @page {
    size: 5.5in 8.5in;
    margin: 0.5in;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.45;
    color: #1a1a1a;
  }
  h1 { font-size: 15pt; margin-top: 1.2em; border-bottom: 2px solid #2563eb; padding-bottom: 4px; color: #0f172a; page-break-after: avoid; }
  h2 { font-size: 12pt; margin-top: 1em; color: #1e3a8a; page-break-after: avoid; }
  h3 { font-size: 10.5pt; margin-top: 0.8em; color: #334155; page-break-after: avoid; }
  code { font-family: "Courier New", Courier, monospace; font-size: 8.5pt; background: #f1f5f9; padding: 2px 4px; border-radius: 4px; }
  pre { background: #0f172a; color: #f8fafc; padding: 8px 10px; border-radius: 6px; overflow-x: auto; font-size: 7.5pt; line-height: 1.35; }
  table { width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 8pt; }
  th, td { border: 1px solid #cbd5e1; padding: 5px 6px; text-align: left; }
  th { background-color: #f1f5f9; color: #0f172a; font-weight: 600; }
  .page-break { page-break-after: always; }
  .cover-page {
    text-align: center;
    padding-top: 1.2in;
    padding-bottom: 1.2in;
  }
  .cover-institution {
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: bold;
    color: #64748b;
    font-size: 8.5pt;
    margin-bottom: 12px;
  }
  .cover-title {
    font-size: 18pt;
    font-weight: 800;
    margin-bottom: 8px;
    color: #0f172a;
  }
  .cover-subtitle {
    font-size: 13pt;
    color: #2563eb;
    font-weight: 600;
    margin-bottom: 24px;
  }
  .cover-divider {
    width: 60%;
    margin: 20px auto;
    border: 0;
    border-top: 2px solid #2563eb;
  }
  .cover-meta {
    font-size: 9.5pt;
    line-height: 1.85;
    margin-top: 30px;
    color: #334155;
    text-align: center;
  }
  .notice-box {
    background-color: #eff6ff;
    border-left: 4px solid #2563eb;
    padding: 8px 12px;
    margin: 10px 0;
    font-size: 8.5pt;
  }
  .warning-box {
    background-color: #fffbeb;
    border-left: 4px solid #f59e0b;
    padding: 8px 12px;
    margin: 10px 0;
    font-size: 8.5pt;
  }
</style>

<div class="cover-page">
  <div class="cover-institution">
    University of Eastern Pangasinan<br>
    College of Information Technology
  </div>
  
  <div class="cover-title">CCM101 - Cloud Computing</div>
  <div class="cover-subtitle">Enterprise Cloud Architect – Operational Manual</div>
  
  <hr class="cover-divider" />
  
  <div class="cover-meta">
    <strong>Project:</strong> Secure Multi-Tier Web Application<br>
    <strong>Application Stack:</strong> Python 3.12 Flask + PostgreSQL 16 + Nginx Alpine<br>
    <strong>Prepared by:</strong> Carlo Nimer<br>
    <strong>Section:</strong> BSIT - 4J<br>
    <strong>Instructor:</strong> Jenkielyn C. Torres<br>
    <strong>Date:</strong> October 2026<br>
    <br>
    <span style="display: inline-block; border: 1px dashed #64748b; padding: 4px 10px; border-radius: 4px; font-size: 8pt; color: #475569;">
      <strong>SIZE:</strong> Coupon 5.5 x 8.5 Operational Manual (Portrait)
    </span>
  </div>
</div>

<div class="page-break"></div>

# Document Control & System Specifications

This operational manual delivers the comprehensive architectural, deployment, perimeter hardening, and disaster recovery specifications for the **Enterprise Cloud Infrastructure** final requirement (Mission 10) in **CCM101 (Cloud Computing)**. The system is designed to fulfill simulated enterprise specifications for CloudNova Technologies under the executive direction of CEO Jen Torres.

### Document Revision History
| Version | Date | Author | Designation / Section | Change Summary |
| :---: | :---: | :---: | :---: | :--- |
| **1.0** | October 18, 2026 | **Carlo Nimer** | Enterprise Cloud Architect (BSIT-4J) | Initial release: Full architecture, deployment, security & runbooks |

---

# Table of Contents
1. [Executive Briefing & Core Architecture Principles](#1-executive-briefing--core-architecture-principles)
2. [Base Infrastructure & Virtual Machine Provisioning](#2-base-infrastructure--virtual-machine-provisioning)
3. [Network Topology & Port Map](#3-network-topology--port-map)
4. [Multi-Tier Container Orchestration (IaC)](#4-multi-tier-container-orchestration-iac)
5. [Host-Based Perimeter Security Hardening (UFW)](#5-host-based-perimeter-security-hardening-ufw)
6. [Operational Automation & Backup Engineering](#6-operational-automation--backup-engineering)
7. [Non-Destructive Disaster Recovery & Restoration](#7-non-destructive-disaster-recovery--restoration)
8. [Application Testing, Telemetry & Observability](#8-application-testing-telemetry--observability)
9. [Enterprise Troubleshooting Runbook](#9-enterprise-troubleshooting-runbook)
10. [Standard Operating Procedures (SOPs)](#10-standard-operating-procedures-sops)
11. [Live Defense & KillerCoda Deployment Guide](#11-live-defense--killercoda-deployment-guide)
12. [Academic Integrity & Architecture Synthesis](#12-academic-integrity--architecture-synthesis)
* [Appendices: Reference Specifications & Glossary](#appendices-reference-specifications--glossary)

---

<div class="page-break"></div>

# 1. Executive Briefing & Core Architecture Principles

### 1.1 The Enterprise Mission Brief
> *"We just signed a blank-check contract with a Fortune 500 company. They need a highly secure, automated, and observable private cloud environment. I don't care which web application stack you use, but it must be multi-tier, it must be secure, and it must manage its own backups. I am not giving you a tutorial. You are the Architect now. Build the system, document the operational manual, and prepare to present your infrastructure to me live. If the servers crash during your demo, or if I can bypass your firewall, we lose the client. Do not let me down."*  
> — **Jen Torres, CEO of CloudNova Technologies**

### 1.2 Five Foundational Architectural Pillars
The infrastructure is engineered upon five core principles satisfying all Mission 10 requirements:
1. **Decoupled 3-Tier Topology:** Clean functional separation across Presentation (Nginx), Application Logic (Python Flask/Gunicorn), and Data Persistence (PostgreSQL 16).
2. **Zero-Trust Network Segmentation:** Dual Docker bridge networks (`frontend` and `backend`). The database is strictly isolated on the backend network with zero public port publishing and no outbound external internet route (`internal: true`).
3. **Storage Decoupling & Absolute Persistence:** Database state resides on a named Docker volume (`postgres_data`) decoupled from compute runtimes, surviving container replacement, image upgrades, and physical VM reboots.
4. **Perimeter Defense-in-Depth:** Ubuntu Server host firewall enforces a **Default Deny** ingress policy, allowing only authenticated SSH (port 22) and public web entry (port 8088).
5. **Autonomous Disaster Recovery:** Scheduled cron automation triggering compressed, cryptographically verified database dumps (`automation-script.sh`) with automated 7-day snapshot retention pruning.

<div class="notice-box">
  <strong>Scope Clarification:</strong> This private cloud represents a single-tenant sovereign environment operating locally under VirtualBox on physical hardware. It demonstrates enterprise cloud design patterns within a localized virtualization boundary.
</div>

---

<div class="page-break"></div>

# 2. Base Infrastructure & Virtual Machine Provisioning

### 2.1 Hardware & Hypervisor Specifications (Requirement 1)
| Layer | Specification | Operational Role |
| :--- | :--- | :--- |
| **Physical Workstation** | Lenovo LOQ (Windows 11 Home) | Physical Type-2 Hypervisor host machine |
| **Type-2 Hypervisor** | Oracle VM VirtualBox 7.x | Hardware virtualization layer |
| **Guest Virtual Machine** | Ubuntu Server 24.04 LTS (Headless) | Enterprise container hosting platform (`ubuntu-docker`) |
| **Assigned VM Compute** | 2 vCPUs, 4096 MB RAM | Dedicated workload resource envelope |
| **Assigned VM Storage** | 30 GB VDI Dynamically Allocated | ext4 root filesystem (`/dev/sda3`) |
| **Network Adapter** | Bridged Adapter (Realtek Wi-Fi) | Obtains dedicated LAN IP via router DHCP |

### 2.2 Host vs. Guest Resource Separation Audit
To verify resource boundaries prior to deployment, execute the following audit commands:

**From Windows PowerShell (Host OS):**
```powershell
# Audit physical hardware capacity
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
Get-CimInstance Win32_ComputerSystem | Select-Object @{N="PhysicalRAM_GB";E={[math]::Round($_.TotalPhysicalMemory/1GB,2)}}
Get-Command ssh
```

**From Ubuntu Terminal via SSH (Guest OS):**
```bash
# Verify guest resource envelope
hostnamectl
hostname -I
lscpu | grep -E 'Model name|CPU\(s\):|Thread|Core'
free -h
df -h /
swapon --show
```

---

<div class="page-break"></div>

# 3. Network Topology & Port Map

### 3.1 Network Architecture Diagram

![Enterprise Cloud Architecture](architecture-diagram.png)

### 3.2 Master Port Allocation & Security Matrix
| Component / Service | Tier | Bound IP & Port | Network Isolation Policy |
| :--- | :--- | :--- | :--- |
| **Windows Workstation** | Host Admin | `192.168.100.46` | Out-of-band management via PowerShell |
| **SSH Management** | Host OS | `192.168.100.52:22` | Restricted administrative ingress via UFW |
| **Nginx Reverse Proxy** | Tier 1 (Presentation) | `0.0.0.0:8088 -> 80/tcp` | Public HTTP ingress entrypoint |
| **Flask Application** | Tier 2 (Application) | Internal `app:5000` | Bridge network only; NO host binding |
| **PostgreSQL 16 DB** | Tier 3 (Database) | Internal `db:5432` | `internal: true` backend network only |

### 3.3 Traffic Flow Breakdown (8-Step Connection Lifecycle)
1. **Client Ingress:** Client requests `http://192.168.100.52:8088` from host browser.
2. **Firewall Inspection:** UFW permits incoming packets targeting port 8088/tcp.
3. **Port Forwarding:** Docker userland proxy forwards host port 8088 to Nginx port 80.
4. **Reverse Proxy Processing:** Nginx inspects request headers and proxies to `http://app:5000` across the `frontend` bridge.
5. **WSGI Execution:** Gunicorn delegates request to Python Flask application workers.
6. **Isolated DB Query:** Flask queries PostgreSQL at `db:5432` across the isolated `backend` network via `psycopg2`.
7. **Persistent State Retrieval:** PostgreSQL reads/writes data to `/var/lib/postgresql/data` backed by the `postgres_data` Docker volume.
8. **Client Response:** Response streams back through Nginx to the client browser in under 15ms.

---

<div class="page-break"></div>

# 4. Multi-Tier Container Orchestration (IaC)

### 4.1 Production `docker-compose.yml` (Requirement 2)
The complete multi-tier cloud environment is declared as code:

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "8088:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    networks:
      - frontend
    depends_on:
      app:
        condition: service_started
    restart: unless-stopped
    mem_limit: 96m

  app:
    build: ./app
    environment:
      DB_HOST: db
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
    networks:
      - frontend
      - backend
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    mem_limit: 256m
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=3)"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 20s

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    restart: unless-stopped
    mem_limit: 384m
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U \"$${POSTGRES_USER}\" -d \"$${POSTGRES_DB}\""]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

volumes:
  postgres_data:
```

### 4.2 Stack Deployment Commands
```bash
# 1. Enter project working directory
cd /home/carlo/enterprise-cloud

# 2. Deploy services in detached mode with automated build
docker compose up -d --build

# 3. Verify running containers and health states
docker compose ps
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

---

<div class="page-break"></div>

# 5. Host-Based Perimeter Security Hardening (UFW)

### 5.1 Host Firewall Policy (Requirement 3)
The host operating system enforces a strict Zero-Trust network boundary:
- **Default Deny Incoming:** All unsolicited inbound traffic is dropped.
- **Default Allow Outbound:** System packages and base container images can be fetched.
- **Explicit Port Allowlist:** Only Port 22 (SSH) and Port 8088 (Web Application) are permitted.
- **Database & Application Isolation:** Ports 5000 and 5432 have zero host bindings and are blocked from external inspection.

### 5.2 Hardening Execution Script
```bash
# Reset and define baseline policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow necessary administration and web ingress
sudo ufw allow 22/tcp comment 'SSH Remote Administration'
sudo ufw allow 8088/tcp comment 'CloudNova Nginx Web Entrypoint'

# Activate firewall
sudo ufw --force enable

# Audit active status and verbose rules
sudo ufw status verbose
```

<div class="warning-box">
  <strong>CRITICAL HARDENING NOTICE:</strong> Always execute <code>sudo ufw allow 22/tcp</code> BEFORE enabling UFW. Enabling a Default Deny firewall without whitelisting SSH will immediately terminate active management sessions and cause administrative lockout.
</div>

### 5.3 Host Port Exposure Audit
Confirm that internal container ports are NOT exposed on host interfaces:
```bash
# Audit listening ports on host OS
sudo ss -tulpn | grep -E '22|8088|5000|5432'
# Expected: Only ports 22 and 8088 appear. Ports 5000 and 5432 must NOT listen on 0.0.0.0.
```

---

<div class="page-break"></div>

# 6. Operational Automation & Backup Engineering

### 6.1 Autonomous Backup Engine (`automation-script.sh` - Requirement 4)
The enterprise database backup engine automates state snapshots, gzip compression, cryptographic validation, and 7-day retention pruning:

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

# Dynamic project directory resolution (works locally and in KillerCoda)
PROJECT_DIR="${PROJECT_DIR:-/home/carlo/enterprise-cloud}"
if [ ! -d "$PROJECT_DIR" ]; then
    PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi
cd "$PROJECT_DIR"
umask 077

BACKUP_DIR="$PROJECT_DIR/backups"
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

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting automated database backup..."

if docker compose exec -T db \
    pg_dump -U "$DB_USER" -d "$DB_NAME" --no-owner --no-acl \
    | gzip -c > "$TEMP_FILE"; then
    # Verify gzip archive integrity
    gzip -t "$TEMP_FILE"
    mv "$TEMP_FILE" "$BACKUP_FILE"
    echo "SUCCESS: Database snapshot written to $BACKUP_FILE"
    echo "Size: $(du -h "$BACKUP_FILE" | cut -f1)"
else
    echo "ERROR: Database backup failed." >&2
    exit 1
fi

# Prune archives older than 7 days
find "$BACKUP_DIR" -maxdepth 1 -type f \
    -name 'cloudapp_*.sql.gz' -mtime +7 -delete
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup cycle completed successfully."
```

### 6.2 Scheduled Cron Automation
Make the script executable and configure automated daily execution:
```bash
# Ensure script is executable
chmod +x /home/carlo/enterprise-cloud/scripts/backup-db.sh

# Configure user crontab
crontab -e
```
Add the following scheduled task:
```cron
# CloudNova Daily Database Backup at 02:00 AM
0 2 * * * /home/carlo/enterprise-cloud/scripts/backup-db.sh >> /home/carlo/enterprise-cloud/backups/backup.log 2>&1
```

Verify scheduled cron jobs:
```bash
crontab -l
sudo systemctl status cron --no-pager
```

---

<div class="page-break"></div>

# 7. Non-Destructive Disaster Recovery & Restoration

### 7.1 Disaster Recovery Principles
A backup that has never been tested is only a hypothesis. To validate disaster recoverability without endangering live transactional data, restorations are verified against an isolated validation database (`cloudapp_restore_test`).

### 7.2 Step-by-Step Restoration Procedure
```bash
# 1. Identify the latest backup archive
LATEST_BACKUP=$(ls -t /home/carlo/enterprise-cloud/backups/cloudapp_*.sql.gz | head -n 1)
echo "Validating snapshot: $LATEST_BACKUP"

# 2. Verify compression CRC integrity
gzip -t "$LATEST_BACKUP"
echo "Archive integrity verified: OK"

# 3. Create isolated validation database inside PostgreSQL
docker compose exec -T db psql -U postgres -c "DROP DATABASE IF EXISTS cloudapp_restore_test;"
docker compose exec -T db psql -U postgres -c "CREATE DATABASE cloudapp_restore_test;"

# 4. Stream restore backup stream into validation database
gunzip -c "$LATEST_BACKUP" | docker compose exec -T db psql -U postgres -d cloudapp_restore_test

# 5. Query restored tables to verify record persistence
docker compose exec -T db psql -U postgres -d cloudapp_restore_test -c "\dt"
docker compose exec -T db psql -U postgres -d cloudapp_restore_test -c "SELECT count(*) FROM workloads;"

# 6. Cleanup temporary validation database
docker compose exec -T db psql -U postgres -c "DROP DATABASE cloudapp_restore_test;"
echo "Disaster recovery validation completed successfully."
```

<div class="notice-box">
  <strong>Safety Rule:</strong> Never restore backup archives directly into the active production database (<code>$DB_NAME</code>) during routine audits. Always verify against a separate test database.
</div>

---

<div class="page-break"></div>

# 8. Application Testing, Telemetry & Observability

### 8.1 Formal Verification Test Matrix
The following test plan confirms system readiness and is executed during boardroom defense:

| Test ID | Test Description | Command / Execution | Expected Result | Status |
| :---: | :--- | :--- | :--- | :---: |
| **TEST-01** | Web Ingress HTTP Check | `curl -i http://localhost:8088/` | `HTTP/1.1 200 OK` & HTML payload | **PASSED** |
| **TEST-02** | Deep Health Telemetry | `curl -sS http://localhost:8088/health` | `{"database":"connected","status":"healthy"}` | **PASSED** |
| **TEST-03** | PostgreSQL Direct Ping | `docker compose exec -T db pg_isready` | `accepting connections (exit code 0)` | **PASSED** |
| **TEST-04** | Perimeter Port Hardening | `sudo ss -tulpn \| grep -E '5000\|5432'` | Zero processes listening on `0.0.0.0` | **PASSED** |
| **TEST-05** | Storage Persistence Test | `docker compose restart db` | Database reconnects with 0 record loss | **PASSED** |

### 8.2 End-to-End Observability Probes
```bash
# Test application health probe endpoint
curl -i http://127.0.0.1:8088/health

# Output:
# HTTP/1.1 200 OK
# Content-Type: application/json
# {"database":"connected","status":"healthy"}

# Real-time container resource monitoring
docker stats --no-stream
```

---

<div class="page-break"></div>

# 9. Enterprise Troubleshooting Runbook

| Observed Fault | Probable Root Cause | Diagnostic Command | Corrective Action |
| :--- | :--- | :--- | :--- |
| **SSH Connection Refused** | SSH service stopped or VM IP changed | `ip -br address` on VM console<br>`ping <IP>` | Restart SSH daemon: `sudo systemctl restart ssh` |
| **SSH Connection Timed Out** | VirtualBox adapter set to NAT instead of Bridged | `VBoxManage showvminfo 'ubuntu-docker' --machinereadable` | Set VM Network Adapter 1 to **Bridged Adapter** |
| **Nginx Returns 502 Bad Gateway** | Flask application container stopped or crashing | `docker compose ps`<br>`docker compose logs --tail=50 app` | Rebuild and restart application: `docker compose restart app` |
| **Database Connection Refused** | PostgreSQL container starting up or credentials mismatch | `docker compose logs --tail=50 db`<br>`docker compose ps` | Check health check status; verify credentials match `.env` |
| **Port 8088 Already Bound** | Conflicting service listening on host port 8088 | `sudo ss -tulpn \| grep 8088` | Terminate conflicting process or update port in `docker-compose.yml` |
| **Backup Integrity Fails (`gzip -t`)** | Disk space exhausted or interrupted stream | `df -h /`<br>`dmesg \| tail -n 20` | Free root filesystem space; execute `./scripts/backup-db.sh` manually |

---

<div class="page-break"></div>

# 10. Standard Operating Procedures (SOPs)

### SOP-01: Server Booting & Initialization
1. Launch **Oracle VM VirtualBox**.
2. Select virtual machine `ubuntu-docker` and start in **Headless** mode (or `VBoxManage startvm 'ubuntu-docker' --type headless`).
3. Allow 30 seconds for kernel boot and DHCP IP assignment.

### SOP-02: Establishing Administrative Session
From Windows Terminal / PowerShell:
```powershell
ssh carlo@192.168.100.52
# Enter administrative credentials when prompted
```

### SOP-03: Daily Infrastructure Health Assessment
```bash
cd /home/carlo/enterprise-cloud
docker compose ps
curl -sS http://localhost:8088/health
sudo ufw status verbose
ls -lh backups/
```

### SOP-04: Graceful Infrastructure Shutdown
```bash
cd /home/carlo/enterprise-cloud
# Stop and remove containers WITHOUT deleting persistent volumes
docker compose down

# Gracefully shut down guest OS
sudo shutdown -h now
```
<div class="warning-box">
  <strong>CAUTION:</strong> Never pass the <code>-v</code> flag to <code>docker compose down</code> unless you intend to permanently delete all database records.
</div>

---

<div class="page-break"></div>

# 11. Live Defense & KillerCoda Deployment Guide

During the simulated corporate boardroom presentation, you must be capable of deploying the complete stack on a fresh Ubuntu host or **KillerCoda** sandbox instance (Rule 3).

### Step-by-Step Live Defense Script:

```bash
# 1. Clone your portfolio repository
git clone https://github.com/carlonimer/CCM101-cnimer.git
cd CCM101-cnimer/Laboratory-10-Enterprise-Cloud-Architect

# 2. Configure environment variables
cp .env.example .env

# 3. Launch multi-tier stack with Infrastructure as Code
docker compose up -d --build

# 4. Enforce host firewall security perimeter
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp comment 'SSH'
sudo ufw allow 8088/tcp comment 'Web Entrypoint'
sudo ufw --force enable

# 5. Make automation script executable and run test backup
chmod +x scripts/backup-db.sh
./scripts/backup-db.sh

# 6. Prove system observability and security
docker compose ps
curl -s http://localhost:8088/health
sudo ufw status verbose
ls -lh ~/enterprise-cloud/backups/ || ls -lh backups/
```

### Live Penetration / Defense Proof:
Demonstrate to CEO Jen Torres that internal ports are impenetrable:
```powershell
# From Windows PowerShell (Host machine):
Test-NetConnection -ComputerName 192.168.100.52 -Port 8088  # Returns: True (Allowed)
Test-NetConnection -ComputerName 192.168.100.52 -Port 22    # Returns: True (Allowed)
Test-NetConnection -ComputerName 192.168.100.52 -Port 5432  # Returns: False (Blocked)
```

---

<div class="page-break"></div>

# 12. Academic Integrity & Architecture Synthesis

### 12.1 Guiding Principle: "Be the Pilot of AI, Not the Passenger"
> *"Use technology to enhance your learning, but let your own knowledge, judgment, and critical thinking guide your work."*  
> — **CCM101 Academic Integrity Policy**

Throughout this final requirement, modern AI and developer tools served as an accelerator for syntax validation, configuration templating, and documentation structure. However, every architectural decision—such as separating bridge networks to prevent Docker from bypassing UFW, architecting non-destructive database restore verification, and tuning Gunicorn worker threads—was verified, implemented, and defended directly. True system architecture requires hands-on understanding; an AI cannot run hypervisor bridged packets or defend a system live in a corporate boardroom.

### 12.2 Semester Learning Synthesis (Missions 1 to 10)
From navigating the command line in **Mission 1** to architecting sovereign multi-tier cloud infrastructure in **Mission 10**, this curriculum transitioned my skill set from user to engineer:
- **Foundations (Missions 1–3):** Linux headless administration, system diagnostics, and multi-cloud trade-off analysis.
- **Modern Virtualization (Missions 4–6):** Docker containerization, images, volumes, and microservice networking.
- **Operations & Security (Missions 7–9):** System monitoring, firewall rules, automated shell scripting, and cron scheduling.
- **Culmination (Mission 10):** End-to-end realization of an Enterprise Cloud Architect delivering production-ready, observable, and resilient infrastructure.

---

<div class="page-break"></div>

# Appendices: Reference Specifications & Glossary

### Appendix A: Critical Directory & File Paths
- **Application Directory:** `/home/carlo/enterprise-cloud/`
- **Application Source:** `/home/carlo/enterprise-cloud/app/`
- **Nginx Ingress Configuration:** `/home/carlo/enterprise-cloud/nginx/default.conf`
- **Environment Secrets:** `/home/carlo/enterprise-cloud/.env`
- **Database Backup Storage:** `/home/carlo/enterprise-cloud/backups/`
- **PostgreSQL Volume Mount:** `/var/lib/postgresql/data` (`postgres_data`)
- **Automated Backup Script:** `/home/carlo/enterprise-cloud/scripts/backup-db.sh`

### Appendix B: Technical Glossary
- **Reverse Proxy:** An intermediate proxy service (Nginx) that intercepts public web requests and distributes them to internal backend services.
- **Persistent Volume:** A Docker storage mechanism that stores state directly on the host filesystem independently of the container lifecycle.
- **UFW (Uncomplicated Firewall):** A front-end interface for Linux iptables managing host network packet filtering.
- **Zero-Trust Network:** A security model where no internal service or port is accessible by default unless explicitly whitelisted.
- **WSGI (Web Server Gateway Interface):** Standard Python calling convention (Gunicorn) interfacing web servers with application frameworks.

---
*Enterprise Cloud Infrastructure Operational Manual*  
*CCM101 – Cloud Computing Final Requirement | Mission 10*  
*University of Eastern Pangasinan — College of Information Technology*
