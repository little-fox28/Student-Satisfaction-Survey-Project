**Lưu ý:** trước khi tính lọc các record không đủ điều kiện.

### **1\. Nhóm chỉ số mô tả tổng quan (Descriptive Metrics)**

*Dùng để trả lời câu hỏi: "Tình hình hiện tại như thế nào?"*

#### **A. Chỉ số Hạnh phúc Trung bình (Average Happiness Score \- AHS)**

Đây là chỉ số quan trọng nhất (North Star Metric) của dự án.

* **Dữ liệu nguồn:** 4 câu hỏi ở Phần 2\.  
* **Công thức: AHS=(Q2.1 \+ Q2.2 \+ Q2.3 \+ Q2.4)4  N**  
  *(Trong đó N là tổng số sinh viên khảo sát)*  
* **Insight:** Cho biết mức độ hạnh phúc chung của sinh viên FPoly đang ở mức nào trên thang 5 (Ví dụ: 3.8/5.0 là Khá hạnh phúc).

#### **B. Chỉ số Hài lòng theo từng nhóm yếu tố (Factor Satisfaction Score)**

* **Dữ liệu nguồn:** Phần 3 (Các nhóm Academic, Environment, Social, Finance).  
* **Cách tính:** Tính trung bình cộng (Mean) của tất cả câu hỏi trong từng nhóm.  
  * *Lưu ý:* Chuyển đổi các câu hỏi đảo ngược (Negative questions)   
* **Insight:** Biết được đâu là điểm mạnh (ví dụ: Cơ sở vật chất tốt) và đâu là điểm yếu (ví dụ: Áp lực Deadline quá cao) của nhà trường.

#### **C. Tỷ lệ Hạnh phúc ròng (Net Happiness Score \- Tương tự NPS)**

* **Cách tính:**  
  * Nhóm Hạnh phúc (Promoters): Chọn mức 4, 5\.  
  * Nhóm Không hạnh phúc (Detractors): Chọn mức 1, 2\.  
  * Score \= %Happy \- %Unhappy  
* **Insight:** Con số này cho thấy "thực lực" hạnh phúc. Nếu dương (+) là tốt, âm (-) là báo động.

---

### **2\. Nhóm chỉ số so sánh & Phân khúc (Comparative & Segmentation)**

*Dùng để trả lời câu hỏi: "Ai hạnh phúc hơn ai?" (Dựa vào Phần 1: Demographics)*

#### **D. Khoảng cách Hạnh phúc theo Kỳ học (Semester Happiness Curve)**

* **Cách tính:** Group By cột Kỳ học và tính Mean của AHS. Vẽ biểu đồ đường (Line Chart).  
* **Insight dự kiến:** Thường sinh viên kỳ 1 (Freshman) rất hào hứng (Hạnh phúc cao), kỳ 4-5 (Chuyên ngành) áp lực cao (Hạnh phúc giảm), kỳ 7 (Sắp ra trường) có thể tăng hoặc giảm tùy vào triển vọng nghề nghiệp.  
* **Biểu đồ:** Column Chart.

#### **E. Mối liên hệ giữa GPA và Hạnh phúc (GPA-Happiness Correlation)**

* **Cách tính:** So sánh điểm trung bình hạnh phúc giữa các nhóm GPA (\<5.0, 5.0-6.5, 6.5-8.0, \>8.0).  
* **Insight:** Trả lời câu hỏi kinh điển: *"Học giỏi có chắc là vui không?"*. Có thể bạn sẽ phát hiện ra nhóm GPA 6.5-8.0 lại hạnh phúc hơn nhóm \>8.0 (do ít áp lực hơn).

#### **F. Chỉ số áp lực tài chính theo nơi ở (Residence Stress Index)**

* **Cách tính:** Lọc riêng câu hỏi về "Gánh nặng chi phí" , so sánh giữa nhóm "Ở trọ" và "Ở với gia đình".  
* **Insight:** Chứng minh định lượng rằng sinh viên ở trọ chịu áp lực lớn hơn bao nhiêu % so với sinh viên ở nhà.

### **3\. Nhóm chỉ số phân tích chuyên sâu (Advanced Analytics)**

*Dùng để trả lời câu hỏi: "Yếu tố nào tác động mạnh nhất?" (Tìm nguyên nhân)*

#### **G. Hệ số tương quan Pearson (Pearson Correlation Coefficient \- r)**

* **Cách tính:** Dùng hàm CORREL() trong Excel hoặc df.corr() trong Python. Tính tương quan giữa điểm trung bình của **Từng nhóm yếu tố (X)** với **Điểm Hạnh phúc chung (Y)**.  
* **Giá trị:** r chạy từ \-1 đến 1\.  
  * r \> 0.5: Tác động mạnh.  
  * r \< 0.2: Ít tác động.  
* **Insight:**  
  * Ví dụ: Nếu r của nhóm "Quan hệ xã hội" \= 0.7, còn nhóm "Cơ sở vật chất" \= 0.3. **Kết luận:** *Để sinh viên hạnh phúc hơn, nhà trường nên tổ chức nhiều hoạt động kết nối (Teambuilding) thay vì chỉ tập trung xây sửa phòng học.* (Đây là insight giúp đạt điểm xuất sắc).

#### **H. Chỉ số rủi ro bỏ học (Retention Risk Index)**

* **Dữ liệu nguồn:** Câu hỏi 4 Phần 2 *"Nếu được chọn lại, tôi vẫn sẽ chọn học tại FPoly"*.  
* **Cách tính:** Tính % số sinh viên chọn mức 1 và 2 (Không đồng ý).  
* **Insight:** Báo động cho phòng Công tác sinh viên về tỷ lệ sinh viên có ý định rời bỏ trường hoặc không hài lòng với quyết định nhập học.

#### **I. Phân tích Từ khóa nỗi đau (Pain Point Word Cloud)**

* **Dữ liệu nguồn:** Câu hỏi mở Phần 4\.  
* **Cách tính:** Dùng Python (thư viện wordcloud, underthesea để tách từ tiếng Việt), loại bỏ các từ vô nghĩa (stopwords). Đếm tần suất từ xuất hiện.  
* **Insight:** Những từ khóa to nhất chính là vấn đề bức xúc nhất (ví dụ: "Gửi xe", "Wifi", "Deadline", "Học phí").