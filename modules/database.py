import sqlite3
import os
# Database Configuration
# =========================================================
DB_FOLDER = "database"
DB_NAME = os.path.join(DB_FOLDER, "siem.db")
# Database Connection
# =========================================================
def get_connection():
    """Return a SQLite database connection."""
    os.makedirs(DB_FOLDER, exist_ok=True)
    return sqlite3.connect(DB_NAME)
# Database Initialization
# =====================================================
def create_database():
    """Create required database tables."""
    conn = get_connection()
    cursor = conn.cursor()
    # Logs Table
    # ----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        hostname TEXT NOT NULL,
        username TEXT NOT NULL,
        source_ip TEXT NOT NULL,
        event_id INTEGER NOT NULL,
        event_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        message TEXT NOT NULL
    )
    """)
    #blocked_ips Table
    # ----------------------------  
    cursor.execute("""
CREATE TABLE IF NOT EXISTS blocked_ips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT UNIQUE,
    blocked_time TEXT
)
""")
    # Alerts Table
    # ----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        attack_type TEXT NOT NULL,
        source_ip TEXT NOT NULL,
        severity TEXT NOT NULL,
        recommendation TEXT NOT NULL,
        status TEXT DEFAULT 'OPEN'
    )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")
# Insert Log
# ==========================================================
def insert_log(timestamp,
               hostname,
               username,
               source_ip,
               event_id,
               event_type,
               severity,
               message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (
            timestamp,
            hostname,
            username,
            source_ip,
            event_id,
            event_type,
            severity,
            message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        hostname,
        username,
        source_ip,
        event_id,
        event_type,
        severity,
        message
    ))
    conn.commit()
    conn.close()
# Insert Alert
# ==========================================================
def insert_alert(timestamp,
                 attack_type,
                 source_ip,
                 severity,
                 recommendation,
                 status="OPEN"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alerts (
            timestamp,
            attack_type,
            source_ip,
            severity,
            recommendation,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        attack_type,
        source_ip,
        severity,
        recommendation,
        status
    ))
    conn.commit()
    conn.close()
# ==========================================================
# Fetch Logs
def get_logs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM logs
        ORDER BY id DESC
    """)
    logs = cursor.fetchall()
    conn.close()
    return logs
# =========================================================
# Fetch Alerts
def get_alerts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM alerts
        ORDER BY id DESC
    """)
    alerts = cursor.fetchall()
    conn.close()
    return alerts
#create block ip
def create_blocked_ip_table():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocked_ips(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT UNIQUE,
            blocked_time TEXT

        )
    """)

    conn.commit()
    conn.close()
from datetime import datetime

def block_ip(ip):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO blocked_ips(ip, blocked_time)
        VALUES (?,?)
    """, (ip, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
def get_blocked_ips():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM blocked_ips
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data
#unblock ip
def unblock_ip(ip):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM blocked_ips WHERE ip = ?",
        (ip,)
    )

    conn.commit()
    conn.close()
# Dashboard Statistics
# ==========================================================
def get_statistics():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM logs")
    total_logs = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM alerts")
    total_alerts = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity='CRITICAL'")
    critical = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity='HIGH'")
    high = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity='MEDIUM'")
    medium = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity='LOW'")
    low = cursor.fetchone()[0]
    conn.close()
    return {
        "total_logs": total_logs,
        "total_alerts": total_alerts,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low
    }
# Clear Data (Useful During Testing)
#==========================================================
def clear_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    cursor.execute("DELETE FROM alerts")
    conn.commit()
    conn.close()
    print("🗑 Database cleared.")
    # Clear log file
    with open("logs/security.log", "w") as file:
        file.write("")
#=======================================================
from datetime import datetime
def block_ip(ip):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO blocked_ips(
            ip,
            blocked_time
        )
        VALUES (?, ?)
    """, (
        ip,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()
# Run Directly
#==========================================================
if __name__ == "__main__":
    create_database()