import os
import socket
import time
from datetime import datetime
import psycopg2
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        dbname=os.environ.get("DB_NAME", "cloudapp"),
        user=os.environ.get("DB_USER", "clouduser"),
        password=os.environ.get("DB_PASSWORD", "CloudNovaSecurePass2026!"),
        connect_timeout=3
    )

def init_db():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS enterprise_workloads (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    tier VARCHAR(60) NOT NULL,
                    region VARCHAR(60) NOT NULL,
                    ram VARCHAR(20) NOT NULL,
                    status VARCHAR(30) DEFAULT 'ONLINE',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cur.execute("SELECT COUNT(*) FROM enterprise_workloads;")
            count = cur.fetchone()[0]
            if count == 0:
                initial_nodes = [
                    ('core-banking-gateway', 'High-Throughput Edge Proxy', 'ap-southeast-manila', '16 GB', 'ONLINE'),
                    ('analytics-pipeline-db', 'Dedicated PostgreSQL Cluster', 'ap-southeast-manila', '32 GB', 'ONLINE'),
                    ('neural-inference-node', 'Sovereign AI Compute Cluster', 'us-east-virginia', '64 GB', 'ONLINE')
                ]
                for node in initial_nodes:
                    cur.execute(
                        "INSERT INTO enterprise_workloads (name, tier, region, ram, status) VALUES (%s, %s, %s, %s, %s);",
                        node
                    )
            conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database init notice: {e}")

# Attempt database initialization on startup
try:
    init_db()
except Exception:
    pass

def check_database():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            return cur.fetchone()[0] == 1
    finally:
        conn.close()

def get_workloads():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, tier, region, ram, status, to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') FROM enterprise_workloads ORDER BY id DESC LIMIT 15;")
            rows = cur.fetchall()
        conn.close()
        return rows
    except Exception:
        return []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudNova Technologies — Enterprise Cloud Infrastructure</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #060913;
            --bg-surface: #0b1120;
            --bg-card: rgba(15, 23, 42, 0.72);
            --bg-card-hover: rgba(26, 38, 66, 0.85);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-accent: rgba(56, 189, 248, 0.28);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --cyan: #38bdf8;
            --blue: #2563eb;
            --purple: #8b5cf6;
            --emerald: #10b981;
            --emerald-glow: rgba(16, 185, 129, 0.2);
            --amber: #f59e0b;
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
                radial-gradient(circle at 10% 0%, rgba(56, 189, 248, 0.12) 0px, transparent 45%),
                radial-gradient(circle at 90% 10%, rgba(139, 92, 246, 0.14) 0px, transparent 45%),
                radial-gradient(circle at 50% 90%, rgba(16, 185, 129, 0.08) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* Top Navigation */
        nav {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(6, 9, 19, 0.82);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-subtle);
            padding: 1rem 2rem;
        }

        .nav-inner {
            max-width: 1280px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
            color: var(--text-main);
        }

        .brand-logo {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--cyan), var(--purple));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.35);
        }

        .brand-name {
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .brand-name span {
            background: linear-gradient(90deg, #38bdf8, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: 2rem;
            list-style: none;
        }

        .nav-links a {
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 600;
            transition: color 0.2s;
        }

        .nav-links a:hover {
            color: var(--cyan);
        }

        .nav-cta {
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 0.55rem 1.25rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
        }

        .nav-cta:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.55);
        }

        /* Container */
        .container {
            max-width: 1280px;
            margin: 0 auto;
            padding: 2.5rem 1.5rem;
            width: 100%;
            flex: 1;
        }

        /* Hero */
        .hero {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 2.5rem;
            align-items: center;
            margin-bottom: 3rem;
            padding: 2rem 0;
        }

        .badge-live {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #34d399;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            margin-bottom: 1.25rem;
        }

        .pulse-dot {
            width: 7px;
            height: 7px;
            background-color: var(--emerald);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--emerald);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.7; }
            50% { transform: scale(1.3); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.7; }
        }

        .hero h1 {
            font-size: 3rem;
            font-weight: 800;
            line-height: 1.15;
            letter-spacing: -0.03em;
            margin-bottom: 1.25rem;
        }

        .hero h1 .highlight {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-desc {
            font-size: 1.1rem;
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 2rem;
            max-width: 580px;
        }

        .hero-actions {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .btn-primary {
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: #fff;
            padding: 0.85rem 1.75rem;
            border-radius: 10px;
            font-weight: 700;
            font-size: 0.95rem;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            cursor: pointer;
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.4);
            transition: all 0.2s;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(37, 99, 235, 0.6);
        }

        .btn-secondary {
            background: rgba(15, 23, 42, 0.8);
            color: var(--text-main);
            padding: 0.85rem 1.75rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.95rem;
            text-decoration: none;
            border: 1px solid var(--border-subtle);
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-secondary:hover {
            background: rgba(30, 41, 59, 0.9);
            border-color: var(--border-accent);
        }

        /* Glass Cards */
        .glass-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 1.75rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        }

        /* Telemetry Widget */
        .telemetry-card {
            border: 1px solid var(--border-accent);
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.85), rgba(8, 14, 28, 0.95));
            box-shadow: 0 16px 40px rgba(2, 132, 199, 0.15);
        }

        .telemetry-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 1rem;
            margin-bottom: 1.25rem;
        }

        .telemetry-header h3 {
            font-size: 1rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .metric-box {
            background: rgba(2, 6, 23, 0.6);
            border: 1px solid var(--border-subtle);
            padding: 1rem;
            border-radius: 10px;
        }

        .metric-box .label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-dim);
            margin-bottom: 0.35rem;
        }

        .metric-box .val {
            font-size: 1.35rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            color: var(--cyan);
        }

        .metric-box .sub {
            font-size: 0.75rem;
            color: var(--emerald);
            margin-top: 0.2rem;
        }

        /* Ping Button inside Telemetry */
        .btn-ping-live {
            width: 100%;
            background: rgba(56, 189, 248, 0.1);
            color: var(--cyan);
            border: 1px solid var(--border-accent);
            padding: 0.75rem;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        .btn-ping-live:hover {
            background: rgba(56, 189, 248, 0.2);
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.3);
        }

        /* Region Ticker */
        .region-ticker {
            background: rgba(11, 17, 32, 0.7);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-bottom: 3rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1.5rem;
        }

        .ticker-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .ticker-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--emerald);
            box-shadow: 0 0 8px var(--emerald);
        }

        .ticker-label {
            font-size: 0.8rem;
            color: var(--text-dim);
            text-transform: uppercase;
            font-weight: 700;
        }

        .ticker-val {
            font-size: 0.9rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-main);
        }

        .ticker-latency {
            font-size: 0.8rem;
            color: var(--emerald);
            font-family: 'JetBrains Mono', monospace;
        }

        /* Section Headings */
        .section-header {
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }

        .section-title {
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .section-subtitle {
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }

        /* Two Column Layout */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1.6fr;
            gap: 2rem;
            margin-bottom: 3rem;
        }

        @media (max-width: 968px) {
            .hero { grid-template-columns: 1fr; }
            .grid-2 { grid-template-columns: 1fr; }
            .nav-links { display: none; }
        }

        /* Provisioning Form */
        .form-group {
            margin-bottom: 1.15rem;
        }

        .form-group label {
            display: block;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 0.45rem;
        }

        .form-control {
            width: 100%;
            background: rgba(2, 6, 23, 0.7);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            color: var(--text-main);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            outline: none;
            transition: all 0.2s;
        }

        .form-control:focus {
            border-color: var(--cyan);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
        }

        select.form-control option {
            background-color: var(--bg-surface);
            color: var(--text-main);
        }

        .btn-submit {
            width: 100%;
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: white;
            border: none;
            padding: 0.85rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        .btn-submit:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 22px rgba(37, 99, 235, 0.6);
        }

        .form-hint {
            font-size: 0.75rem;
            color: var(--text-dim);
            margin-top: 0.75rem;
            text-align: center;
        }

        /* Workload Table */
        .table-responsive {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            text-align: left;
        }

        th {
            background: rgba(2, 6, 23, 0.8);
            color: var(--text-muted);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.9rem 1rem;
            border-bottom: 1px solid var(--border-subtle);
        }

        td {
            padding: 0.85rem 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
        }

        tr:hover td {
            background: rgba(255, 255, 255, 0.02);
        }

        .workload-name {
            color: #38bdf8;
            font-weight: 600;
        }

        .badge-status {
            display: inline-block;
            padding: 0.2rem 0.55rem;
            border-radius: 9999px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        /* Architecture Grid */
        .arch-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }

        .tier-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.2s;
        }

        .tier-card:hover {
            border-color: var(--border-accent);
            transform: translateY(-2px);
        }

        .tier-num {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--cyan);
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }

        .tier-title {
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .tier-desc {
            font-size: 0.85rem;
            color: var(--text-muted);
            line-height: 1.5;
            margin-bottom: 1rem;
        }

        .tier-port {
            display: inline-block;
            background: rgba(2, 6, 23, 0.7);
            border: 1px solid var(--border-subtle);
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--emerald);
        }

        /* Footer */
        footer {
            border-top: 1px solid var(--border-subtle);
            background: rgba(6, 9, 19, 0.95);
            padding: 2.5rem 1.5rem;
            color: var(--text-dim);
            font-size: 0.85rem;
            text-align: center;
            margin-top: auto;
        }

        .footer-inner {
            max-width: 1280px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
    </style>
</head>
<body>

    <!-- Navigation -->
    <nav>
        <div class="nav-inner">
            <a href="/" class="brand">
                <div class="brand-logo">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M19.35 10.04C18.67 6.59 15.64 4 12 4C9.11 4 6.6 5.64 5.35 8.04C2.34 8.36 0 10.91 0 14C0 17.31 2.69 20 6 20H19C21.76 20 24 17.76 24 15C24 12.36 21.95 10.22 19.35 10.04Z" fill="url(#cloudGrad)"/>
                        <defs>
                            <linearGradient id="cloudGrad" x1="0" y1="4" x2="24" y2="20" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#ffffff"/>
                                <stop offset="1" stop-color="#bae6fd"/>
                            </linearGradient>
                        </defs>
                    </svg>
                </div>
                <div class="brand-name">Cloud<span>Nova</span> <small style="font-size: 0.65em; font-weight: 500; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; margin-left: 4px;">Enterprise</small></div>
            </a>
            <ul class="nav-links">
                <li><a href="#telemetry">Live Telemetry</a></li>
                <li><a href="#fleet">Fleet Provisioner</a></li>
                <li><a href="#topology">Zero-Trust Topology</a></li>
                <li><a href="/health" target="_blank">Health API</a></li>
            </ul>
            <button class="nav-cta" onclick="document.getElementById('fleet').scrollIntoView({behavior: 'smooth'})">Deploy Workload</button>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container">

        <!-- Hero Section -->
        <div class="hero">
            <div>
                <div class="badge-live">
                    <span class="pulse-dot"></span> Production Cluster Active
                </div>
                <h1>Mission-Critical <span class="highlight">Enterprise Cloud</span> Platform</h1>
                <p class="hero-desc">
                    Engineered for high-availability container orchestration, isolated zero-trust database topologies, and automated disaster recovery resilience.
                </p>
                <div class="hero-actions">
                    <button class="btn-primary" onclick="document.getElementById('fleet').scrollIntoView({behavior: 'smooth'})">
                        <span>Provision Workload</span> &rarr;
                    </button>
                    <button class="btn-secondary" onclick="document.getElementById('topology').scrollIntoView({behavior: 'smooth'})">
                        View Topology Specs
                    </button>
                </div>
            </div>

            <!-- Telemetry Glass Card -->
            <div class="glass-card telemetry-card" id="telemetry">
                <div class="telemetry-header">
                    <h3>⚡ Live Cluster Telemetry</h3>
                    <div class="status-pill">
                        <span class="pulse-dot"></span> <span id="db-status-pill">{{ 'CONNECTED' if is_connected else 'OFFLINE' }}</span>
                    </div>
                </div>

                <div class="metrics-grid">
                    <div class="metric-box">
                        <div class="label">Platform Uptime</div>
                        <div class="val">99.999%</div>
                        <div class="sub">High-Availability</div>
                    </div>
                    <div class="metric-box">
                        <div class="label">Database Cluster</div>
                        <div class="val" style="color: #34d399;">PostgreSQL 16</div>
                        <div class="sub">Internal Isolation</div>
                    </div>
                    <div class="metric-box">
                        <div class="label">Ingress Proxy</div>
                        <div class="val">Nginx:8088</div>
                        <div class="sub">Reverse Proxy</div>
                    </div>
                    <div class="metric-box">
                        <div class="label">Container Host</div>
                        <div class="val" style="font-size: 1.05rem; overflow: hidden; text-overflow: ellipsis;">{{ server_hostname }}</div>
                        <div class="sub">Docker Compose</div>
                    </div>
                </div>

                <button class="btn-ping-live" id="btn-ping" onclick="pingDatabase()">
                    <span>Pinging Database Engine...</span>
                </button>
                <div style="font-size: 0.75rem; color: var(--text-dim); text-align: center; margin-top: 0.6rem; font-family: 'JetBrains Mono', monospace;" id="ping-log">
                    Last Healthcheck: {{ check_time }}
                </div>
            </div>
        </div>

        <!-- Global Region Ticker -->
        <div class="region-ticker">
            <div class="ticker-item">
                <div class="ticker-dot"></div>
                <div>
                    <div class="ticker-label">Asia-Pacific (Manila)</div>
                    <div class="ticker-val">ap-southeast-1 <span class="ticker-latency">8ms</span></div>
                </div>
            </div>
            <div class="ticker-item">
                <div class="ticker-dot"></div>
                <div>
                    <div class="ticker-label">Asia-Pacific (Tokyo)</div>
                    <div class="ticker-val">ap-northeast-1 <span class="ticker-latency">34ms</span></div>
                </div>
            </div>
            <div class="ticker-item">
                <div class="ticker-dot"></div>
                <div>
                    <div class="ticker-label">Europe (Frankfurt)</div>
                    <div class="ticker-val">eu-central-1 <span class="ticker-latency">165ms</span></div>
                </div>
            </div>
            <div class="ticker-item">
                <div class="ticker-dot"></div>
                <div>
                    <div class="ticker-label">US-East (Virginia)</div>
                    <div class="ticker-val">us-east-1 <span class="ticker-latency">148ms</span></div>
                </div>
            </div>
        </div>

        <!-- Two Column: Provisioner & Live Workloads -->
        <div class="grid-2" id="fleet">
            
            <!-- Provisioning Form -->
            <div class="glass-card">
                <div style="margin-bottom: 1.25rem;">
                    <h3 style="font-size: 1.2rem; font-weight: 700;">Deploy Workload</h3>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.2rem;">Commit new instance to persistent database.</p>
                </div>

                <form id="provisionForm" onsubmit="handleProvision(event)">
                    <div class="form-group">
                        <label>Workload Name</label>
                        <input type="text" id="wName" class="form-control" placeholder="e.g. prod-api-cluster" required>
                    </div>

                    <div class="form-group">
                        <label>Architecture Tier</label>
                        <select id="wTier" class="form-control">
                            <option value="Dedicated PostgreSQL Cluster">Dedicated PostgreSQL Cluster</option>
                            <option value="High-Throughput Edge Proxy">High-Throughput Edge Proxy</option>
                            <option value="Sovereign AI Compute Cluster">Sovereign AI Compute Cluster</option>
                            <option value="Microservice Gateway">Microservice Gateway</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Target Region</label>
                        <select id="wRegion" class="form-control">
                            <option value="ap-southeast-manila">ap-southeast-manila</option>
                            <option value="ap-northeast-tokyo">ap-northeast-tokyo</option>
                            <option value="us-east-virginia">us-east-virginia</option>
                            <option value="eu-central-frankfurt">eu-central-frankfurt</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>RAM Allocation</label>
                        <select id="wRam" class="form-control">
                            <option value="8 GB">8 GB High-Speed RAM</option>
                            <option value="16 GB">16 GB Enterprise ECC</option>
                            <option value="32 GB">32 GB Dedicated Buffer</option>
                            <option value="64 GB">64 GB High-Compute</option>
                        </select>
                    </div>

                    <button type="submit" class="btn-submit" id="btn-submit-workload">
                        ⚡ Provision Enterprise Workload
                    </button>
                    <p class="form-hint">Writes directly to PostgreSQL on Docker backend network.</p>
                </form>
            </div>

            <!-- Live PostgreSQL Records Table -->
            <div class="glass-card">
                <div class="section-header" style="margin-bottom: 1rem;">
                    <div>
                        <h3 style="font-size: 1.2rem; font-weight: 700;">Live Fleet Workloads</h3>
                        <p class="section-subtitle">Active records stored in named Docker volume (enterprise-cloud_postgres_data).</p>
                    </div>
                    <button onclick="location.reload()" class="btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.8rem;">
                        &#x21bb; Refresh
                    </button>
                </div>

                <div class="table-responsive">
                    <table id="workloads-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Workload Name</th>
                                <th>Service Tier</th>
                                <th>Region</th>
                                <th>RAM</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody id="workload-rows">
                            {% for w in workloads %}
                            <tr>
                                <td style="color: var(--text-dim);">#{{ w[0] }}</td>
                                <td class="workload-name">{{ w[1] }}</td>
                                <td style="color: var(--text-muted); font-size: 0.8rem;">{{ w[2] }}</td>
                                <td>{{ w[3] }}</td>
                                <td>{{ w[4] }}</td>
                                <td><span class="badge-status">{{ w[5] }}</span></td>
                            </tr>
                            {% else %}
                            <tr>
                                <td colspan="6" style="text-align: center; color: var(--text-dim); padding: 2rem;">No workloads provisioned yet. Use the form to deploy.</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Zero-Trust Architecture Section -->
        <div id="topology">
            <div class="section-header">
                <div>
                    <h2 class="section-title">Zero-Trust Infrastructure Topology</h2>
                    <p class="section-subtitle">Engineered with defense-in-depth isolation and host firewall enforcement.</p>
                </div>
            </div>

            <div class="arch-grid">
                <div class="tier-card">
                    <div class="tier-num">Tier 1 &mdash; Perimeter Ingress</div>
                    <div class="tier-title">Nginx Reverse Proxy</div>
                    <div class="tier-desc">Handles incoming HTTP client requests. Terminates external network connections and balances traffic to backend containers.</div>
                    <div class="tier-port">Host: Port 8088 &rarr; Container: Port 80</div>
                </div>

                <div class="tier-card">
                    <div class="tier-num">Tier 2 &mdash; Application Engine</div>
                    <div class="tier-title">Flask / Gunicorn App</div>
                    <div class="tier-desc">Multi-worker application layer running inside dual-bridge networks. Connects frontend ingress to isolated database.</div>
                    <div class="tier-port">Internal: Port 5000 (Protected)</div>
                </div>

                <div class="tier-card">
                    <div class="tier-num">Tier 3 &mdash; Data Fortress</div>
                    <div class="tier-title">PostgreSQL 16 Cluster</div>
                    <div class="tier-desc">Strictly isolated inside backend bridge (internal: true). Zero direct route to outside internet; protected by persistent storage volume.</div>
                    <div class="tier-port">Internal: Port 5432 (Isolated)</div>
                </div>
            </div>
        </div>

    </div>

    <!-- Footer -->
    <footer>
        <div class="footer-inner">
            <div>
                <strong>CloudNova Technologies Inc.</strong> &copy; 2026. Enterprise Cloud Infrastructure Platform.
            </div>
            <div>
                Status: <span style="color: #34d399; font-weight: 700;">All Systems Operational</span> &bull; SLA: 99.999%
            </div>
        </div>
    </footer>

    <script>
        function pingDatabase() {
            const btn = document.getElementById('btn-ping');
            const pill = document.getElementById('db-status-pill');
            const log = document.getElementById('ping-log');
            btn.innerHTML = '<span>Pinging Database Engine...</span>';
            btn.disabled = true;

            const t0 = performance.now();
            fetch('/health')
                .then(res => res.json())
                .then(data => {
                    const elapsed = Math.round(performance.now() - t0);
                    pill.textContent = data.database.toUpperCase();
                    pill.style.color = '#34d399';
                    btn.innerHTML = `<span>&#10003; PostgreSQL Healthy (${elapsed}ms)</span>`;
                    log.textContent = `Last Healthcheck: ${new Date().toLocaleTimeString()} (HTTP 200 OK)`;
                    setTimeout(() => {
                        btn.innerHTML = '<span>Test PostgreSQL Ping</span>';
                        btn.disabled = false;
                    }, 1500);
                })
                .catch(err => {
                    pill.textContent = 'UNAVAILABLE';
                    pill.style.color = '#f87171';
                    btn.innerHTML = `<span>Error: ${err.message}</span>`;
                    setTimeout(() => {
                        btn.innerHTML = '<span>Retry Ping</span>';
                        btn.disabled = false;
                    }, 2000);
                });
        }

        // Run an initial ping on page load
        window.addEventListener('DOMContentLoaded', () => {
            pingDatabase();
        });

        function handleProvision(e) {
            e.preventDefault();
            const btn = document.getElementById('btn-submit-workload');
            const name = document.getElementById('wName').value.trim();
            const tier = document.getElementById('wTier').value;
            const region = document.getElementById('wRegion').value;
            const ram = document.getElementById('wRam').value;

            if (!name) return;

            btn.disabled = true;
            btn.innerHTML = '<span>Provisioning to PostgreSQL...</span>';

            fetch('/api/workloads', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, tier, region, ram })
            })
            .then(res => {
                if (!res.ok) throw new Error('Provisioning failed');
                return res.json();
            })
            .then(data => {
                btn.innerHTML = '<span>&#10003; Provisioned Successfully!</span>';
                document.getElementById('wName').value = '';
                setTimeout(() => {
                    location.reload();
                }, 700);
            })
            .catch(err => {
                alert('Database Error: ' + err.message);
                btn.disabled = false;
                btn.innerHTML = '<span>⚡ Provision Enterprise Workload</span>';
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    connected = False
    try:
        connected = check_database()
    except Exception:
        connected = False

    accept = request.headers.get("Accept", "")
    if "application/json" in accept or request.args.get("format") == "json":
        return jsonify({
            "project": "CloudNova Enterprise Cloud Platform",
            "application": "Flask",
            "server": socket.gethostname(),
            "database": "connected" if connected else "unavailable"
        }), 200 if connected else 503

    workloads = get_workloads()
    return render_template_string(
        HTML_TEMPLATE,
        server_hostname=socket.gethostname(),
        check_time=datetime.now().strftime("%H:%M:%S UTC"),
        is_connected=connected,
        workloads=workloads
    ), 200 if connected else 503

@app.route("/health")
def health():
    try:
        check_database()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception:
        return jsonify({"status": "unhealthy", "database": "unavailable"}), 503

@app.route("/api/workloads", methods=["GET", "POST"])
def api_workloads():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        name = data.get("name", "unnamed-workload").strip()
        tier = data.get("tier", "Dedicated PostgreSQL Cluster")
        region = data.get("region", "ap-southeast-manila")
        ram = data.get("ram", "16 GB")
        
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO enterprise_workloads (name, tier, region, ram, status) VALUES (%s, %s, %s, %s, 'ONLINE') RETURNING id;",
                    (name, tier, region, ram)
                )
                new_id = cur.fetchone()[0]
                conn.commit()
            conn.close()
            return jsonify({"status": "created", "id": new_id, "name": name}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    # GET
    rows = get_workloads()
    workload_list = [
        {"id": r[0], "name": r[1], "tier": r[2], "region": r[3], "ram": r[4], "status": r[5], "created_at": r[6]}
        for r in rows
    ]
    return jsonify({"workloads": workload_list}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
