# Các phương pháp thu thập Event ID trên Windows

## 1. Event Viewer
Event Viewer là công cụ tích hợp sẵn trong Windows cho phép người dùng xem và quản lý các nhật ký sự kiện. Các nhật ký này bao gồm thông tin về các sự kiện hệ thống, bảo mật, ứng dụng, v.v. Người dùng có thể lọc, tìm kiếm và xuất các sự kiện từ Event Viewer.

## 2. Windows Event Forwarding (WEF)
WEF cho phép chuyển tiếp các sự kiện từ nhiều máy tính đến một máy chủ tập trung. Điều này rất hữu ích cho việc thu thập nhật ký từ nhiều điểm cuối và phân tích chúng tại một nơi duy nhất. WEF có thể được cấu hình thông qua Group Policy hoặc bằng tay.

## 3. PowerShell
PowerShell cung cấp các cmdlet mạnh mẽ để truy cập và quản lý nhật ký sự kiện Windows. Các cmdlet như `Get-WinEvent` cho phép truy vấn, lọc và xuất các sự kiện theo nhiều tiêu chí khác nhau, bao gồm Event ID, nguồn, thời gian, v.v.

## 4. Công cụ dòng lệnh `wevtutil`
`wevtutil` là một công cụ dòng lệnh cho phép quản lý nhật ký sự kiện Windows. Nó có thể được sử dụng để truy vấn, xuất, xóa và cấu hình nhật ký sự kiện. Đây là một công cụ hữu ích cho việc tự động hóa các tác vụ liên quan đến nhật ký sự kiện.

## 5. Các giải pháp của bên thứ ba
Có nhiều giải pháp của bên thứ ba như NXLog, Winlogbeat, Splunk Universal Forwarder, v.v., được thiết kế để thu thập và chuyển tiếp nhật ký sự kiện Windows đến các hệ thống quản lý nhật ký tập trung (SIEM).

## 6. Microsoft Defender for Identity
Microsoft Defender for Identity (trước đây là Azure Advanced Threat Protection) dựa vào các nhật ký sự kiện cụ thể của Windows để phát hiện các mối đe dọa. Cảm biến của nó phân tích các nhật ký sự kiện này từ bộ điều khiển miền của bạn và các máy chủ khác.

## 7. Google Security Operations
Google Security Operations cung cấp tài liệu về cách thu thập dữ liệu sự kiện Microsoft Windows, bao gồm kiến trúc triển khai, các bước cài đặt và cấu hình cần thiết để tạo ra các nhật ký được hỗ trợ.

