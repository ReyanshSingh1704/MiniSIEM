from collections import Counter
from modules.log_parser import parse_logs
from modules.recommendations import get_recommendation
from modules.alert_manager import save_all_alerts
# ==========================================
# Brute Force Detection
def detect_bruteforce(logs):
    failed_ips = []
    for log in logs:
        if log["event_type"] == "Failed Login":
            failed_ips.append(log["source_ip"])
    counter = Counter(failed_ips)
    alerts = []
    for ip, count in counter.items():
        if count >= 5:
            alerts.append({
                "attack_type": "Brute Force",
                "source_ip": ip,
                "severity": "HIGH",
                "recommendation": get_recommendation("Brute Force")
            })
    return alerts
# ==========================================
# Port Scan Detection
def detect_portscan(logs):
    scan_ips = []
    for log in logs:
        if log["event_type"] == "Port Scan":
            scan_ips.append(log["source_ip"])
    counter = Counter(scan_ips)
    alerts = []
    for ip, count in counter.items():
        if count >= 5:
            alerts.append({
                "attack_type": "Port Scan",
                "source_ip": ip,
                "severity": "MEDIUM",
                "recommendation": get_recommendation("Port Scan")
            })
    return alerts
# ==========================================
# PowerShell Detection
def detect_powershell(logs):
    alerts = []
    seen_ips = set()
    for log in logs:
        if log["event_id"] == 4104:
            if log["source_ip"] not in seen_ips:
                alerts.append({
                "attack_type": "PowerShell",
                "source_ip": log["source_ip"],
                "severity": "HIGH",
                "recommendation": get_recommendation("PowerShell")
            })
            seen_ips.add(log["source_ip"])
    return alerts
# Netcat Detection
# ==========================================
def detect_netcat(logs):
    alerts = []
    for log in logs:
        if log["event_id"] == 9002:
            alerts.append({
                "attack_type": "Netcat",
                "source_ip": log["source_ip"],
                "severity": "CRITICAL",
                "recommendation": get_recommendation("Netcat")
            })
    return alerts
# Master Detection Function
# ==========================================
def run_detection():
    logs = parse_logs()
    alerts = []
    alerts.extend(detect_bruteforce(logs))
    alerts.extend(detect_portscan(logs))
    alerts.extend(detect_powershell(logs))
    alerts.extend(detect_netcat(logs))
    return alerts
# Testing
# ==========================================
if __name__ == "__main__":
    alerts = run_detection()
    print("\n========== DETECTED ALERTS ==========\n")
    if not alerts:
        print("No threats detected.")
    else:
        save_all_alerts(alerts)
        for alert in alerts:
            print("--------------------------------")
            print("Attack :", alert["attack_type"])
            print("IP :", alert["source_ip"])
            print("Severity :", alert["severity"])
            print("Recommendations:")
            for action in alert["recommendation"]:
                print(" -", action)
            print("--------------------------------")