# deploy_agent.ps1
# Script để triển khai EDR Agent trên hệ thống Windows

# --- Cấu hình --- 
$AgentDir = "C:\EDRAgent"
$PythonPath = "C:\Python311\python.exe" # Thay đổi nếu Python được cài đặt ở nơi khác
$RepoUrl = "https://github.com/YOUR_USERNAME/edr-prototype.git" # Thay đổi thành URL repo của bạn

# --- Kiểm tra và cài đặt Python (nếu cần) ---
Write-Host "Kiểm tra cài đặt Python..."
if (-not (Test-Path $PythonPath)) {
    Write-Host "Python không tìm thấy tại $PythonPath. Vui lòng cài đặt Python 3.8+ và cập nhật đường dẫn."
    Write-Host "Tải xuống từ: https://www.python.org/downloads/windows/"
    Exit 1
}

# --- Tạo thư mục Agent ---
Write-Host "Tạo thư mục Agent tại $AgentDir..."
if (-not (Test-Path $AgentDir)) {
    New-Item -Path $AgentDir -ItemType Directory -Force
}

# --- Clone hoặc cập nhật Repository ---
Write-Host "Clone hoặc cập nhật Repository..."
if (-not (Test-Path "$AgentDir\edr-prototype")) {
    # Nếu chưa có repo, clone về
    Write-Host "Cloning repository từ $RepoUrl..."
    git clone $RepoUrl "$AgentDir\edr-prototype"
} else {
    # Nếu đã có, cập nhật
    Write-Host "Cập nhật repository..."
    cd "$AgentDir\edr-prototype"
    git pull
}

# --- Di chuyển các file Agent vào thư mục chính của Agent ---
Write-Host "Di chuyển các file Agent..."
Copy-Item -Path "$AgentDir\edr-prototype\agent\event_collector.py" -Destination "$AgentDir\event_collector.py" -Force
Copy-Item -Path "$AgentDir\edr-prototype\agent\analysis_module.py" -Destination "$AgentDir\analysis_module.py" -Force
Copy-Item -Path "$AgentDir\edr-prototype\data\security_events.json" -Destination "$AgentDir\security_events.json" -Force
Copy-Item -Path "$AgentDir\edr-prototype\data\security_alerts.json" -Destination "$AgentDir\security_alerts.json" -Force

# --- Cài đặt dependencies cho Agent ---
Write-Host "Cài đặt dependencies cho Agent (pywin32)..."
& "$PythonPath" -m pip install pywin32
if ($LASTEXITCODE -ne 0) {
    Write-Host "Lỗi khi cài đặt pywin32. Đảm bảo Python được cài đặt đúng cách và có quyền truy cập Internet."
    Exit 1
}

# --- Cấu hình và chạy Agent (Ví dụ: Scheduled Task) ---
Write-Host "Cấu hình Scheduled Task để chạy Agent..."
$TaskName = "EDRAgentCollector"
$TaskAction = New-ScheduledTaskAction -Execute "$PythonPath" -Argument "$AgentDir\event_collector.py"
$TaskTrigger = New-ScheduledTaskTrigger -Daily -At "3am" # Chạy hàng ngày lúc 3 giờ sáng

# Xóa task cũ nếu tồn tại
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Đăng ký task mới
Register-ScheduledTask -TaskName $TaskName -Action $TaskAction -Trigger $TaskTrigger -Description "Thu thập Event Log cho EDR Agent" -User "System" -RunLevel Highest

Write-Host "Đã triển khai EDR Agent thành công!"
Write-Host "Scheduled Task '$TaskName' đã được tạo."
Write-Host "Bạn có thể kiểm tra trạng thái của task trong Task Scheduler."

# --- Hướng dẫn chạy thủ công để kiểm tra ---
Write-Host "\nĐể kiểm tra Agent thủ công, chạy lệnh sau trong PowerShell:
& \"$PythonPath\" \"$AgentDir\event_collector.py\""

# --- Ghi chú quan trọng ---
Write-Host "\nLƯU Ý QUAN TRỌNG: Script này là một nguyên mẫu. Trong môi trường sản xuất, bạn cần cân nhắc các yếu tố sau:
- Bảo mật: Xác thực, mã hóa dữ liệu, quản lý quyền.
- Độ tin cậy: Xử lý lỗi, ghi log chi tiết, cơ chế tự phục hồi.
- Hiệu suất: Tối ưu hóa việc thu thập và gửi dữ liệu."


