# METADATA: Student Satisfaction & Happiness Survey (FPOLY HCM)

## 1. Project Overview
Dự án tập trung vào việc thu thập và phân tích mức độ hài lòng của sinh viên tại FPOLY cơ sở HCM. Mô hình phân tích dựa trên giả thuyết các nhóm nhân tố tác động (X) sẽ quyết định chỉ số hạnh phúc đầu ra (Y).

## 2. Variable Model Structure
* **Dependent Variable (Y)**: Chỉ số Hạnh phúc tổng thể, đo lường kết quả đầu ra của trải nghiệm sinh viên.
* **Independent Variables (X)**: Gồm 4 nhóm nhân tố ảnh hưởng: Học tập (X1), Môi trường (X2), Xã hội (X3), và Tài chính (X4).
* **Control Variables (QC)**: Biến kiểm soát chất lượng dữ liệu để loại bỏ phản hồi nhiễu.

---

## 3. Data Dictionary

| ID | Variable Name | Question Text | Group | Scale & Logic |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `dem_gender` | Giới tính (Nam/Nữ/Khác) | Demographics | Categorical |
| 2 | `dem_semester` | Kỳ học (Kỳ 1 -> Kỳ 9) | Demographics | Ordinal |
| 3 | `dem_major` | Chuyên ngành (Dropdown list) | Demographics | Categorical |
| 4 | `dem_residence` | Tình trạng cư trú (Trọ/Nhà/KTX) | Demographics | Categorical |
| 5 | `dem_gpa` | GPA tích lũy hiện tại | Demographics | Ordinal (Range) |
| 6 | `hap_overall_satisfaction` | Hài lòng với cuộc sống hiện tại | Happiness (Y) | Likert 1-5 |
| 7 | `hap_daily_joy` | Vui vẻ và năng lượng khi đến trường | Happiness (Y) | Likert 1-5 |
| 8 | `hap_life_purpose` | Cuộc sống tại FPoly có ý nghĩa/mục tiêu | Happiness (Y) | Likert 1-5 |
| 9 | `hap_loyalty_choice` | Sẽ vẫn chọn học tại FPoly nếu chọn lại | Happiness (Y) | Likert 1-5 |
| 10 | `aca_program_suitability` | Chương trình học phù hợp năng lực | Academic (X1) | Likert 1-5 |
| 11 | **`aca_deadline_pressure`** | Áp lực nặng nề với Deadline/Lab | Academic (X1) | **Reverse Likert 1-5** |
| 12 | `aca_teaching_quality` | Giảng viên tạo hứng thú giảng dạy | Academic (X1) | Likert 1-5 |
| 13 | `aca_system_stability` | Hệ thống LMS/CMS/AP hoạt động ổn định | Academic (X1) | Likert 1-5 |
| 14 | `env_facility_quality` | CSVC (máy lạnh, wifi) đáp ứng tốt | Environment (X2) | Likert 1-5 |
| 15 | `env_service_satisfaction` | Hài lòng dịch vụ (gửi xe, canteen...) | Environment (X2) | Likert 1-5 |
| 16 | `env_dynamic_culture` | Môi trường năng động và cởi mở | Environment (X2) | Likert 1-5 |
| 17 | `soc_peer_support` | Có bạn thân thiết chia sẻ khó khăn | Social (X3) | Likert 1-5 |
| 18 | `soc_community_join` | Dễ hòa nhập hoạt động phong trào/CLB | Social (X3) | Likert 1-5 |
| 19 | `soc_family_support` | Nhận được sự ủng hộ từ gia đình | Social (X3) | Likert 1-5 |
| 20 | `fin_tuition_value` | Học phí tương xứng chất lượng | Finance (X4) | Likert 1-5 |
| 21 | **`fin_living_cost_worry`** | Lo lắng về gánh nặng chi phí sinh hoạt | Finance (X4) | **Reverse Likert 1-5** |
| 22 | `fin_career_confidence` | Tự tin về cơ hội việc làm sau tốt nghiệp | Finance (X4) | Likert 1-5 |
| 23 | **`qc_trap_answer`** | Câu hỏi kiểm soát (Vui lòng chọn số 2) | QC | Constant = 2 |
| 24 | `text_student_wish` | Điều ước để sinh viên hạnh phúc hơn | Qualitative | String (Free text) |



---
*Last updated: 2026-01-19*