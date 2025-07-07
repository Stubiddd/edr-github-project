# Tài liệu hướng dẫn triển khai hệ thống EDR trên Windows

**Tác giả:** Manus AI  
**Ngày tạo:** 7 tháng 7, 2025  
**Phiên bản:** 1.0

## Mục lục

1. [Giới thiệu](#giới-thiệu)
2. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
3. [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
4. [Hướng dẫn cài đặt](#hướng-dẫn-cài-đặt)
5. [Cấu hình hệ thống](#cấu-hình-hệ-thống)
6. [Sử dụng hệ thống](#sử-dụng-hệ-thống)
7. [Bảo trì và khắc phục sự cố](#bảo-trì-và-khắc-phục-sự-cố)
8. [Tài liệu tham khảo](#tài-liệu-tham-khảo)

## Giới thiệu

Hệ thống EDR (Endpoint Detection and Response) được phát triển để cung cấp khả năng giám sát, phát hiện và phản ứng với các mối đe dọa bảo mật trên các điểm cuối Windows. Hệ thống này được thiết kế để theo dõi 50 loại sự kiện bảo mật quan trọng và cung cấp cảnh báo kịp thời cho các quản trị viên bảo mật.

### Mục tiêu của hệ thống

Hệ thống EDR này nhằm mục đích:

- **Giám sát liên tục:** Theo dõi các hoạt động trên điểm cuối Windows 24/7
- **Phát hiện sớm:** Xác định các mối đe dọa và hành vi đáng ngờ trong thời gian thực
- **Phản ứng nhanh:** Cung cấp cảnh báo và thông tin chi tiết để hỗ trợ phản ứng sự cố
- **Phân tích toàn diện:** Cung cấp khả năng phân tích và báo cáo chi tiết về các sự kiện bảo mật

### Các tính năng chính

1. **Thu thập dữ liệu tự động:** Tự động thu thập các Event Log từ Windows Event Viewer
2. **Phân tích thông minh:** Sử dụng các quy tắc và thuật toán để phát hiện hành vi bất thường
3. **Cảnh báo thời gian thực:** Gửi cảnh báo ngay lập tức khi phát hiện mối đe dọa
4. **Dashboard trực quan:** Giao diện web hiện đại để giám sát và quản lý hệ thống
5. **API RESTful:** Cung cấp API để tích hợp với các hệ thống khác

## Yêu cầu hệ thống

### Yêu cầu phần cứng tối thiểu

- **CPU:** Intel Core i3 hoặc AMD Ryzen 3 (2 cores, 2.5GHz)
- **RAM:** 4GB (khuyến nghị 8GB)
- **Ổ cứng:** 50GB dung lượng trống
- **Mạng:** Kết nối Internet ổn định

### Yêu cầu phần mềm

- **Hệ điều hành:** Windows 10/11 hoặc Windows Server 2016/2019/2022
- **Python:** Phiên bản 3.8 trở lên
- **Node.js:** Phiên bản 16 trở lên (cho frontend)
- **Quyền quản trị:** Quyền Administrator để truy cập Event Log

### Yêu cầu mạng

- **Port 5000:** Cho Flask backend API
- **Port 5173:** Cho React frontend (development)
- **Port 80/443:** Cho production deployment

## Kiến trúc hệ thống

Hệ thống EDR bao gồm các thành phần chính sau:

### 1. Agent thu thập dữ liệu (Data Collection Agent)

Agent này chạy trên mỗi điểm cuối Windows và có trách nhiệm:

- Thu thập các Event Log từ Windows Event Viewer
- Lọc và xử lý dữ liệu theo danh sách 50 Event ID được định nghĩa
- Chuyển đổi dữ liệu sang định dạng JSON
- Gửi dữ liệu đến hệ thống trung tâm

**Công nghệ sử dụng:**
- Python với thư viện `pywin32` để truy cập Windows API
- JSON để định dạng dữ liệu
- HTTP/HTTPS để truyền tải dữ liệu

### 2. Module phân tích và cảnh báo (Analysis & Alerting Module)

Module này thực hiện:

- Phân tích dữ liệu Event Log theo các quy tắc được định nghĩa
- Phát hiện các hành vi bất thường và mối đe dọa tiềm ẩn
- Tạo cảnh báo với các mức độ ưu tiên khác nhau
- Lưu trữ kết quả phân tích

**Các loại phân tích:**
- **Phân tích dựa trên quy tắc:** Kiểm tra các điều kiện cụ thể
- **Phân tích hành vi:** So sánh với hành vi bình thường
- **Tương quan sự kiện:** Kết hợp nhiều sự kiện để phát hiện tấn công phức tạp

### 3. Hệ thống lưu trữ dữ liệu (Data Storage System)

Hệ thống lưu trữ bao gồm:

- **File JSON:** Lưu trữ dữ liệu Event Log và cảnh báo
- **SQLite Database:** Lưu trữ metadata và cấu hình hệ thống
- **Log files:** Lưu trữ nhật ký hoạt động của hệ thống

### 4. API Backend (Flask Application)

Backend API cung cấp:

- RESTful API endpoints để truy cập dữ liệu
- Xử lý logic nghiệp vụ
- Quản lý xác thực và phân quyền
- Tích hợp với các hệ thống bên ngoài

**Các endpoint chính:**
- `/api/edr/events` - Lấy danh sách sự kiện
- `/api/edr/alerts` - Lấy danh sách cảnh báo
- `/api/edr/stats` - Lấy thống kê tổng quan
- `/api/edr/event-distribution` - Phân bố Event ID
- `/api/edr/timeline` - Timeline sự kiện

### 5. Frontend Dashboard (React Application)

Giao diện người dùng cung cấp:

- Dashboard tổng quan với các chỉ số quan trọng
- Danh sách cảnh báo với khả năng lọc và tìm kiếm
- Biểu đồ và visualization cho dữ liệu
- Giao diện quản lý cấu hình hệ thống

**Các tính năng chính:**
- Responsive design cho desktop và mobile
- Real-time updates
- Interactive charts và graphs
- Export dữ liệu

## Hướng dẫn cài đặt

### Bước 1: Chuẩn bị môi trường

1. **Cài đặt Python:**
   ```bash
   # Tải Python từ https://python.org
   # Chọn phiên bản 3.8 trở lên
   # Đảm bảo chọn "Add Python to PATH"
   ```

2. **Cài đặt Node.js:**
   ```bash
   # Tải Node.js từ https://nodejs.org
   # Chọn phiên bản LTS
   ```

3. **Cài đặt Git:**
   ```bash
   # Tải Git từ https://git-scm.com
   ```

### Bước 2: Tải mã nguồn

```bash
# Clone repository (nếu có)
git clone <repository-url>
cd edr-system

# Hoặc tạo thư mục mới
mkdir edr-system
cd edr-system
```

### Bước 3: Cài đặt Backend

1. **Tạo virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Cài đặt dependencies:**
   ```bash
   pip install flask flask-cors flask-sqlalchemy pywin32
   ```

3. **Tạo cấu trúc thư mục:**
   ```
   edr-backend/
   ├── src/
   │   ├── routes/
   │   │   ├── __init__.py
   │   │   ├── edr.py
   │   │   └── user.py
   │   ├── models/
   │   │   ├── __init__.py
   │   │   └── user.py
   │   ├── static/
   │   ├── database/
   │   └── main.py
   ├── venv/
   └── requirements.txt
   ```

### Bước 4: Cài đặt Frontend

1. **Tạo React application:**
   ```bash
   npx create-react-app edr-dashboard
   cd edr-dashboard
   ```

2. **Cài đặt dependencies:**
   ```bash
   npm install recharts lucide-react
   npm install @shadcn/ui  # Nếu sử dụng
   ```

### Bước 5: Cấu hình hệ thống

1. **Cấu hình Backend:**
   - Chỉnh sửa file `src/main.py`
   - Cấu hình database connection
   - Thiết lập CORS policy

2. **Cấu hình Frontend:**
   - Cập nhật API endpoints
   - Cấu hình proxy cho development

### Bước 6: Khởi động hệ thống

1. **Khởi động Backend:**
   ```bash
   cd edr-backend
   venv\Scripts\activate
   python src/main.py
   ```

2. **Khởi động Frontend:**
   ```bash
   cd edr-dashboard
   npm start
   ```

3. **Truy cập hệ thống:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## Cấu hình hệ thống

### Cấu hình Event Collection

Hệ thống được cấu hình để thu thập 50 loại Event ID quan trọng. Danh sách này có thể được tùy chỉnh trong file `event_collector.py`:

```python
important_event_ids = [
    4625, 4740, 4624, 4720, 4672, 4722, 4723, 4724, 4725, 4726,
    # ... thêm các Event ID khác
]
```

### Cấu hình Analysis Rules

Các quy tắc phân tích được định nghĩa trong file `analysis_module.py`. Ví dụ:

```python
# Rule 1: Failed Login Attempts
if event["EventID"] == 4625:
    # Logic phát hiện đăng nhập thất bại
    
# Rule 2: New User Creation  
if event["EventID"] == 4720:
    # Logic phát hiện tạo user mới
```

### Cấu hình Alerting

Cấu hình cảnh báo bao gồm:

- **Ngưỡng cảnh báo:** Số lượng sự kiện tối đa trong khoảng thời gian
- **Mức độ ưu tiên:** High, Medium, Low
- **Phương thức thông báo:** Email, SMS, Webhook

### Cấu hình Database

Cấu hình kết nối database trong `main.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edr.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

## Sử dụng hệ thống

### Dashboard chính

Dashboard cung cấp cái nhìn tổng quan về:

- **Tổng số cảnh báo:** Hiển thị số lượng cảnh báo trong ngày
- **Sự kiện mức cao:** Số lượng cảnh báo mức độ cao cần xử lý ngay
- **Điểm cuối:** Số lượng endpoints đang được giám sát
- **Trạng thái hệ thống:** Tình trạng hoạt động của hệ thống

### Quản lý cảnh báo

Trang cảnh báo cho phép:

- Xem danh sách tất cả cảnh báo
- Lọc theo mức độ ưu tiên
- Tìm kiếm theo từ khóa
- Xem chi tiết từng cảnh báo
- Đánh dấu cảnh báo đã xử lý

### Phân tích sự kiện

Trang phân tích cung cấp:

- Biểu đồ phân bố Event ID
- Timeline sự kiện theo thời gian
- Thống kê theo loại sự kiện
- Báo cáo xu hướng

### API Usage

Sử dụng API để tích hợp với hệ thống khác:

```javascript
// Lấy danh sách cảnh báo
fetch('/api/edr/alerts')
  .then(response => response.json())
  .then(data => console.log(data));

// Lấy thống kê
fetch('/api/edr/stats')
  .then(response => response.json())
  .then(data => console.log(data));
```

## Bảo trì và khắc phục sự cố

### Bảo trì định kỳ

1. **Kiểm tra log files:**
   - Xem log của backend application
   - Kiểm tra log của data collection agent
   - Theo dõi performance metrics

2. **Backup dữ liệu:**
   - Backup database định kỳ
   - Lưu trữ event logs quan trọng
   - Backup cấu hình hệ thống

3. **Cập nhật hệ thống:**
   - Cập nhật dependencies
   - Patch security vulnerabilities
   - Nâng cấp phiên bản mới

### Khắc phục sự cố thường gặp

#### Sự cố 1: Agent không thu thập được dữ liệu

**Nguyên nhân:**
- Thiếu quyền Administrator
- Windows Event Log service không chạy
- Lỗi kết nối mạng

**Giải pháp:**
```bash
# Kiểm tra quyền
whoami /priv

# Khởi động Event Log service
net start eventlog

# Kiểm tra kết nối
ping <server-ip>
```

#### Sự cố 2: Backend API không phản hồi

**Nguyên nhân:**
- Port bị chặn
- Service không chạy
- Lỗi cấu hình

**Giải pháp:**
```bash
# Kiểm tra port
netstat -an | findstr :5000

# Khởi động lại service
python src/main.py

# Kiểm tra log
tail -f app.log
```

#### Sự cố 3: Frontend không hiển thị dữ liệu

**Nguyên nhân:**
- CORS policy
- API endpoint sai
- Network connectivity

**Giải pháp:**
```javascript
// Kiểm tra CORS
fetch('/api/edr/stats', {
  mode: 'cors',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Kiểm tra network tab trong browser
// Xem console errors
```

### Monitoring và Performance

1. **System Metrics:**
   - CPU usage
   - Memory consumption
   - Disk I/O
   - Network traffic

2. **Application Metrics:**
   - Response time
   - Error rate
   - Throughput
   - Active connections

3. **Business Metrics:**
   - Number of events processed
   - Alert generation rate
   - False positive rate
   - Mean time to detection

### Security Considerations

1. **Access Control:**
   - Implement authentication
   - Use role-based permissions
   - Secure API endpoints

2. **Data Protection:**
   - Encrypt sensitive data
   - Secure data transmission
   - Implement data retention policies

3. **System Hardening:**
   - Regular security updates
   - Network segmentation
   - Intrusion detection

## Tài liệu tham khảo

### Tài liệu kỹ thuật

1. **Microsoft Windows Event Log Documentation**
   - [Windows Event Log Reference](https://docs.microsoft.com/en-us/windows/win32/eventlog/event-logging)
   - [Security Event IDs](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/security-auditing-overview)

2. **Flask Documentation**
   - [Flask Official Documentation](https://flask.palletsprojects.com/)
   - [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)

3. **React Documentation**
   - [React Official Documentation](https://reactjs.org/docs/)
   - [Recharts Documentation](https://recharts.org/)

### Tài liệu bảo mật

1. **NIST Cybersecurity Framework**
   - [Framework Documentation](https://www.nist.gov/cyberframework)

2. **MITRE ATT&CK Framework**
   - [ATT&CK Matrix](https://attack.mitre.org/)

3. **SANS Institute Resources**
   - [Incident Response Guidelines](https://www.sans.org/white-papers/)

### Công cụ và thư viện

1. **Python Libraries:**
   - `pywin32` - Windows API access
   - `flask` - Web framework
   - `pandas` - Data analysis
   - `json` - JSON processing

2. **JavaScript Libraries:**
   - `react` - Frontend framework
   - `recharts` - Data visualization
   - `lucide-react` - Icons

3. **Development Tools:**
   - Visual Studio Code
   - Git
   - Postman (API testing)
   - Chrome DevTools

---

**Lưu ý:** Tài liệu này được tạo cho mục đích giáo dục và demo. Trong môi trường production, cần thêm các biện pháp bảo mật và tối ưu hóa hiệu suất phù hợp.

