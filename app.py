from flask import Flask, render_template, redirect
from modules.database import (
    create_database,
    get_logs,
    get_alerts,
    get_statistics,
    clear_database,block_ip,
    create_blocked_ip_table,
    get_blocked_ips,unblock_ip
)
from modules.generate_logs import (
    generate_normal_logs,
    generate_bruteforce_logs,
    generate_portscan_logs,
    generate_suspicious_logs
)
from modules.detector import run_detection
from modules.alert_manager import save_all_alerts
import os
os.makedirs("logs", exist_ok=True)
os.makedirs("database", exist_ok=True)

app = Flask(__name__)
# Initialize Database
create_database()
create_blocked_ip_table()
# Dashboard
# ==========================
@app.route("/")
def dashboard():

    blocked_ips = get_blocked_ips()

    stats = get_statistics()
    logs = get_logs()[:10]
    alerts = get_alerts()[:10]

    soc_status = "SECURE"
    status_color = "success"

    for alert in alerts:

        attack = alert[2]

        if attack in ["Brute Force", "PowerShell", "Netcat"]:
            soc_status = "UNDER ATTACK"
            status_color = "danger"
            break

        elif attack == "Port Scan":
            soc_status = "SUSPICIOUS"
            status_color = "warning"

    return render_template(
        "dashboard.html",
        stats=stats,
        logs=logs,
        alerts=alerts,
        blocked_ips=blocked_ips,
        soc_status=soc_status,
        status_color=status_color
    )
# Generate Normal Logs
# ==========================
@app.route("/generate/normal")
def generate_normal():
    generate_normal_logs()
    alerts = run_detection()
    save_all_alerts(alerts)
    return redirect("/")
# Generate Brute Force
# ==========================
@app.route("/generate/bruteforce")
def generate_bruteforce():
    generate_bruteforce_logs()
    alerts = run_detection()
    save_all_alerts(alerts)
    return redirect("/")
# Generate Port Scan
# ==========================
@app.route("/generate/portscan")
def generate_portscan():
    generate_portscan_logs()
    alerts = run_detection()
    save_all_alerts(alerts)
    return redirect("/")
# Generate Suspicious Commands
# ==========================
@app.route("/generate/suspicious")
def generate_suspicious():
    generate_suspicious_logs()
    alerts = run_detection()
    save_all_alerts(alerts)
    return redirect("/")
# Clear Database
# ==========================
@app.route("/clear")
def clear():
    clear_database()
    return redirect("/")
# ==========================
@app.route("/block/<ip>")
def block(ip):
    block_ip(ip)
    return redirect("/")
#to unblock ip
@app.route("/unblock/<ip>")
def unblock(ip):

    unblock_ip(ip)

    return redirect("/")
# Run App
# ==========================
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)