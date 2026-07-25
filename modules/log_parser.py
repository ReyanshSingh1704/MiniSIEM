def parse_logs():
    parsed_logs = []
    with open("logs/security.log", "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 8:
                continue
            log = {
                "timestamp": parts[0].strip(),
                "hostname": parts[1].strip(),
                "username": parts[2].strip(),
                "source_ip": parts[3].strip(),
                "event_id": int(parts[4].strip()),
                "event_type": parts[5].strip(),
                "severity": parts[6].strip(),
                "message": parts[7].strip()
            }
            parsed_logs.append(log)
    return parsed_logs
if __name__ == "__main__":
    logs = parse_logs()
    for log in logs[:5]:
        print(log)