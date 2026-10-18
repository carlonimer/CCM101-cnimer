# Final Course Reflection: Journey of an Enterprise Cloud Architect
**Student Name:** Carlo Nimer  
**Course & Code:** CCM101 – Cloud Computing  
**Section:** BSIT - 4J  
**Instructor:** Jenkielyn C. Torres  
**Institution:** College of Information Technology, University of Eastern Pangasinan  
**Date:** October 2026  

---

## 1. Executive Reflection: The Architectural Transformation

When I first began CCM101 in **Mission 1: Welcome to the Cloud**, I stepped into the role of a Junior Trainee at the simulated CloudNova Technologies. At that starting point, cloud computing seemed like an abstract, distant concept—often associated only with web interfaces or cloud storage drives. Learning fundamental headless Linux commands, understanding SSH keys, navigating directories without a graphical user interface, and manipulating file permissions laid the essential groundwork for everything that followed.

As the curriculum progressed through **Missions 2 through 9**, the challenges shifted from merely operating within a single virtual machine to understanding cloud-native design principles. Moving through infrastructure blueprinting, multi-cloud evaluation, virtualization, containerization with Docker, network segmentation, and automation scripts gradually transitioned my mindset from that of an end-user to an infrastructure engineer.

Reaching **Mission 10: The Enterprise Cloud Architect** was our culminating final requirement experience. There was no guided tutorial, no step-by-step handholding, and no safety net. Stepping up to solve a Fortune 500 enterprise brief required synthesizing every core discipline mastered over the semester:
1. Translating business and regulatory requirements into an architectural blueprint.
2. Building an automated, reproducible multi-tier application stack via Infrastructure as Code (`docker-compose.yml`).
3. Locking down the perimeter with host-based firewall policies (`UFW`) and strict network isolation.
4. Designing autonomous operational self-healing and disaster recovery mechanisms via Bash and `cron`.
5. Documenting the infrastructure at an executive level so that any operations team could maintain and restore it.

---

## 2. Technical Hurdles & Architectural Breakthroughs

Throughout Mission 10, several technical decisions and hurdles solidified my practical DevOps understanding:

### A. Container State vs. Persistence
One of the most crucial concepts in cloud architecture is that containers are inherently ephemeral. If a container crashes, restarts, or is destroyed, any data inside its writable layer vanishes. Designing persistent Docker volumes (`cloudnova_db_data` and `cloudnova_wp_data`) that detach state from compute was critical. Testing this by purposely taking the container down and rebooting the entire Ubuntu virtual machine—and observing that the database records and configurations remained 100% intact—demonstrated the power of cloud persistence.

### B. The Docker & Host Firewall Reality
A key architectural discovery was understanding how Docker interacts with Linux `iptables` and host-based firewalls like UFW. Because Docker automatically manipulates `iptables` chains to route traffic to exposed container ports, naively exposing a database port (e.g. `3306:3306`) could inadvertently bypass UFW rules and expose internal databases to external networks. 
To address this in my architecture, the database container was strictly bound only to an internal, isolated Docker bridge network (`cloudnova-network`) with zero public host port mappings. Only the front-end web service on port 80 is reachable, adhering to the principle of least privilege.

### C. Operational Autonomy & Disaster Recovery
Automating disaster recovery via `automation-script.sh` taught me that an unverified backup is no backup at all. Implementing automated database dumps, volume archiving, SHA-256 cryptographic checksums, automated 7-day retention cleanup, and cron scheduling ensures that the infrastructure remains self-sustaining without daily administrative friction.

---

## 3. Academic Integrity & "Being the Pilot of AI"

The guiding principle of this laboratory activity states:  
> *"Be the pilot of AI, not the passenger. Use technology to enhance your learning, but let your own knowledge, judgment, and critical thinking guide your work."*

Throughout this course, utilizing modern development and generative tools has highlighted a crucial reality: AI can suggest syntax, provide boilerplate templates, and assist in drafting technical text, but **AI cannot understand the physical context of your network, diagnose unexpected hypervisor bridge packet drops, or defend an architecture live before an executive board.**

By acting as the **pilot**, I used AI as an accelerator for brainstorming, validating best-practice options, and refining technical documentation. However, every architectural choice—from subnet assignments and volume configurations to firewall rules, bash error-handling logic, and live KillerCoda execution—was verified, implemented, tested, and understood personally. Taking ownership of the system ensures that when CEO Jen Torres or our course instructor probes our security perimeter or questions our disaster recovery runbook, I can explain and defend every single line of code with confidence.

---

## 4. Professional Forward Look

CCM101 has fundamentally altered how I view modern IT systems. Cloud computing is not just about hosting a server; it is about reliability, security, scalability, and automation. 

Moving forward into my academic and professional career in Information Technology, the technical skills honed in this laboratory—Linux systems administration, Docker containerization, Infrastructure as Code, cybersecurity hardening, and operational scripting—will serve as the solid bedrock for my trajectory into Cloud Architecture, DevOps engineering, and secure system administration.
