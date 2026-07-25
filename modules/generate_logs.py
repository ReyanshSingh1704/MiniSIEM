import random
from datetime import datetime
from modules.database import insert_log
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "security.log")

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8"):
        pass

# -----------------------------
HOSTNAMES = [
    "WIN-01",
    "WIN-02",
    "SERVER-01"
]
USERS = [
    "Administrator","Atharv","Abhyuday","SOCUser","Guest","Reyansh"
]
NORMAL_EVENTS = [
    (4624, "Login Success", "INFO", "User logged in successfully"),
    (4634, "Logout", "INFO", "User logged out"),
    (6416, "USB Connected", "LOW", "USB device connected"),
]
SUSPICIOUS_COMMANDS = [
    (4104, "PowerShell", "HIGH", "PowerShell command executed"),
    (9002, "Netcat", "CRITICAL", "Netcat executed"),
]
# Common Log Writer
# -----------------------------
def write_log(timestamp, hostname, username, ip,
              event_id, event_type, severity, message):
    line = (
        f"{timestamp} | "
        f"{hostname} | "
        f"{username} | "
        f"{ip} | "
        f"{event_id} | "
        f"{event_type} | "
        f"{severity} | "
        f"{message}"
    )
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(line + "\n")
    insert_log(
        timestamp,
        hostname,
        username,
        ip,
        event_id,
        event_type,
        severity,
        message
    )
# Generate Normal Logs
# -----------------------------
def generate_normal_logs(count=10):
    for _ in range(count):
        write_log(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            random.choice(HOSTNAMES),
            random.choice(USERS),
            f"192.168.1.{random.randint(2,200)}",
            *random.choice(NORMAL_EVENTS)
        )
    print(f"✅ {count} Normal Logs Generated")
# Brute Force Simulation
# -----------------------------
def generate_bruteforce_logs():
    attacker_ip = "192.168.1.250"
    for _ in range(5):
        write_log(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "WIN-01",
            "Administrator",
            attacker_ip,
            4625,
            "Failed Login",
            "HIGH",
            "Failed login attempt"
        )
    print("🚨 Brute Force Logs Generated")
# Port Scan Simulation
# -----------------------------
def generate_portscan_logs():
    attacker_ip = "10.10.10.10"
    ports = [21, 22, 23, 80, 443, 8080]
    for port in ports:
        write_log(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "SERVER-01",
            "Unknown",
            attacker_ip,
            9001,
            "Port Scan",
            "MEDIUM",
            f"Port {port} scanned"
        )
    print("🚨 Port Scan Logs Generated")
# Suspicious Command Simulation
# -----------------------------
def generate_suspicious_logs():
    ip = "172.16.0.50"
    for event in SUSPICIOUS_COMMANDS:
        write_log(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "WIN-02",
            "Administrator",
            ip,
            *event
        )
    print("🚨 Suspicious Command Logs Generated")
# Main Menu
# -----------------------------
if __name__ == "__main__":
    print("\n========== MiniSIEM Log Generator ==========")
    print("1. Generate Normal Logs")
    print("2. Simulate Brute Force")
    print("3. Simulate Port Scan")
    print("4. Simulate Suspicious Commands")
    choice = input("\nEnter Choice: ")
    if choice == "1":
        generate_normal_logs()
    elif choice == "2":
        generate_bruteforce_logs()
    elif choice == "3":
        generate_portscan_logs()
    elif choice == "4":
        generate_suspicious_logs()
    else:
        print("Invalid Choice")