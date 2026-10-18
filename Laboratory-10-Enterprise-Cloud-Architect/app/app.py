import os
import socket
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def check_database():
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
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
    try:
        connected = check_database()
        return jsonify({
            "project": "Enterprise Cloud Infrastructure",
            "application": "Flask",
            "server": socket.gethostname(),
            "database": "connected" if connected else "unavailable"
        }), 200 if connected else 503
    except Exception:
        return jsonify({"database": "unavailable"}), 503

@app.route("/health")
def health():
    try:
        check_database()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception:
        return jsonify({"status": "unhealthy", "database": "unavailable"}), 503
