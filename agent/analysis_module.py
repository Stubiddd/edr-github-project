import json
from datetime import datetime, timedelta

def load_events(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_events(events):
    alerts = []
    
    # Rule 1: Failed Login Attempts (Event ID: 4625)
    # Cảnh báo nếu có hơn 5 lần đăng nhập thất bại từ cùng một nguồn trong 5 phút
    failed_logins = {}
    for event in events:
        if event["EventID"] == 4625:
            source_ip = event["Strings"][2] if len(event["Strings"]) > 2 else "Unknown"
            timestamp = datetime.strptime(event["TimeGenerated"], "%Y-%m-%d %H:%M:%S")
            
            if source_ip not in failed_logins:
                failed_logins[source_ip] = []
            failed_logins[source_ip].append(timestamp)

            # Kiểm tra trong 5 phút gần nhất
            recent_attempts = [t for t in failed_logins[source_ip] if timestamp - t <= timedelta(minutes=5)]
            if len(recent_attempts) > 5:
                alerts.append({
                    "AlertID": f"FAILED_LOGIN_ATTEMPTS_{source_ip}_{timestamp.strftime('%Y%m%d%H%M%S')}",
                    "EventType": "Failed Login Attempts",
                    "Severity": "High",
                    "Description": f"Phát hiện hơn 5 lần đăng nhập thất bại từ IP {source_ip} trong 5 phút.",
                    "Timestamp": str(timestamp),
                    "RelatedEvents": [event]
                })
                # Xóa các lần thử cũ để tránh cảnh báo lặp lại
                failed_logins[source_ip] = [t for t in failed_logins[source_ip] if timestamp - t <= timedelta(minutes=5)]

    # Rule 2: New User Creation (Event ID: 4720)
    # Cảnh báo ngay lập tức khi có người dùng mới được tạo
    for event in events:
        if event["EventID"] == 4720:
            new_username = event["Strings"][1] if len(event["Strings"]) > 1 else "Unknown"
            alerts.append({
                "AlertID": f"NEW_USER_CREATION_{new_username}_{event['TimeGenerated'].replace(' ', '_')}",
                "EventType": "New User Creation",
                "Severity": "Medium",
                "Description": f"Người dùng mới \"{new_username}\" đã được tạo.",
                "Timestamp": event["TimeGenerated"],
                "RelatedEvents": [event]
            })

    # Rule 3: Privileged Account Usage (Event ID: 4672)
    # Cảnh báo khi tài khoản đặc quyền được sử dụng
    for event in events:
        if event["EventID"] == 4672:
            account_name = event["Strings"][1] if len(event["Strings"]) > 1 else "Unknown"
            alerts.append({
                "AlertID": f"PRIVILEGED_ACCOUNT_USAGE_{account_name}_{event['TimeGenerated'].replace(' ', '_')}",
                "EventType": "Privileged Account Usage",
                "Severity": "Low",
                "Description": f"Tài khoản đặc quyền \"{account_name}\" đã được sử dụng.",
                "Timestamp": event["TimeGenerated"],
                "RelatedEvents": [event]
            })

    # Rule 4: Suspicious Process Execution (Event ID: 4688) - Example for script execution
    # Cảnh báo nếu một tiến trình đáng ngờ được thực thi (ví dụ: script.bat)
    for event in events:
        if event["EventID"] == 4688:
            process_name = event["Strings"][0] if len(event["Strings"]) > 0 else "Unknown"
            command_line = event["Strings"][1] if len(event["Strings"]) > 1 else "Unknown"
            if "script.bat" in command_line.lower() or ("powershell.exe" in command_line.lower() and "-encodedcommand" in command_line.lower()):
                alerts.append({
                    "AlertID": f"SUSPICIOUS_PROCESS_EXECUTION_{process_name}_{event['TimeGenerated'].replace(' ', '_')}",
                    "EventType": "Suspicious Process Execution",
                    "Severity": "High",
                    "Description": f"Tiến trình đáng ngờ \"{process_name}\" với dòng lệnh \"{command_line}\" đã được thực thi.",
                    "Timestamp": event["TimeGenerated"],
                    "RelatedEvents": [event]
                })

    return alerts

def save_alerts(alerts, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(alerts, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    events_file = "security_events.json"
    alerts_file = "security_alerts.json"

    events = load_events(events_file)
    alerts = analyze_events(events)
    save_alerts(alerts, alerts_file)

    print(f"Đã phân tích {len(events)} sự kiện và tạo {len(alerts)} cảnh báo.")
    print(f"Cảnh báo đã được lưu vào {alerts_file}")


