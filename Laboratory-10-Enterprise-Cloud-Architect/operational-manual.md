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
    <strong>Application Stack:</strong> WordPress + MySQL<br>
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
1. [Executive Briefing & Mission Scope](#1-executive-briefing--mission-scope)
2. [Architecture & Network Topology](#2-architecture--network-topology)
3. [Base Infrastructure Provisioning](#3-base-infrastructure-provisioning)
4. [Containerized Deployment (Infrastructure as Code)](#4-containerized-deployment-infrastructure-as-code)
5. [Host-Based Perimeter Hardening (UFW)](#5-host-based-perimeter-hardening-ufw)
6. [Autonomous Operations & Disaster Recovery Automation](#6-autonomous-operations--disaster-recovery-automation)
7. [Disaster Recovery & Data Restoration Runbook](#7-disaster-recovery--data-restoration-runbook)
8. [System Verification & Observability](#8-system-verification--observability)
9. [KillerCoda Live Defense Quick-Start Guide](#9-killercoda-live-defense-quick-start-guide)

---

# 1. Executive Briefing & Mission Scope

CloudNova Technologies was contracted by a Fortune 500 enterprise to architect and deploy a sovereign, automated, and hardened private cloud application environment.

### Core Architecture Pillars:
- **Multi-Tier Segregation**: Web application front-end decoupled from backend database storage.
- **State Persistence**: Storage volumes configured to survive container recreation and physical host reboots.
- **Zero-Trust Perimeter**: Default-deny firewall policy permitting only strictly necessary administration and presentation ports.
- **Operational Autonomy**: Automated daily hot database backups, tarball volume archives, SHA-256 integrity hashing, and automated retention rotation without human intervention.
- **Reproducibility**: Complete Infrastructure-as-Code (IaC) deployable in under 3 minutes on any Linux host or ephemeral testing node (KillerCoda).

---

# 2. Architecture & Network Topology

The infrastructure leverages a layered defense-in-depth model separating physical hardware, virtualization, host operating system security, container orchestration, and isolated internal bridge networks.

![Enterprise Cloud Architecture Diagram](architecture-diagram.png)

### Topology Specification:
| Component | Technology | IP / Network Binding | Description |
| :--- | :--- | :--- | :--- |
| **Physical Host** | Windows 11 Laptop | `192.168.100.x` | Workstation running hypervisor |
| **Hypervisor** | Oracle VM VirtualBox (Type 2) | Bridged Adapter (`RTL8852BE`) | Bridges VM directly onto local physical LAN |
| **Guest OS** | Ubuntu Server 24.04 LTS (Headless) | DHCP on LAN (`192.168.100.x`) | Hardened minimal Linux server environment |
| **Host Firewall** | UFW (Uncomplicated Firewall) | Kernel `iptables` | Enforces Default Deny Incoming; Allows 22/tcp, 80/tcp |
| **Docker Engine** | Docker Community Engine v26+ | `cloudnova-network` (Bridge) | Container runtime and orchestration |
| **Web Service** | WordPress 6.5 (Apache / PHP 8.2) | `0.0.0.0:80 -> 80/tcp` | Presentation layer serving client web traffic |
| **Database** | MySQL 8.0 Enterprise Container | Internal: `3306/tcp` (No host binding) | Isolated persistence engine; strictly unreachable from outside |
| **Storage Volumes** | Docker Named Volumes | Host local `/var/lib/docker/volumes` | `cloudnova_wp_data` and `cloudnova_db_data` |

---

# 3. Base Infrastructure Provisioning

### 3.1. Virtual Machine Specifications
1. **Hypervisor**: Oracle VM VirtualBox 7.x
2. **Guest OS**: Ubuntu Server 24.04 LTS (64-bit Headless)
3. **Compute Allocation**: 2 vCPUs, 2048 MB RAM
4. **Virtual Storage**: 25 GB VDI (Dynamically allocated)
5. **Network Configuration**:
   - Adapter 1: **Bridged Adapter** attached to active physical Wi-Fi/Ethernet interface.
   - Promiscuous Mode: Allow All (or Deny with standard bridging).

### 3.2. Initial Host Preparation
Once Ubuntu Server is installed and booted, verify network address allocation:
```bash
# Identify assigned IP address
ip -br addr show

# Update package repositories and upgrade baseline security packages
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git tar gzip ufw ca-certificates gnupg lsb-release
```

---

# 4. Containerized Deployment (Infrastructure as Code)

### 4.1. Docker & Docker Compose Engine Installation
Install the official Docker Engine and Docker Compose plugin:
```bash
# Set up Docker official repository keyrings
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker engine and compose
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Grant non-root execution permissions to current user
sudo usermod -aG docker $USER
```

### 4.2. Infrastructure Stack Definition (`docker-compose.yml`)
Deploy the enterprise stack utilizing declarative configuration:
```yaml
version: '3.8'

services:
  database:
    image: mysql:8.0
    container_name: cloudnova-db
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: CloudNovaRootSecure2026!
      MYSQL_DATABASE: cloudnova_wp
      MYSQL_USER: cloudnova_user
      MYSQL_PASSWORD: CloudNovaUserSecret2026!
    volumes:
      - db_data:/var/lib/mysql
    networks:
      - cloudnova-net
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-pCloudNovaRootSecure2026!"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 768M

  web:
    image: wordpress:6.5-apache
    container_name: cloudnova-web
    restart: unless-stopped
    depends_on:
      database:
        condition: service_healthy
    ports:
      - "80:80"
    environment:
      WORDPRESS_DB_HOST: database:3306
      WORDPRESS_DB_NAME: cloudnova_wp
      WORDPRESS_DB_USER: cloudnova_user
      WORDPRESS_DB_PASSWORD: CloudNovaUserSecret2026!
      WORDPRESS_TABLE_PREFIX: wp_
    volumes:
      - wp_data:/var/www/html
    networks:
      - cloudnova-net
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:80/ || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 20s
    deploy:
      resources:
        limits:
          memory: 512M

volumes:
  db_data:
    name: cloudnova_db_data
    driver: local
  wp_data:
    name: cloudnova_wp_data
    driver: local

networks:
  cloudnova-net:
    name: cloudnova-network
    driver: bridge
```

### 4.3. Launching the Infrastructure
```bash
# Provision and launch containers in detached background daemon mode
docker compose up -d

# Verify container runtime health
docker compose ps
```

---

# 5. Host-Based Perimeter Hardening (UFW)

To fulfill **Requirement 3**, the Ubuntu host must enforce strict ingress controls.

### 5.1. Implementing Default Deny Policy
```bash
# Reset UFW to known baseline
sudo ufw --force reset

# Set default security policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Explicitly permit Remote Administration (SSH)
sudo ufw allow 22/tcp comment "SSH Remote Management"

# Explicitly permit Web Traffic (HTTP)
sudo ufw allow 80/tcp comment "HTTP CloudNova Web App"

# Optional: Allow HTTPS for future SSL/TLS offloading
sudo ufw allow 443/tcp comment "HTTPS Secure Web App"

# Activate firewall
sudo ufw --force enable
```

### 5.2. Audit Firewall Status
Verify active rules:
```bash
sudo ufw status verbose
```
*Expected Output:*
```text
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere (SSH Remote Management)
80/tcp                     ALLOW IN    Anywhere (HTTP CloudNova Web App)
443/tcp                    ALLOW IN    Anywhere (HTTPS Secure Web App)
```

### 5.3. Enterprise Defense Architecture Note: The "Docker-UFW" Perimeter
Standard Docker installations inject rules directly into `iptables` PREROUTING chains, which can bypass UFW if host port bindings are exposed (e.g. `-p 3306:3306`).
**CloudNova Architectural Defense**:
1. Database port `3306` is **never mapped to host interfaces** in `docker-compose.yml`. It exists solely on `cloudnova-network`.
2. Even if an adversary probes host IP on Port 3306, the host kernel rejects the connection because no daemon is listening on host port 3306, and UFW rejects all unmapped incoming traffic.

---

# 6. Autonomous Operations & Disaster Recovery Automation

To fulfill **Requirement 4**, operational tasks are managed autonomously via a custom Bash script and cron scheduling.

### 6.1. Script Deployment
Create and assign execute permissions to `automation-script.sh`:
```bash
# Make script executable
chmod +x automation-script.sh

# Deploy to operational directory
sudo mkdir -p /opt/cloudnova
sudo cp automation-script.sh /opt/cloudnova/
```

### 6.2. Script Capabilities Summary
- **Database Dump**: Executes hot transaction backup of MySQL database without locking tables (`--single-transaction`).
- **Volume Tarball**: Spawns an ephemeral alpine worker to snapshot `/var/www/html` persistent storage.
- **Cryptographic Hashes**: Generates SHA-256 checksums of every backup artifact for audit validation.
- **Retention Rotation**: Automatically purges archives older than 7 days to prevent disk exhaustion.
- **Health Logging**: Comprehensive timestamped logs written to `/var/log/cloudnova-backup.log`.

### 6.3. Manual Execution & Verification
```bash
# Perform manual test run
sudo /opt/cloudnova/automation-script.sh --run

# View generated archives
sudo /opt/cloudnova/automation-script.sh --list

# View execution log
tail -n 25 /var/log/cloudnova-backup.log
```

### 6.4. Cron Job Scheduling
Configure the system scheduler (`cron`) to execute the operational backup autonomously every morning at 02:00 AM:
```bash
# Edit root crontab
sudo crontab -e
```
Add the following configuration line:
```cron
# CloudNova Autonomous Operations Backup Schedule (Daily at 2:00 AM)
0 2 * * * /opt/cloudnova/automation-script.sh --run >> /var/log/cloudnova-backup.log 2>&1
```

---

# 7. Disaster Recovery & Data Restoration Runbook

In the event of accidental data corruption, deletion, or container compromise, follow this step-by-step restoration procedure:

### Step 1: Identify Target Backup Set
```bash
ls -lh /var/backups/cloudnova/
# Example files:
# db_cloudnova_wp_20261018_020000.sql.gz
# wp_volume_20261018_020000.tar.gz
# checksums_20261018_020000.sha256
```

### Step 2: Validate Cryptographic Checksum
```bash
cd /var/backups/cloudnova
sha256sum -c checksums_20261018_020000.sha256
```

### Step 3: Restore MySQL Database Dump
```bash
# Stream decompressed SQL dump directly into MySQL container
gunzip < /var/backups/cloudnova/db_cloudnova_wp_20261018_020000.sql.gz | \
  docker exec -i cloudnova-db mysql -u root -pCloudNovaRootSecure2026! cloudnova_wp
```

### Step 4: Restore Web Persistent Volume
```bash
# Clear corrupted data and extract backup into volume
docker run --rm \
  -v cloudnova_wp_data:/target \
  -v /var/backups/cloudnova:/backup:ro \
  alpine sh -c "rm -rf /target/* && tar -xzf /backup/wp_volume_20261018_020000.tar.gz -C /target"
```

### Step 5: Restart Application Stack
```bash
docker compose restart
docker compose ps
```

---

# 8. System Verification & Observability

During the executive defense, use these verification commands to prove system stability and compliance:

### 1. Verify Multi-Tier Services Online
```bash
docker compose ps
```
*Criteria*: Both `cloudnova-web` and `cloudnova-db` must report status `Up (healthy)`.

### 2. Verify Data Persistence Across VM Reboot
```bash
# 1. Add a test post in WordPress at http://<VM_IP>/
# 2. Reboot the virtual machine:
sudo reboot
# 3. Once rebooted, verify containers auto-started:
docker ps
# 4. Access browser: Post and configuration remain intact.
```

### 3. Verify Firewall Integrity (Port Scan Defense)
Run from the Host Machine (PowerShell):
```powershell
# Test allowed web port (Must succeed)
Test-NetConnection -ComputerName <VM_IP> -Port 80

# Test allowed SSH port (Must succeed)
Test-NetConnection -ComputerName <VM_IP> -Port 22

# Test blocked database port (Must fail / time out)
Test-NetConnection -ComputerName <VM_IP> -Port 3306
```

---

# 9. KillerCoda Live Defense Quick-Start Guide

If requested to deploy the entire environment live during the defense on a fresh **KillerCoda Ubuntu playground**, execute these commands sequentially:

```bash
# 1. Clone repository
git clone https://github.com/carlonimer/CCM101-cnimer.git
cd CCM101-cnimer/Laboratory-10-Enterprise-Cloud-Architect

# 2. Deploy multi-tier infrastructure
docker compose up -d

# 3. Configure and activate UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw --force enable

# 4. Make automation script executable and run test backup
chmod +x automation-script.sh
sudo ./automation-script.sh --run

# 5. Verify system status
docker compose ps
sudo ufw status verbose
ls -lh /var/backups/cloudnova
```
*Total Deployment Time: ~90 seconds.*

---
**Document Sign-Off:**  
*Enterprise Cloud Architect:* **Carlo Nimer**  
*Course Instructor:* **Jenkielyn C. Torres**  
*College of Information Technology, University of Eastern Pangasinan*
