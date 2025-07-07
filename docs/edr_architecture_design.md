# Thiết kế kiến trúc hệ thống EDR trên Windows

## 1. Giới thiệu
Nguyên mẫu hệ thống EDR (Endpoint Detection and Response) này được thiết kế để giám sát và phân tích 50 loại sự kiện bảo mật quan trọng trên các điểm cuối Windows. Mục tiêu là cung cấp khả năng phát hiện sớm các mối đe dọa và hỗ trợ phản ứng nhanh chóng.

## 2. Các thành phần chính của hệ thống EDR
Hệ thống EDR sẽ bao gồm các thành phần chính sau:

*   **Agent thu thập dữ liệu (Endpoint Agent):** Triển khai trên mỗi điểm cuối Windows để thu thập các nhật ký sự kiện.
*   **Hệ thống lưu trữ dữ liệu (Data Storage):** Nơi lưu trữ tập trung các nhật ký sự kiện đã thu thập.
*   **Module phân tích và cảnh báo (Analysis & Alerting Module):** Xử lý, phân tích và phát hiện các hành vi đáng ngờ từ dữ liệu nhật ký.
*   **Giao diện người dùng (User Interface - Dashboard):** Cung cấp khả năng hiển thị, quản lý và tương tác với hệ thống.

## 3. Chi tiết kiến trúc

### 3.1. Agent thu thập dữ liệu (Endpoint Agent)

**Mục tiêu:** Thu thập các nhật ký sự kiện Windows được chỉ định (50 Event ID) một cách hiệu quả và đáng tin cậy.

**Công nghệ đề xuất:**

*   **PowerShell Scripts/Windows API:** Sử dụng PowerShell scripts hoặc các lệnh gọi Windows API để truy cập trực tiếp vào Event Log. Điều này cho phép kiểm soát chi tiết việc thu thập các Event ID cụ thể.
*   **Winlogbeat (Elastic Stack):** Một lightweight shipper có thể được cài đặt trên các điểm cuối để chuyển tiếp nhật ký sự kiện Windows đến một hệ thống tập trung (ví dụ: Elasticsearch). Winlogbeat cung cấp khả năng lọc mạnh mẽ và đáng tin cậy.

**Cơ chế thu thập:**

*   **Theo thời gian thực:** Agent sẽ liên tục giám sát Event Log và gửi các sự kiện mới ngay lập tức.
*   **Lọc Event ID:** Chỉ thu thập các Event ID đã được xác định trong danh sách 50 sự kiện quan trọng để giảm tải và tập trung vào dữ liệu liên quan đến bảo mật.
*   **Định dạng dữ liệu:** Chuyển đổi dữ liệu nhật ký sang định dạng JSON để dễ dàng xử lý và lưu trữ.

### 3.2. Hệ thống lưu trữ dữ liệu (Data Storage)

**Mục tiêu:** Lưu trữ an toàn, có thể mở rộng và dễ dàng truy vấn các nhật ký sự kiện.

**Công nghệ đề xuất:**

*   **Elasticsearch:** Một công cụ tìm kiếm và phân tích phân tán, mạnh mẽ, phù hợp để lưu trữ và lập chỉ mục dữ liệu nhật ký có cấu trúc và phi cấu trúc. Kết hợp với Kibana, nó cung cấp khả năng trực quan hóa và tìm kiếm mạnh mẽ.
*   **MongoDB:** Một cơ sở dữ liệu NoSQL dựa trên tài liệu, linh hoạt và có thể mở rộng, phù hợp để lưu trữ dữ liệu nhật ký JSON.

**Lựa chọn:** Elasticsearch được ưu tiên do khả năng tìm kiếm toàn văn, phân tích thời gian thực và tích hợp tốt với Kibana cho việc trực quan hóa.

### 3.3. Module phân tích và cảnh báo (Analysis & Alerting Module)

**Mục tiêu:** Phân tích dữ liệu nhật ký để phát hiện các hành vi đáng ngờ và tạo cảnh báo.

**Công nghệ đề xuất:**

*   **Python:** Ngôn ngữ lập trình chính để phát triển các thuật toán phân tích và logic cảnh báo. Các thư viện như `pandas` để xử lý dữ liệu, `scikit-learn` cho các thuật toán học máy (nếu cần phát hiện bất thường).
*   **Stream Processing (Apache Kafka/Logstash):** Để xử lý dữ liệu nhật ký theo thời gian thực trước khi lưu trữ và phân tích. Logstash có thể được sử dụng để làm giàu, chuyển đổi và định tuyến dữ liệu.

**Các loại phân tích:**

