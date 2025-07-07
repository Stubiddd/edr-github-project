import win32evtlog
import json

def get_event_logs(log_type='Security', event_ids=None):
    """
    Thu thập các sự kiện từ Windows Event Log.

    Args:
        log_type (str): Loại nhật ký (ví dụ: 'Security', 'System', 'Application').
        event_ids (list): Danh sách các Event ID cần thu thập. Nếu None, thu thập tất cả.

    Returns:
        list: Danh sách các sự kiện đã thu thập dưới dạng dictionary.
    """
    events = []
    try:
        hand = win32evtlog.OpenEventLog(None, log_type)
        total_events = win32evtlog.GetNumberOfEventLogRecords(hand)
        print(f"Đang thu thập {total_events} sự kiện từ nhật ký {log_type}...")

        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        offset = 0
        while True:
            # Đọc 100 sự kiện mỗi lần
            objects = win32evtlog.ReadEventLog(hand, flags, offset, 100)
            if not objects:
                break
            for event in objects:
                event_data = {
                    'EventID': event.EventID,
                    'SourceName': event.SourceName,
                    'TimeGenerated': str(event.TimeGenerated),
                    'ComputerName': event.ComputerName,
                    'EventType': event.EventType,
                    'Category': event.EventCategory,
                    'Strings': event.StringInserts
                }
                if event_ids is None or event.EventID in event_ids:
                    events.append(event_data)
            offset += len(objects)

    except Exception as e:
        print(f"Lỗi khi đọc nhật ký sự kiện: {e}")
    finally:
        if 'hand' in locals() and hand:
            win32evtlog.CloseEventLog(hand)
    return events


if __name__ == "__main__":
    # Danh sách 50 Event ID quan trọng (ví dụ, cần cập nhật đầy đủ)
    important_event_ids = [
        4625, 4740, 4624, 4720, 4672, 4722, 4723, 4724, 4725, 4726,
        4723, 4724, 4727, 4731, 4735, 4737, 4624, 4725, 4624, 4624,
        4672, 4624, 4648, 4663, 5140, 5145, 4657, 11707, 1033, 20001,
        20003, 4946, 4947, 4950, 4951, 4698, 4688, 6005, 6006, 1074,
        1102, 4688, 1116, 5136, 5141, 524, 4254, 4255, 10400, 4688,
        4697, 1102, 865, 4625, 4776, 4663, 4688, 7045, 4699, 5136,
        4104, 5156, 5145, 5158, 4662, 4689, 7041, 4719, 1102, 4616,
        520, 5379
    ]

    security_events = get_event_logs(log_type='Security', event_ids=important_event_ids)
    print(f"Đã thu thập {len(security_events)} sự kiện bảo mật.")
    with open('security_events.json', 'w', encoding='utf-8') as f:
        json.dump(security_events, f, ensure_ascii=False, indent=4)
    print("Đã lưu sự kiện bảo mật vào security_events.json")

    # Ví dụ thu thập thêm System events
    # system_events = get_event_logs(log_type='System')
    # print(f"Đã thu thập {len(system_events)} sự kiện hệ thống.")
    # with open('system_events.json', 'w', encoding='utf-8') as f:
    #     json.dump(system_events, f, ensure_ascii=False, indent=4)
    # print("Đã lưu sự kiện hệ thống vào system_events.json")


