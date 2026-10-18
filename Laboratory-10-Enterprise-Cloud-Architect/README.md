# Laboratory Activity 10: The Enterprise Cloud Architect
**Course:** CCM101 – Cloud Computing  
**Role:** Enterprise Cloud Architect (CloudNova Technologies)  
**Architect:** Carlo Nimer  
**Section:** BSIT 2A  
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
* **Host Platform:** Windows 11 Workstation running **Oracle VM VirtualBox 7.x** (Type 2 Hypervisor).
* **Base Virtual Machine:** Headless **Ubuntu Server 24.04 LTS** with Bridged Networking on `192.168.100.x` LAN.
* **Security Perimeter:** Host-level **Uncomplicated Firewall (UFW)** with **Default Deny Incoming** policy:
  * Ingress **Port 22/tcp (SSH)**: Allowed for secure administration.
  * Ingress **Port 80/tcp (HTTP)**: Allowed for client web application access.
  * Ingress **Port 3306/tcp (MySQL)**: **Blocked** from external networks; isolated strictly inside Docker bridge network.
* **Container Orchestration (IaC):** Multi-tier **Docker Compose** stack:
  * **Web Tier (`cloudnova-web`):** WordPress 6.5 with Apache & PHP 8.2.
  * **Database Tier (`cloudnova-db`):** MySQL 8.0 Enterprise container with integrated health checks.
  * **Network Isolation:** Private bridge network (`cloudnova-network`).
  * **Persistent Storage:** Docker named volumes (`cloudnova_wp_data`, `cloudnova_db_data`) ensuring data survives restarts and VM reboots.
* **Autonomous Operations & Disaster Recovery:**
  * Custom executable Bash script (`automation-script.sh`) performing automated hot MySQL database dumps, volume archiving, SHA-256 integrity verification, and 7-day retention rotation.
  * Automated execution via **Cron** (`0 2 * * *`).

---

## Deliverables Directory

| File | Description | Link |
| :--- | :--- | :--- |
| **`architecture-diagram.png`** | Full enterprise network topology and container isolation diagram | [View Diagram](architecture-diagram.png) |
| **`docker-compose.yml`** | Production multi-tier Infrastructure-as-Code stack definition | [View File](docker-compose.yml) |
| **`automation-script.sh`** | Autonomous disaster recovery, backup, and rotation bash script | [View File](automation-script.sh) |
| **`operational-manual.md`** | Comprehensive Client Handover Manual (Formatted for 5.5" x 8.5" Booklet) | [View Manual](operational-manual.md) |
| **`final-reflection.md`** | Personal capstone reflection synthesizing journey from Mission 1 to 10 | [View Reflection](final-reflection.md) |

---

## Quick Start / Live Defense Deployment Guide

To deploy this entire infrastructure on any fresh Ubuntu host or **KillerCoda** sandbox instance:

```bash
# 1. Clone repository & enter Mission 10 directory
git clone https://github.com/carlonimer/CCM101-cnimer.git
cd CCM101-cnimer/Laboratory-10-Enterprise-Cloud-Architect

# 2. Deploy multi-tier containerized stack
docker compose up -d

# 3. Configure and activate host firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp comment 'SSH'
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw --force enable

# 4. Make operational script executable & run test backup
chmod +x automation-script.sh
sudo ./automation-script.sh --run

# 5. Verify system status
docker compose ps
sudo ufw status verbose
ls -lh /var/backups/cloudnova
```

---
*Developed for CCM101 Final Mission Defense.*
