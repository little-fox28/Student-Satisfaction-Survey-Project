class Config:
    # Mapping câu hỏi thô sang biến tường minh
    COLUMN_MAPPING = {
        # Metadata
        'Dấu thời gian': 'timestamp',
        'Tên người dùng': 'email',
        'Địa chỉ email': 'email',
        'Xác nhận đồng ý tham gia khảo sát:': 'consent',

        # Demographics (dem_)
        'Bạn là sinh viên của ngành:': 'dem_major',
        'Bạn đang học ở kỳ:': 'dem_semester',
        'GPA hiện tại của bạn:': 'dem_gpa',
        'Tình trạng cư trú của bạn hiện tại:': 'dem_residence',

        # Happiness Indicators (hap_)
        'Nhìn chung, tôi cảm thấy hài lòng với cuộc sống hiện tại của mình.': 'hap_general_satisfaction',
        'Tôi thường xuyên cảm thấy vui vẻ và tràn đầy năng lượng khi đến trường.': 'hap_school_energy',
        'Tôi cảm thấy cuộc sống của mình tại FPoly có ý nghĩa và mục tiêu rõ ràng.': 'hap_meaningful_life',
        'Nếu được chọn lại, tôi vẫn sẽ chọn học tại FPoly.': 'hap_loyalty_choice', # Fixes the KeyError

        # Academic Factors (aca_)
        'Chương trình học hiện tại phù hợp với năng lực của tôi.': 'aca_curriculum_fit',
        'Tôi cảm thấy áp lực nặng nề với tần suất Deadline/Assignment/Lab.': 'aca_deadline_pressure', # Reverse coded
        'Phương pháp giảng dạy của giảng viên tạo hứng thú cho tôi.': 'aca_teaching_quality',
        'Hệ thống LMS/CMS/AP hoạt động ổn định, hỗ trợ tốt cho việc học.': 'aca_lms_stability',

        # Environment Factors (env_)
        'Cơ sở vật chất (phòng học, máy lạnh, wifi) đáp ứng tốt nhu cầu của tôi.': 'env_facilities',
        'Tôi hài lòng với các dịch vụ tiện ích (giữ xe, canteen, thang máy).': 'env_utilities',
        'Môi trường học tập tại FPoly năng động và cởi mở.': 'env_dynamic_culture',

        # Social Factors (soc_)
        'Tôi có những người bạn thân thiết tại trường để chia sẻ khó khăn.': 'soc_friendship_support',
        'Tôi cảm thấy dễ dàng hòa nhập với các hoạt động phong trào/CLB tại trường.': 'soc_activity_integration',
        'Tôi nhận được sự ủng hộ từ gia đình trong quá trình học tập.': 'soc_family_support',

        # Finance & Future Factors (fin_)
        'Học phí hiện tại tương xứng với chất lượng đào tạo nhận được.': 'fin_tuition_value',
        'Tôi lo lắng về gánh nặng chi phí sinh hoạt hàng tháng.': 'fin_living_cost_worry', # Reverse coded
        'Tôi tự tin về cơ hội việc làm sau khi tốt nghiệp FPoly.': 'fin_job_prospects',

        # Quality Control
        'Vui lòng chọn đáp án "Không đồng ý" cho câu hỏi này để chúng tôi biết bạn đang đọc kỹ.': 'attention_check',
        'Nếu có một điều ước để làm sinh viên FPoly hạnh phúc hơn, bạn ước điều gì?': 'wish',
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