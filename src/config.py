class Config:
    # Mapping câu hỏi thô sang biến tường minh
    COLUMN_MAPPING = {
            'Dấu thời gian': 'timestamp',
            'Tên người dùng': 'email',
            'Xác nhận đồng ý tham gia khảo sát:': 'consent',
            'Bạn là sinh viên của ngành:': 'major',
            'Bạn đang học ở kỳ:': 'semester',
            'GPA hiện tại của bạn:': 'gpa',
            'Tình trạng cư trú của bạn hiện tại:': 'residence_status',
            'Nhìn chung, tôi cảm thấy hài lòng với cuộc sống hiện tại của mình.': 'satisfaction_life',
            'Tôi thường xuyên cảm thấy vui vẻ và tràn đầy năng lượng khi đến trường.': 'satisfaction_school_life',
            'Tôi cảm thấy cuộc sống của mình tại FPoly có ý nghĩa và mục tiêu rõ ràng.': 'satisfaction_meaningful_life',
            'Nếu được chọn lại, tôi vẫn sẽ chọn học tại FPoly.': 'satisfaction_choice',
            'Chương trình học hiện tại phù hợp với năng lực của tôi.': 'academic_curriculum_suitability',
            'Tôi cảm thấy áp lực nặng nề với tần suất Deadline/Assignment/Lab.': 'academic_pressure',
            'Phương pháp giảng dạy của giảng viên tạo hứng thú cho tôi.': 'academic_teaching_method',
            'Hệ thống LMS/CMS/AP hoạt động ổn định, hỗ trợ tốt cho việc học.': 'academic_lms_stability',
            'Cơ sở vật chất (phòng học, máy lạnh, wifi) đáp ứng tốt nhu cầu của tôi.': 'env_facilities',
            'Tôi hài lòng với các dịch vụ tiện ích (giữ xe, canteen, thang máy).': 'env_services',
            'Môi trường học tập tại FPoly năng động và cởi mở.': 'env_dynamic',
            'Tôi có những người bạn thân thiết tại trường để chia sẻ khó khăn.': 'social_friends',
            'Tôi cảm thấy dễ dàng hòa nhập với các hoạt động phong trào/CLB tại trường.': 'social_activities_clubs',
            'Tôi nhận được sự ủng hộ từ gia đình trong quá trình học tập.': 'social_family_support',
            'Học phí hiện tại tương xứng với chất lượng đào tạo nhận được.': 'finance_tuition_fee',
            'Tôi lo lắng về gánh nặng chi phí sinh hoạt hàng tháng.': 'finance_living_cost',
            'Tôi tự tin về cơ hội việc làm sau khi tốt nghiệp FPoly.': 'future_job_opportunity',
            'Vui lòng chọn đáp án "Không đồng ý" cho câu hỏi này để chúng tôi biết bạn đang đọc kỹ.': 'attention_check',
            'Nếu có một điều ước để làm sinh viên FPoly hạnh phúc hơn, bạn ước điều gì?': 'wish'
        }

    # Mapping lời đánh giá sang mức độ dạng số
    LIKERT_MAPPING = {
            'Hoàn toàn không đồng ý': 1,
            'Không đồng ý': 2,
            'Trung lập': 3,
            'Đồng ý': 4,
            'Hoàn toàn đồng ý': 5
        }

    # MAPPING GPA
    GPA_MAPPING = {
            '<= 5.0': 4.5,
            '(5.0 - 6.0]': 5.5,
            '(6.0 - 7.0]': 6.5,
            '(7.0 - 8.0]': 7.5,
            '(8.0 - 9.0]': 8.5,
            '>= 9.0': 9.5
        }

    # Danh sách các biến cần đảo ngược điểm (Reverse Coding)
    REVERSE_COLS = ["aca_deadline_pressure", "fin_living_cost_worry"]