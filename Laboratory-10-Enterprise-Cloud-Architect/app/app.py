import os
import socket
import time
from datetime import datetime
import psycopg2
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudNova Technologies - Enterprise Cloud Portal</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #070a13;
            --bg-card: rgba(15, 23, 42, 0.75);
            --bg-card-hover: rgba(30, 41, 59, 0.85);
            --border-glow: rgba(59, 130, 246, 0.25);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-purple: #a855f7;
            --accent-emerald: #10b981;
            --accent-emerald-glow: rgba(16, 185, 129, 0.2);
            --accent-amber: #f59e0b;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
                radial-gradient(at 50% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 2.5rem 1.5rem;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
            width: 100%;
            flex: 1;
        }

        /* Header */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--border-subtle);
            flex-wrap: wrap;
            gap: 1rem;
        }

        .brand-block {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .brand-logo {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #0284c7, #8b5cf6);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.4);
        }

        .brand-logo svg {
            width: 26px;
            height: 26px;
            fill: #ffffff;
        }

        .brand-text h1 {
            font-size: 1.4rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(to right, #ffffff, #cbd5e1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-text p {
            font-size: 0.8rem;
            color: var(--accent-blue);
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .badge-live {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--accent-emerald-glow);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #34d399;
            padding: 0.4rem 0.9rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.5px;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 10px #10b981;
            animation: pulse 1.8s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        /* Banner */
        .hero-banner {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-glow);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }

        .hero-banner::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399);
        }

        .hero-title {
            font-size: 1.6rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }

        .hero-subtitle {
            color: var(--text-muted);
            font-size: 0.95rem;
            max-width: 750px;
            line-height: 1.6;
        }

        /* Architecture Flow */
        .arch-flow {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2rem;
        }

        .arch-card {
            background: var(--bg-card);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.25s ease;
            position: relative;
        }

        .arch-card:hover {
            transform: translateY(-4px);
            border-color: var(--border-glow);
            box-shadow: 0 8px 25px rgba(56, 189, 248, 0.15);
        }

        .tier-label {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--accent-blue);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.4rem;
        }

        .card-name {
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .status-pill {
            font-size: 0.7rem;
            font-weight: 700;
            padding: 0.2rem 0.5rem;
            border-radius: 6px;
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .meta-list {
            list-style: none;
            font-size: 0.85rem;
            color: var(--text-muted);
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        .meta-list li {
            display: flex;
            justify-content: space-between;
        }

        .mono {
            font-family: 'JetBrains Mono', monospace;
            color: #e2e8f0;
            font-size: 0.8rem;
        }

        /* Verification Panel */
        .details-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        @media (max-width: 850px) {
            .details-grid {
                grid-template-columns: 1fr;
            }
        }

        .panel {
            background: var(--bg-card);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 1.5rem;
        }

        .panel-heading {
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #f1f5f9;
        }

        .db-status-box {
            background: rgba(2, 6, 23, 0.6);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
        }

        .db-info h4 {
            font-size: 1rem;
            font-weight: 700;
            color: #f8fafc;
        }

        .db-info p {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
        }

        .btn-ping {
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: #ffffff;
            border: none;
            padding: 0.6rem 1.1rem;
            border-radius: 8px;
            font-family: inherit;
            font-size: 0.85rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3);
        }

        .btn-ping:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45);
        }

        .btn-ping:active {
            transform: translateY(1px);
        }

        .info-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }

        .info-table td {
            padding: 0.6rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .info-table td:first-child {
            color: var(--text-muted);
            font-weight: 500;
        }

        .info-table td:last-child {
            text-align: right;
            font-weight: 600;
            color: #f1f5f9;
        }

        footer {
            margin-top: auto;
            text-align: center;
            font-size: 0.8rem;
            color: var(--text-muted);
            padding-top: 2rem;
            border-top: 1px solid var(--border-subtle);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <div class="brand-block">
                <div class="brand-logo">
                    <svg viewBox="0 0 24 24"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM19 18H6c-2.21 0-4-1.79-4-4 0-2.05 1.53-3.76 3.56-3.97l1.07-.11.5-.95C8.08 7.14 9.94 6 12 6c2.62 0 4.88 1.86 5.39 4.43l.3 1.5 1.53.11c1.56.1 2.78 1.41 2.78 2.96 0 1.65-1.35 3-3 3z"/></svg>
                </div>
                <div class="brand-text">
                    <h1>CloudNova Technologies</h1>
                    <p>Enterprise Cloud Operations Portal</p>
                </div>
            </div>
            <div class="badge-live">
                <span class="pulse-dot"></span>
                <span>SYSTEM OPERATIONAL</span>
            </div>
        </header>

        <!-- Hero -->
        <div class="hero-banner">
            <div class="hero-title">CCM101 Final Requirement: The Enterprise Cloud Architect</div>
            <div class="hero-subtitle">
                Production-grade multi-tier containerized cloud infrastructure deployed on Ubuntu Server 24.04 LTS with automated disaster recovery, perimeter security hardening, and persistent state management.
            </div>
        </div>

        <!-- Architecture Tiers -->
        <div class="arch-flow">
            <!-- Tier 1: Nginx -->
            <div class="arch-card">
                <div class="tier-label">Tier 1: Reverse Proxy</div>
                <div class="card-name">
                    <span>Nginx Alpine</span>
                    <span class="status-pill">ACTIVE</span>
                </div>
                <ul class="meta-list">
                    <li><span>Host Port:</span> <span class="mono">8088 / HTTP</span></li>
                    <li><span>Container Port:</span> <span class="mono">80 / TCP</span></li>
                    <li><span>Security:</span> <span>Public Ingress</span></li>
                </ul>
            </div>

            <!-- Tier 2: Flask -->
            <div class="arch-card">
                <div class="tier-label">Tier 2: Application Tier</div>
                <div class="card-name">
                    <span>Flask / Gunicorn</span>
                    <span class="status-pill">HEALTHY</span>
                </div>
                <ul class="meta-list">
                    <li><span>Internal Port:</span> <span class="mono">5000 / TCP</span></li>
                    <li><span>Workers:</span> <span class="mono">2 Gunicorn</span></li>
                    <li><span>Network:</span> <span class="mono">frontend, backend</span></li>
                </ul>
            </div>

            <!-- Tier 3: PostgreSQL -->
            <div class="arch-card">
                <div class="tier-label">Tier 3: Database Tier</div>
                <div class="card-name">
                    <span>PostgreSQL 16</span>
                    <span class="status-pill" style="color: #38bdf8; border-color: rgba(56, 189, 248, 0.4); background: rgba(56, 189, 248, 0.1);">ISOLATED</span>
                </div>
                <ul class="meta-list">
                    <li><span>Internal Port:</span> <span class="mono">5432 / TCP</span></li>
                    <li><span>Host Access:</span> <span style="color: #f87171; font-weight:700;">BLOCKED (UFW)</span></li>
                    <li><span>Network:</span> <span class="mono">backend (internal)</span></li>
                </ul>
            </div>

            <!-- Tier 4: Storage -->
            <div class="arch-card">
                <div class="tier-label">Storage & Automation</div>
                <div class="card-name">
                    <span>Volume & Cron</span>
                    <span class="status-pill">PERSISTENT</span>
                </div>
                <ul class="meta-list">
                    <li><span>Volume:</span> <span class="mono">postgres_data</span></li>
                    <li><span>Backup:</span> <span class="mono">Daily 02:00 AM</span></li>
                    <li><span>Retention:</span> <span>7 Days (Auto-Rotate)</span></li>
                </ul>
            </div>
        </div>

        <!-- Verification Panels -->
        <div class="details-grid">
            <!-- Left: Interactive Database Status -->
            <div class="panel">
                <div class="panel-heading">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C6.48 2 2 4.02 2 6.5s4.48 4.5 10 4.5 10-2.02 10-4.5S17.52 2 12 2zm0 7c-4.42 0-8-1.57-8-3.5S7.58 2 12 2s8 1.57 8 3.5S16.42 9 12 9zm0 2c-5.52 0-10 2.02-10 4.5s4.48 4.5 10 4.5 10-2.02 10-4.5S17.52 11 12 11zm0 7c-4.42 0-8-1.57-8-3.5s3.58-3.5 8-3.5 8 1.57 8 3.5-3.58 3.5-8 3.5zm0 2c-5.52 0-10 2.02-10 4.5s4.48 4.5 10 4.5 10-2.02 10-4.5S17.52 20 12 20z"/></svg>
                    <span>Live Database Telemetry</span>
                </div>
                <div class="db-status-box">
                    <div class="db-info">
                        <h4>PostgreSQL 16 Connection Status</h4>
                        <p id="ping-text">State: <strong style="color: #34d399;">Connected & Healthy</strong></p>
                    </div>
                    <button class="btn-ping" onclick="pingDatabase()">Ping Database</button>
                </div>
                <table class="info-table">
                    <tr>
                        <td>Container Hostname</td>
                        <td class="mono">{{ server_hostname }}</td>
                    </tr>
                    <tr>
                        <td>Database Engine</td>
                        <td class="mono">PostgreSQL 16 Alpine</td>
                    </tr>
                    <tr>
                        <td>Target Database</td>
                        <td class="mono">{{ db_name }}</td>
                    </tr>
                    <tr>
                        <td>Persistent Volume</td>
                        <td class="mono">enterprise-cloud_postgres_data</td>
                    </tr>
                    <tr>
                        <td>Last Telemetry Check</td>
                        <td class="mono" id="check-time">{{ check_time }}</td>
                    </tr>
                </table>
            </div>

            <!-- Right: Student & Environment Metadata -->
            <div class="panel">
                <div class="panel-heading">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                    <span>Architect Information</span>
                </div>
                <table class="info-table">
                    <tr>
                        <td>Architect</td>
                        <td>Carlo Nimer</td>
                    </tr>
                    <tr>
                        <td>Section</td>
                        <td>BSIT - 4J</td>
                    </tr>
                    <tr>
                        <td>Course</td>
                        <td>CCM101 - Cloud Computing</td>
                    </tr>
                    <tr>
                        <td>Instructor</td>
                        <td>Jenkielyn C. Torres</td>
                    </tr>
                    <tr>
                        <td>Institution</td>
                        <td>Univ. of Eastern Pangasinan</td>
                    </tr>
                    <tr>
                        <td>Hypervisor</td>
                        <td>Oracle VirtualBox 7.x</td>
                    </tr>
                    <tr>
                        <td>Host VM OS</td>
                        <td>Ubuntu Server 24.04 LTS</td>
                    </tr>
                    <tr>
                        <td>Firewall Policy</td>
                        <td>UFW Default Deny</td>
                    </tr>
                </table>
            </div>
        </div>

        <!-- Footer -->
        <footer>
            CloudNova Technologies &copy; 2026. Enterprise Cloud Infrastructure Final Requirement — BSIT - 4J.
        </footer>
    </div>

    <script>
        function pingDatabase() {
            const btn = document.querySelector('.btn-ping');
            const statusText = document.getElementById('ping-text');
            const checkTime = document.getElementById('check-time');
            btn.textContent = 'Pinging...';
            btn.disabled = true;

            fetch('/health')
                .then(res => res.json())
                .then(data => {
                    const now = new Date().toLocaleTimeString();
                    statusText.innerHTML = `State: <strong style="color: #34d399;">${data.database.toUpperCase()} & ${data.status.toUpperCase()}</strong>`;
                    checkTime.textContent = now;
                    btn.textContent = 'Ping Success!';
                    setTimeout(() => {
                        btn.textContent = 'Ping Database';
                        btn.disabled = false;
                    }, 1200);
                })
                .catch(err => {
                    statusText.innerHTML = `State: <strong style="color: #f87171;">ERROR: ${err.message}</strong>`;
                    btn.textContent = 'Retry';
                    btn.disabled = false;
                });
        }
    </script>
</body>
</html>
"""

def check_database():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        dbname=os.environ.get("DB_NAME", "cloudapp"),
        user=os.environ.get("DB_USER", "clouduser"),
        password=os.environ.get("DB_PASSWORD", "CloudNovaSecurePass2026!"),
        connect_timeout=3
    )
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            return cur.fetchone()[0] == 1
    finally:
        conn.close()

@app.route("/")
def home():
    connected = False
    try:
        connected = check_database()
    except Exception:
        connected = False

    # Return pure JSON for API clients / curl requests
    accept = request.headers.get("Accept", "")
    if "application/json" in accept or request.args.get("format") == "json":
        return jsonify({
            "project": "Enterprise Cloud Infrastructure",
            "application": "Flask",
            "server": socket.gethostname(),
            "database": "connected" if connected else "unavailable"
        }), 200 if connected else 503

    # Render modern visual dashboard for web browsers
    return render_template_string(
        HTML_TEMPLATE,
        server_hostname=socket.gethostname(),
        db_name=os.environ.get("DB_NAME", "cloudapp"),
        check_time=datetime.now().strftime("%H:%M:%S UTC"),
        is_connected=connected
    ), 200 if connected else 503

@app.route("/health")
def health():
    try:
        check_database()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception:
        return jsonify({"status": "unhealthy", "database": "unavailable"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
