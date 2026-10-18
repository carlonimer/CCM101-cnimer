<style>
  @page {
    size: 5.5in 8.5in;
    margin: 0.5in;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #1a1a1a;
  }
  h1 { font-size: 16pt; margin-top: 1.2em; border-bottom: 2px solid #2563eb; padding-bottom: 4px; }
  h2 { font-size: 13pt; margin-top: 1em; color: #1e3a8a; }
  h3 { font-size: 11pt; margin-top: 0.8em; }
  code { font-family: "Courier New", Courier, monospace; font-size: 9pt; background: #f1f5f9; padding: 2px 4px; border-radius: 4px; }
  pre { background: #0f172a; color: #f8fafc; padding: 10px; border-radius: 6px; overflow-x: auto; font-size: 8pt; }
  .page-break { page-break-after: always; }
  .cover-page {
    text-align: center;
    padding-top: 1.5in;
    padding-bottom: 1.5in;
  }
  .cover-title { font-size: 18pt; font-weight: bold; margin-bottom: 8px; color: #0f172a; }
  .cover-subtitle { font-size: 13pt; color: #2563eb; font-weight: 600; margin-bottom: 24px; }
  .cover-meta { font-size: 10pt; line-height: 1.8; margin-top: 40px; color: #334155; }
</style>

<div class="cover-page">
  <p style="text-transform: uppercase; letter-spacing: 2px; font-weight: bold; color: #64748b; font-size: 9pt; margin-bottom: 10px;">
    University of Eastern Pangasinan — College of Information Technology
  </p>
  <div class="cover-title">CCM101 - Cloud Computing</div>
  <div class="cover-subtitle">Enterprise Cloud Architect – Operational Manual</div>
  <hr style="width: 60%; margin: 20px auto; border: 0; border-top: 2px solid #2563eb;" />
  <div class="cover-meta">
    <strong>Project:</strong> Secure Multi-Tier Web Application<br>
    <strong>Application Stack:</strong> Nginx + Flask/Gunicorn + PostgreSQL 16<br>
    <strong>Prepared by:</strong> Carlo Nimer<br>
    <strong>Section:</strong> BSIT 2A<br>
    <strong>Instructor:</strong> Jenkielyn C. Torres<br>
    <strong>Date:</strong> October 2026<br>
    <br>
    <em>FORMAT SPECIFICATION: Coupon 5.5" x 8.5" Operational Manual (Portrait)</em>
  </div>
</div>

<div class="page-break"></div>

# Table of Contents
1. [Executive Briefing & Architecture Overview](#1-executive-briefing--architecture-overview)
2. [Network Topology & Port Map](#2-network-topology--port-map)
3. [Base Infrastructure Provisioning](#3-base-infrastructure-provisioning)
4. [Container Orchestration & IaC Deployment](#4-container-orchestration--iac-deployment)
5. [Host-Based Perimeter Security (UFW)](#5-host-based-perimeter-security-ufw)
6. [Operational Automation & Backup Script](#6-operational-automation--backup-script)
7. [Disaster Recovery & Restoration Runbook](#7-disaster-recovery--restoration-runbook)
8. [Live Defense Demonstration Runbook](#8-live-defense-demonstration-runbook)

---

# 1. Executive Briefing & Architecture Overview

CloudNova Technologies designed and provisioned a sovereign, automated, multi-tier enterprise cloud infrastructure for Fortune 500 client operations.

![Enterprise Cloud Architecture](architecture-diagram.png)

### Key Architectural Pillars:
* **Presentation Tier:** Nginx reverse proxy listening on host port `8088`.
* **Application Tier:** Python Flask WSGI application served by Gunicorn on internal port `5000`.
* **Database Tier:** PostgreSQL 16 Enterprise Database listening on internal port `5432`.
* **State Persistence:** Named Docker volume (`enterprise_cloud_postgres_data`) detached from compute, ensuring 100% data survival across container recreations and host reboots.
* **Perimeter Hardening:** Host-based Uncomplicated Firewall (UFW) enforcing a Default Deny policy.
* **Autonomous Operations:** Automated hot PostgreSQL backups (`pg_dump`) compressed with gzip, cryptographic SHA-256 verification, and 7-day automated retention rotation via Cron.

---

# 2. Network Topology & Port Map

| Component | Layer / Service | IP / Port Binding | Accessibility |
| :--- | :--- | :--- | :--- |
| **Host Workstation** | Windows 11 Laptop | `192.168.100.46` | Presentation & PowerShell SSH Admin |
| **Hypervisor** | Oracle VM VirtualBox 7.x | Bridged Realtek Wi-Fi Adapter | Bridges VM into physical LAN |
| **Linux VM** | Ubuntu Server 24.04 LTS | `192.168.100.52` | Hardened Linux Host OS |
| **Host Firewall** | UFW | Ports 22 & 8088 Allowed | Rejects all unmapped ports by default |
| **Reverse Proxy** | Nginx Alpine Container | `0.0.0.0:8088 -> 80/tcp` | Public HTTP Entrypoint |
| **Application** | Flask / Gunicorn Container | Internal `5000/tcp` | Accessible only via Docker Network |
| **Database** | PostgreSQL 16 Alpine | Internal `5432/tcp` | Strictly isolated; NO host port binding |

---

# 3. Base Infrastructure Provisioning

### VM Hardware Specifications:
- **Compute:** 2 vCPUs, 4096 MB RAM
- **Storage:** 30 GB VDI Virtual Disk
- **Networking:** Adapter 1 Bridged to host Wi-Fi adapter

### Connecting from PowerShell:
The Ubuntu VM is fully accessible from Windows PowerShell for presentation and demonstration:
```powershell
ssh carlo@192.168.100.52
# Password: [Your User Password]
```

---

# 4. Container Orchestration & IaC Deployment

The entire multi-tier stack is declared in `docker-compose.yml`:

```bash
cd ~/enterprise-cloud
docker compose up -d
docker compose ps
```

### Health Verification Endpoint:
```bash
curl -sS http://localhost:8088/health
# Response: {"database":"connected","status":"healthy"}
```

---

# 5. Host-Based Perimeter Security (UFW)

Enforce host hardening using Uncomplicated Firewall:

```bash
# 1. Reset and establish baseline policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 2. Allow SSH remote administration
sudo ufw allow 22/tcp comment 'SSH Administration'

# 3. Allow Nginx Web Application Port
sudo ufw allow 8088/tcp comment 'CloudNova Web App'

# 4. Enable firewall
sudo ufw --force enable

# 5. Verify active rules
sudo ufw status verbose
```

---

# 6. Operational Automation & Backup Script

The automation script (`./scripts/backup-db.sh` or `automation-script.sh`) manages disaster recovery:

```bash
chmod +x ./scripts/backup-db.sh
./scripts/backup-db.sh
```

### Cron Job Automation:
Configure the scheduler to execute automatically:
```bash
crontab -e
```
Add the following entry:
```cron
# Execute CloudNova PostgreSQL backup daily at 02:00 AM
0 2 * * * /home/carlo/enterprise-cloud/scripts/backup-db.sh >> /var/log/cloudapp-backup.log 2>&1
```

---

# 7. Disaster Recovery & Restoration Runbook

### Step 1: Locate Latest Snapshot
```bash
ls -lht ~/enterprise-cloud/backups/*.sql.gz | head -n 3
```

### Step 2: Restore Database
```bash
gunzip < ~/enterprise-cloud/backups/cloudapp_[TIMESTAMP].sql.gz | \
  docker exec -i enterprise-cloud-db-1 psql -U clouduser -d cloudapp
```

---

# 8. Live Defense Demonstration Runbook

During the boardroom demonstration:

1. **Demonstrate Web App Response (from Windows Browser):**  
   Open `http://192.168.100.52:8088` in Chrome/Edge.  
   Expected JSON: `{"application":"Flask","database":"connected","project":"Enterprise Cloud Infrastructure",...}`
2. **Demonstrate Port Security (from Windows PowerShell):**
   ```powershell
   Test-NetConnection -ComputerName 192.168.100.52 -Port 8088 # Success
   Test-NetConnection -ComputerName 192.168.100.52 -Port 22   # Success
   Test-NetConnection -ComputerName 192.168.100.52 -Port 5432 # Failed (Securely Blocked)
   ```
3. **Demonstrate Automated Disaster Recovery:**
   ```bash
   ./scripts/backup-db.sh
   ls -lh ~/enterprise-cloud/backups/
   ```
4. **Demonstrate Reboot Persistence:**
   ```bash
   sudo reboot
   # After reboot: docker ps verifies containers automatically recovered.
   ```

---
*Signed by Enterprise Cloud Architect:* **Carlo Nimer**  
*Course Instructor:* **Jenkielyn C. Torres**  
*College of Information Technology, University of Eastern Pangasinan*
