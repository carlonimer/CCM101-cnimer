# Cloud Computing Portfolio (CCM101)
**Student Name:** Carlo Nimer  
**Institution:** University of Eastern Pangasinan — College of Information Technology  
**Program & Section:** Bachelor of Science in Information Technology (BSIT - 4J)  
**Instructor:** Jenkielyn C. Torres  

Welcome to my Cloud Computing Portfolio repository for **CCM101**. This portfolio showcases the hands-on laboratories, system blueprints, virtualization setups, containerized environments, security configurations, and automation scripts developed throughout the semester.

---

## Laboratory Activities Directory

| Mission / Lab | Title | Status | Link |
| :--- | :--- | :---: | :--- |
| **Laboratory 01** | Welcome to the Cloud (Linux Foundations & System Info) | Completed | [Explore Lab 01](Laboratory-01-Welcome-to-the-Cloud/) |
| **Laboratory 02** | Build the Cloud Infrastructure Blueprint | Completed | [Explore Lab 02](Laboratory-02-Build-the-Cloud-Infrastructure-Blueprint/) |
| **Laboratory 03** | Multi-Cloud Explorer | Completed | [Explore Lab 03](Laboratory-03-Multi-Cloud-Explorer/) |
| *Missions 04–09* | Cloud-Native Containers, Networking & Automation | Completed | *Course Progression* |
| **Laboratory 10 (Capstone)** | **Mission 10: The Enterprise Cloud Architect** | **Completed** | [**Explore Lab 10 Capstone**](Laboratory-10-Enterprise-Cloud-Architect/) |

---

## Capstone Highlight: Mission 10 (The Enterprise Cloud Architect)
For the final mission, I stepped into the role of **Enterprise Cloud Architect** for the simulated company *CloudNova Technologies* to design, deploy, and defend a sovereign, multi-tier enterprise cloud infrastructure:
* **Architecture:** 3-tier decoupled architecture featuring an Nginx reverse proxy (host port `8088`), Python Flask application tier served by Gunicorn (internal port `5000`), and PostgreSQL 16 database tier (internal port `5432`).
* **Network Segmentation:** Dual Docker bridge networks (`frontend` and `backend`), with `backend` set to `internal: true` so the database cannot communicate with or be reached from external networks.
* **Storage Persistence:** Named volume (`enterprise-cloud_postgres_data`) ensuring 100% database persistence across container recreations and host reboots.
* **Perimeter Security:** Hardened Ubuntu Server host with Uncomplicated Firewall (UFW) enforcing a Default Deny policy, permitting only SSH (port 22) and web ingress (port 8088).
* **Autonomous Operations:** Executable Bash disaster recovery script (`scripts/backup-db.sh`) with compressed PostgreSQL snapshots (`pg_dump`), automatic 7-day retention cleanup, and scheduled via Cron (`0 2 * * *`).
* **Client Handover Manual:** Complete operational runbook formatted for 5.5" × 8.5" booklet printing.

Explore full documentation, source code, and live demo commands in [`Laboratory-10-Enterprise-Cloud-Architect/`](Laboratory-10-Enterprise-Cloud-Architect/).
