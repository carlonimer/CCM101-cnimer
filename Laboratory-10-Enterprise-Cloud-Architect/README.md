# Laboratory Activity 10: The Enterprise Cloud Architect
**Course:** CCM101 – Cloud Computing  
**Role:** Enterprise Cloud Architect (CloudNova Technologies)  
**Architect:** Carlo Nimer | John Earl Valdez
**Section:** BSIT - 4J  
**Instructor:** Jenkielyn C. Torres  
**Institution:** University of Eastern Pangasinan — College of Information Technology  

---

## Mission Brief
> *"We just signed a blank-check contract with a Fortune 500 company. They need a highly secure, automated, and observable private cloud environment... I am not giving you a tutorial. You are the Architect now. Build the system, document the operational manual, and prepare to present your infrastructure to me live."*  
> — **Jen Torres, CEO of CloudNova Technologies**

---

## Infrastructure Topology & Architecture

![CloudNova Enterprise Cloud Topology](architecture-diagram.png)

### Key Architecture Components
* **Host Platform:** Windows 11 Workstation running **Oracle VM VirtualBox 7.x** (Type 2 Hypervisor, 4 GB RAM, 2 vCPUs).
* **Base Virtual Machine:** Headless **Ubuntu Server 24.04 LTS** with Bridged Networking on `192.168.100.x` LAN (`192.168.100.52`).
* **Security Perimeter:** Host-level **Uncomplicated Firewall (UFW)** with **Default Deny Incoming** policy:
  * Ingress **Port 22/tcp (SSH)**: Allowed for remote administration from PowerShell.
  * Ingress **Port 8088/tcp (HTTP)**: Allowed for Nginx web application entrypoint.
  * Ingress **Port 5432/tcp (PostgreSQL)** & **Port 5000/tcp (Flask)**: **Blocked** from external networks; isolated strictly inside Docker bridge networks.
* **Container Orchestration (IaC):** Multi-tier **Docker Compose** stack:
  * **Tier 1 (Reverse Proxy):** Nginx (`enterprise-cloud-nginx-1`) listening on host port `8088`, forwarding client traffic to the Flask application.
  * **Tier 2 (Application):** Flask application served by Gunicorn (`enterprise-cloud-app-1`) on internal port `5000`.
  * **Tier 3 (Database):** PostgreSQL 16 (`enterprise-cloud-db-1`) on internal port `5432`.
  * **Network Isolation:** Dual-network design with `frontend` bridge and `backend` isolated network (`internal: true`).
  * **Persistent Storage:** Named Docker volume (`enterprise-cloud_postgres_data`) ensuring database state survives container restarts and VM reboots.
* **Autonomous Operations & Disaster Recovery:**
  * Custom executable Bash script (`scripts/backup-db.sh` / `automation-script.sh`) performing automated compressed PostgreSQL snapshots (`pg_dump`), temporary file safety cleanup, and 7-day retention rotation.
  * Automated execution via **Cron** (`0 2 * * * /home/carlo/enterprise-cloud/scripts/backup-db.sh >> /home/carlo/enterprise-cloud/backups/backup.log 2>&1`).

---

## Deliverables Directory

| File / Folder | Description | Link |
| :--- | :--- | :--- |
| **`architecture-diagram.png`** | Enterprise network topology diagram (Host $\rightarrow$ VirtualBox $\rightarrow$ Ubuntu $\rightarrow$ UFW $\rightarrow$ Nginx $\rightarrow$ Flask $\rightarrow$ PostgreSQL) | [View Diagram](architecture-diagram.png) |
| **`docker-compose.yml`** | Production multi-tier Infrastructure-as-Code stack definition | [View File](docker-compose.yml) |
| **`automation-script.sh`** | Autonomous PostgreSQL backup and rotation bash script | [View File](automation-script.sh) |
| **`operational-manual.md`** | Comprehensive Client Handover Manual (Formatted for 5.5" x 8.5" Booklet) | [View Manual](operational-manual.md) |
| **`final-reflection.md`** | Personal final reflection synthesizing journey from Mission 1 to 10 | [View Reflection](final-reflection.md) |
| **`app/`** | Application tier source code (Flask app, Gunicorn, Dockerfile) | [Explore App](app/) |
| **`nginx/`** | Reverse proxy configuration (`default.conf`) | [Explore Nginx](nginx/) |
| **`scripts/`** | Operational scripts (`backup-db.sh`) | [Explore Scripts](scripts/) |

---

## Quick Start / Live Defense Deployment Guide

To deploy this entire infrastructure on any fresh Ubuntu host or **KillerCoda** sandbox instance:

```bash
# 1. Clone repository & enter Mission 10 directory
git clone https://github.com/carlonimer/CCM101-cnimer.git
cd CCM101-cnimer/Laboratory-10-Enterprise-Cloud-Architect

# 2. Configure environment variables
cp .env.example .env

# 3. Deploy multi-tier containerized stack
docker compose up -d --build

# 4. Configure and activate host firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp comment 'SSH'
sudo ufw allow 8088/tcp comment 'CloudNova Web App'
sudo ufw --force enable

# 5. Make operational script executable & run test backup
chmod +x scripts/backup-db.sh
./scripts/backup-db.sh

# 6. Verify system status
docker compose ps
sudo ufw status verbose
ls -lh ~/enterprise-cloud/backups
curl -s http://localhost:8088/health
```

---
*Developed for CCM101 Final Mission Defense.*
