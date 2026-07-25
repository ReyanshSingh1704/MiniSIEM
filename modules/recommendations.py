"""
MiniSIEM Recommendation Engine
This module provides recommended actions
for detected security threats.
"""
def get_recommendation(attack_type):
    """
    Returns a recommended response
    based on the detected attack type.
    """
    recommendations = {

        "Brute Force": [
            "Block the source IP",
            "Reset the affected user's password",
            "Enable Multi-Factor Authentication (MFA)",
            "Review failed login attempts",
            "Monitor the account for suspicious activity"
        ],
        "Port Scan": [
            "Block the scanning IP address",
            "Review firewall rules",
            "Close unused ports",
            "Monitor for further reconnaissance activity"
        ],
        "PowerShell": [
            "Verify if the PowerShell execution was authorized",
            "Review executed PowerShell commands",
            "Scan the host for malware",
            "Restrict PowerShell execution policy if necessary"
        ],
        "Netcat": [
            "Isolate the affected machine immediately",
            "Terminate the suspicious process",
            "Scan the system for malware",
            "Investigate possible reverse shell activity"
        ]
    }
    return recommendations.get(
        attack_type,
        ["No recommendation available."]
    )
# --------------------------------------------------
# Test
if __name__ == "__main__":
    attacks = [
        "Brute Force",
        "Port Scan",
        "PowerShell",
        "Netcat"
    ]
    for attack in attacks:
        print(f"\n{attack}")
        for action in get_recommendation(attack):
            print(f" - {action}")