*   **Phân tích dựa trên luật (Rule-based Analysis):** Định nghĩa các luật dựa trên các Event ID cụ thể và các ngưỡng (ví dụ: 10 lần đăng nhập thất bại trong 5 phút).
*   **Phân tích hành vi (Behavioral Analysis):** Phát hiện các hành vi bất thường so với hành vi bình thường của người dùng hoặc hệ thống (ví dụ: đăng nhập từ vị trí lạ, truy cập tài khoản không thường xuyên sử dụng).
*   **Tương quan sự kiện (Event Correlation):** Kết hợp nhiều sự kiện khác nhau để phát hiện các chuỗi tấn công phức tạp (ví dụ: đăng nhập thất bại -> tạo người dùng mới -> thay đổi quyền).

**Cơ chế cảnh báo:**

*   **Email/SMS:** Gửi cảnh báo đến quản trị viên bảo mật.
*   **Webhook:** Tích hợp với các hệ thống cảnh báo khác (ví dụ: Slack, Microsoft Teams).
*   **Dashboard:** Hiển thị cảnh báo trực tiếp trên giao diện người dùng.

### 3.4. Giao diện người dùng (User Interface - Dashboard)

**Mục tiêu:** Cung cấp một bảng điều khiển trực quan để giám sát, tìm kiếm và quản lý các cảnh báo.

**Công nghệ đề xuất:**

*   **Kibana (Elastic Stack):** Nếu sử dụng Elasticsearch làm hệ thống lưu trữ, Kibana là lựa chọn tự nhiên để trực quan hóa dữ liệu, tạo dashboard và tìm kiếm nhật ký.
*   **React/Angular/Vue.js (Frontend Framework):** Để xây dựng một giao diện web tùy chỉnh, cung cấp khả năng tương tác cao.
*   **Flask/Node.js (Backend API):** Để xây dựng các API phục vụ dữ liệu từ Elasticsearch/MongoDB đến giao diện người dùng.

**Các tính năng chính:**

*   **Tổng quan (Overview Dashboard):** Hiển thị các số liệu thống kê quan trọng, số lượng cảnh báo, các sự kiện hàng đầu.
*   **Tìm kiếm nhật ký (Log Search):** Cho phép người dùng tìm kiếm và lọc các nhật ký sự kiện dựa trên nhiều tiêu chí.
*   **Quản lý cảnh báo (Alert Management):** Hiển thị danh sách các cảnh báo, trạng thái, mức độ ưu tiên và khả năng xử lý cảnh báo.
*   **Trực quan hóa dữ liệu (Data Visualization):** Biểu đồ, đồ thị để hiển thị xu hướng và mẫu hình của các sự kiện.

## 4. Xử lý 50 Event ID cụ thể

Danh sách 50 Event ID được cung cấp sẽ được phân loại và ánh xạ tới các luật phân tích và cảnh báo cụ thể. Ví dụ:

*   **Failed Login Attempts (Event ID: 4625):** Sẽ được theo dõi và cảnh báo nếu số lần thất bại vượt quá ngưỡng trong một khoảng thời gian nhất định.
*   **New User Creation (Event ID: 4720):** Sẽ tạo cảnh báo ngay lập tức và yêu cầu xác minh.
*   **Privileged Account Usage (Event ID: 4672):** Sẽ được giám sát chặt chẽ và cảnh báo nếu có hoạt động bất thường.
*   **File and Folder Access (Event ID: 4663):** Sẽ được theo dõi cho các truy cập trái phép hoặc truy cập vào các tệp nhạy cảm.

**Phân loại Event ID:**

*   **Nhóm sự kiện đăng nhập/xác thực:** 1, 2, 3, 7, 8, 10, 11, 12, 13, 14, 15, 35.
*   **Nhóm sự kiện thay đổi tài khoản/nhóm:** 4, 6, 9, 28.
*   **Nhóm sự kiện truy cập tài nguyên:** 17, 18, 36, 43, 45.
*   **Nhóm sự kiện hệ thống/ứng dụng:** 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 37, 38, 39, 40, 41, 42, 44, 46, 47, 48, 49, 50.

## 5. Môi trường triển khai

Nguyên mẫu sẽ được triển khai trên môi trường Windows, có thể là máy ảo hoặc máy vật lý. Các công cụ và thư viện cần thiết sẽ được cài đặt và cấu hình.

## 6. Kết luận

Kiến trúc này cung cấp một khung sườn vững chắc cho việc phát triển nguyên mẫu EDR trên Windows. Việc lựa chọn công nghệ và thiết kế module tập trung vào khả năng thu thập, lưu trữ, phân tích và trình bày dữ liệu hiệu quả để phát hiện và phản ứng với các mối đe dọa bảo mật.

