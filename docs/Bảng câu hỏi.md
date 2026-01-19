**Bảng câu hỏi cho khảo sát**

### **Cấu trúc chung**

Bảng câu hỏi nên chia làm **4 phần chính**. Chúng ta sẽ sử dụng chủ yếu là **Thang đo Likert 5 điểm** (1: Hoàn toàn không đồng ý \-\> 5: Hoàn toàn đồng ý) để dễ tính toán điểm trung bình (Mean) và độ lệch chuẩn (Std Dev).

### **PHẦN 1: THÔNG TIN CHUNG (Biến định danh \- Demographics)**

*Mục đích: Dùng để phân nhóm (segmentation) khi vẽ biểu đồ trong Power BI.*

1. **Giới tính:** (Nam / Nữ / Khác)  
2. **Kỳ học:** kỳ 1, kỳ 2, kỳ 3….   
3. **Chuyên ngành (Major):**  
   * *Lưu ý:* Nên để dạng Dropdown list cố định:
     - CNTT (Công nghệ thông tin)
     - Kỹ thuật phần mềm
     - Phát triển Web
     - Phát triển Mobile
     - Thiết kế Đồ họa
     - Thiết kế UX/UI
     - Kinh tế - Quản lý
     - Marketing & Bán hàng
     - Du lịch & Khách sạn
     - Quản lý Nhà hàng
     - Kế toán
     - Quản lý Sự kiện
     - Không để điền tay để tránh lỗi chính tả khi Group By trong SQL.  
4. **Tình trạng cư trú:** (Ở trọ / Ở với gia đình / KTX)  
   * *Lý do:* Yếu tố này ảnh hưởng mạnh đến áp lực tài chính.  
5. **GPA tích lũy hiện tại (Ước lượng):** (\< 5.0 / 5.0 \- 6.5 / 6.5 \- 8.0 / \> 8.0)  
   * *Lý do:* Xem xét mối tương quan giữa điểm số và hạnh phúc.

### **PHẦN 2: ĐO LƯỜNG MỨC ĐỘ HẠNH PHÚC (Biến phụ thuộc \- Y)**

*Mục đích: Đây là kết quả đầu ra (Output) của mô hình. Là con số cụ thể để đại diện cho "Hạnh phúc".*

Câu hỏi: Hãy đánh giá mức độ đồng ý của bạn với các nhận định sau về cuộc sống hiện tại:

(Thang điểm 1-5)

1. Nhìn chung, tôi cảm thấy hài lòng với cuộc sống hiện tại của mình.  
2. Tôi thường xuyên cảm thấy vui vẻ và tràn đầy năng lượng khi đến trường.  
3. Tôi cảm thấy cuộc sống của mình tại FPoly có ý nghĩa và mục tiêu rõ ràng.  
4. Nếu được chọn lại, tôi vẫn sẽ chọn học tại FPoly.

### **PHẦN 3: CÁC YẾU TỐ ẢNH HƯỞNG (Biến độc lập \- X)**

*Mục đích: Tìm ra nguyên nhân. Chúng ta chia thành 4 nhóm giả thuyết chính.*

#### **Nhóm 1: Yếu tố Học tập & Đào tạo (Academic Factors)**

1. Chương trình học hiện tại phù hợp với năng lực của tôi.  
2. Tôi cảm thấy áp lực nặng nề với tần suất Deadline/Assignment/Lab. (Câu hỏi đảo ngược)  
3. Phương pháp giảng dạy của giảng viên tạo hứng thú cho tôi.  
4. Hệ thống LMS/CMS/AP hoạt động ổn định, hỗ trợ tốt cho việc học.

#### **Nhóm 2: Môi trường & Cơ sở vật chất (Environment & Facilities)**

1. Cơ sở vật chất (phòng học, máy lạnh, wifi) đáp ứng tốt nhu cầu của tôi.  
2. Tôi hài lòng với các dịch vụ tiện ích (giữ xe, canteen, thang máy).  
3. Môi trường học tập tại FPoly năng động và cởi mở.

#### **Nhóm 3: Quan hệ xã hội (Social Relationships)**

1. Tôi có những người bạn thân thiết tại trường để chia sẻ khó khăn.  
2. Tôi cảm thấy dễ dàng hòa nhập với các hoạt động phong trào/CLB tại trường.  
3. Tôi nhận được sự ủng hộ từ gia đình trong quá trình học tập.

#### **Nhóm 4: Tài chính & Triển vọng nghề nghiệp (Finance & Career)**

1. Học phí hiện tại tương xứng với chất lượng đào tạo nhận được.  
2. Tôi lo lắng về gánh nặng chi phí sinh hoạt hàng tháng. (Câu hỏi đảo ngược)  
3. Tôi tự tin về cơ hội việc làm sau khi tốt nghiệp FPoly.

### **PHẦN 4: CÂU HỎI MỞ & KIỂM SOÁT (Qualitative & QC)**

1. **Câu hỏi kiểm soát (Trap Question):** "Vui lòng chọn đáp án số 2 cho câu hỏi này để chúng tôi biết bạn đang đọc kỹ."  
   * *Mục đích:* Loại bỏ các dòng dữ liệu nhiễu (người điền bừa) trước khi đưa vào Python.  
2. **Câu hỏi mở (Optional):** "Nếu có một điều ước để làm sinh viên FPoly hạnh phúc hơn, bạn ước điều gì?"  
   * *Mục đích:* Dùng để phân tích từ khóa (Word Cloud) hoặc tìm kiếm Insight mà các câu hỏi trắc nghiệm bỏ sót.

