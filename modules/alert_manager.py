"""
MiniSIEM Alert Manager
Responsible for storing detected alerts
into the SQLite database.
"""
from datetime import datetime
from modules.database import insert_alert
def save_alert(alert):
    """
    Save a single alert into database.
    """
    recommendation = "\n".join(alert["recommendation"])
    insert_alert(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        attack_type=alert["attack_type"],
        source_ip=alert["source_ip"],
        severity=alert["severity"],
        recommendation=recommendation,
        status="OPEN"
    )
def save_all_alerts(alerts):
    """
    Save all detected alerts.
    """
    for alert in alerts:
        save_alert(alert)
    print(f"✅ {len(alerts)} alert(s) saved successfully.")
if __name__ == "__main__":
    sample_alert = {
        "attack_type": "Brute Force",
        "source_ip": "192.168.1.250",
        "severity": "HIGH",
        "recommendation": [
            "Block Source IP",
            "Enable MFA"
        ]
    }
    save_alert(sample_alert)
    print("Test Alert Saved.")