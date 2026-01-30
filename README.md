# 🚀 FPOLY HCM: Student Satisfaction & Happiness Analytics

Dự án tập trung xây dựng hệ thống báo cáo tự động nhằm đo lường và phân tích chỉ số **Hạnh phúc (Y)** của sinh viên tại **FPOLY cơ sở HCM**. Hệ thống bóc tách sự ảnh hưởng của các nhóm nhân tố (X) để cung cấp cái nhìn toàn diện về trải nghiệm học đường.

---

## 🎯 1. Tổng quan (Project Overview)

- **Mục tiêu:** Định lượng hóa mức độ hài lòng của sinh viên để hỗ trợ nhà trường đưa ra các quyết định cải thiện chất lượng.
- **Phương pháp:** Khảo sát định lượng thông qua **thang đo Likert 5 điểm**.
- **Công nghệ:** Python (Pandas, Numpy), Streamlit, Google Forms API.

---

## 🏗️ 2. Cấu trúc thư mục (Project Structure)

```text
fpoly-happiness-report/
├── data/
│   ├── raw/                        # 📁 Dữ liệu thô từ Google Form (CSV)
│   └── processed/                  # 📁 Dữ liệu đã làm sạch & xử lý đảo điểm
├── src/
│   ├── analytics/                  # 📈 Chứa script tính toán chỉ số thống kê (DA)
│   │   └── analyzer.py
│   ├── dashboard/                  # 🌐 Chứa giao diện Dashboard trực quan (Web)
│   │   └── app.py
│   ├── etl/                        # ⚙️ Chứa script lọc Trap & Reverse Coding (DE)
│   │   └── processor.py
│   ├── __init__.py                 # Khởi tạo gói Python
│   └── config.py                   # Cấu hình dự án (mapping cột, v.v.)
├── main.ipynb                      # 🧪 Jupyter Notebook để chạy pipeline ETL và phân tích tương tác
├── docs/
│   ├── METADATA.md                 # 📖 Từ điển dữ liệu & Logic xử lý
│   ├── requirement.md              # 📋 Đặc tả yêu cầu gốc của dự án
│   └── DUMMY_DATA_GUIDE.md         # 🧪 Hướng dẫn sử dụng dữ liệu giả lập
└── requirements.txt                # 📦 Danh sách thư viện Python cần thiết
```

---

## ⚙️ 3. Yêu cầu hệ thống (System Requirements)

### ✅ Yêu cầu chức năng (Functional Requirements)

- **Thu thập:** Tích hợp dữ liệu tự động hoặc bán tự động từ Google Form.
- **Xử lý ETL:**
    - Tự động lọc bỏ các phản hồi không nghiêm túc qua câu hỏi bẫy (`qc_trap_answer`).
    - Thực hiện đảo ngược điểm (Reverse Coding) cho các biến tâm lý tiêu cực.
- **Tính toán:** Tính điểm trung bình (Mean) và độ lệch chuẩn (Std Dev) cho các nhóm chỉ số.
- **Trực quan:** Hiển thị biểu đồ Radar so sánh 4 nhóm nhân tố X, Boxplot theo GPA và Word Cloud cho ý kiến mở.

### ⚙️ Yêu cầu phi chức năng (Non-Functional Requirements)

- **Độ chính xác:** Logic đảo điểm và tính toán chỉ số phải khớp 100% với đặc tả kỹ thuật.
- **Bảo mật:** Ẩn danh tính sinh viên trong các báo cáo hiển thị.
- **Tính linh hoạt:** Chuyển đổi dễ dàng giữa dữ liệu Dummy (phát triển) và Production (vận hành thật).

---

## 🧪 4. Mô hình dữ liệu (Data Architecture)

### 🧩 Biến độc lập (Independent Variables - X)

Đo lường các nhân tố tác động qua 4 nhóm chính:

- **Academic (X1):** Chương trình học, áp lực deadline, giảng dạy, LMS.
- **Environment (X2):** Cơ sở vật chất, dịch vụ tiện ích, văn hóa trường học.
- **Social (X3):** Quan hệ bạn bè, sự hòa nhập CLB, gia đình.
- **Finance (X4):** Giá trị học phí, chi phí sinh hoạt, triển vọng nghề nghiệp.

### 🏆 Biến phụ thuộc (Dependent Variable - Y)

- **Happiness Index:** Chỉ số đo lường mức độ hài lòng, niềm vui và ý nghĩa cuộc sống tại FPOLY.

---

## 🛠️ 5. Quy trình xử lý (Technical Workflow)

### 🏗️ Nhiệm vụ Data Engineer (ETL Logic)

- **Lọc dữ liệu:** Loại bỏ bản ghi nếu `qc_trap_answer != 2`.
- **Đảo ngược điểm:** Áp dụng cho các biến tiêu cực để điểm cao luôn đồng nghĩa với sự tích cực.
    - `aca_2`: Áp lực nặng nề với Deadline/Lab.
    - `fin_2`: Lo lắng về gánh nặng chi phí sinh hoạt.
    - **Công thức:** `$Score_{new} = 6 - Score_{old}$`

### 📊 Nhiệm vụ Data Analyst (Analytics Logic)

- **Thống kê:** Tính Mean cho các nhóm X và chỉ số Y tổng hợp.
- **Phân đoạn:** So sánh mức độ hạnh phúc giữa các nhóm chuyên ngành, kỳ học và tình trạng cư trú.
- **NLP:** Xử lý văn bản từ câu hỏi "Điều ước" để tìm ra các insight tiềm ẩn.

---

## 📦 7. Hướng dẫn cài đặt (Quick Start)

1.  **Clone repository:**
    ```bash
    git clone https://github.com/fpoly-hcm/happiness-analytics.git
    ```
2.  **Cài đặt thư viện:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Chuẩn bị dữ liệu:**
    Đặt file khảo sát thô (CSV) vào `data/raw/fpoly_survey.csv`.

4.  **Khởi chạy Dashboard (Recommended):**
    Dashboard Streamlit sẽ tự động chạy toàn bộ pipeline ETL và phân tích.
    ```bash
    streamlit run src/dashboard/app.py
    ```

5.  **Chạy Pipeline tương tác với Jupyter Notebook (Optional):**
    Để kiểm tra và chạy từng bước ETL và phân tích một cách tương tác:
    ```bash
    jupyter lab main.ipynb
    ```
    hoặc
    ```bash
    jupyter notebook main.ipynb
    ```
    Sau đó, bạn có thể chạy các cell trong notebook.

---
| *Lần cuối cập nhật: 21/01/2026 bởi BLOSSOM TEAM*
