# 🚀 FPOLY HCM: Student Satisfaction & Happiness Analytics

## 📝 1. Tổng quan dự án (Project Overview)
Dự án tập trung xây dựng hệ thống báo cáo tự động nhằm đo lường và phân tích chỉ số **Hạnh phúc (Y)** của sinh viên tại **FPOLY cơ sở HCM**. Hệ thống bóc tách sự ảnh hưởng của các nhóm nhân tố (X) để cung cấp cái nhìn toàn diện về trải nghiệm học đường.



* **🎯 Mục tiêu:** Định lượng hóa mức độ hài lòng của sinh viên để hỗ trợ nhà trường đưa ra các quyết định cải thiện chất lượng.
* **📊 Phương pháp:** Khảo sát định lượng thông qua **thang đo Likert 5 điểm**.
* **🛠️ Công nghệ:** Python (Pandas, Numpy), Streamlit, Google Forms API.

---

## 🏗️ 2. Cấu trúc thư mục (Project Structure)
```text
fpoly-happiness-report/
├── data/
│   ├── raw/                        # 📁 Dữ liệu thô từ Google Form (CSV)
│   └── processed/                  # 📁 Dữ liệu đã làm sạch & xử lý đảo điểm
├── src/
│   ├── etl_process.py              # ⚙️ Script lọc Trap & Reverse Coding (DE)
│   ├── analytics.py                # 📈 Script tính toán chỉ số thống kê (DA)
│   └── app.py                      # 🌐 Giao diện Dashboard trực quan (Web)
├── docs/
│   ├── METADATA.md                 # 📖 Từ điển dữ liệu & Logic xử lý
│   ├── requirement.md              # 📋 Đặc tả yêu cầu gốc của dự án
│   └── DUMMY_DATA_GUIDE.md         # 🧪 Hướng dẫn sử dụng dữ liệu giả lập
└── requirements.txt                # 📦 Danh sách thư viện Python cần thiết
```
---

## ⚙️ 3. Hướng dẫn Cài đặt và Sử dụng (Setup and Usage Guide)

### a. Cài đặt các thư viện cần thiết (Install Dependencies)

Để cài đặt tất cả các thư viện Python cần thiết cho dự án, hãy chạy lệnh sau trong terminal từ thư mục gốc của dự án:

```bash
pip install -r requirements.txt
```
*Lưu ý: Bạn nên tạo và kích hoạt một môi trường ảo (virtual environment) trước khi cài đặt để tránh xung đột với các thư viện hệ thống.*

### b. Chuẩn bị dữ liệu (Data Preparation)

#### Tùy chọn 1: Sử dụng dữ liệu khảo sát thật
(Mô tả cách lấy dữ liệu thật ở đây)

#### Tùy chọn 2: Tạo dữ liệu giả lập (Generate Dummy Data)
Trong trường hợp không có dữ liệu thật, dự án cung cấp một script để tạo dữ liệu giả lập cho mục đích phát triển và kiểm thử.

**Cách thực hiện:**

1.  Mở terminal của bạn.
2.  Đảm bảo đang ở trong thư mục gốc của dự án (`Student_Satisfaction_Survey`).
3.  Chạy lệnh sau:
    ```bash
    python src/etl/generate_dummy_data.py
    ```
**Kết quả:**
Lệnh này sẽ thực thi script và tạo ra một file `survey_dummy_data.csv` tại đường dẫn `data/raw/survey_dummy_data.csv`. Dữ liệu này đã sẵn sàng để được sử dụng bởi các script phân tích tiếp theo.

-----
Lần cuối cập nhật: 20/01/2026 bởi BLOSSOM TEAM