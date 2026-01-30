import pandas as pd
# For word cloud generation, these libraries would be needed:
# from wordcloud import WordCloud
# from underthesea import word_tokenize # For Vietnamese word tokenization

class DataAnalyzer:
    def __init__(self, file_path: str):
        """
        Khởi tạo với DataFrame đã qua xử lý ETL (sạch và đã đảo điểm).
        """
        self.df = pd.DataFrame(pd.read_csv(file_path))
        self.report = {}

    def analysis(self):
        """
        Method chính thực hiện toàn bộ 5 hướng phân tích chiến lược.
        """
        print("📊 Đang phân tích các chỉ số hạnh phúc...")
        
        self._calculate_ahs()                           # A. Chỉ số Hạnh phúc trung bình
        self._calculate_factor_scores()                 # B. Chỉ số Hạnh phúc theo các nhân tố X
        self._calculate_nhs()                           # C. Tỷ lệ Hạnh phúc ròng
        self._calculate_semester_happiness_curve()      # D. Khoảng cách Hạnh phúc theo Kỳ học
        self._calculate_gpa_happiness_correlation()     # E. Mối liên hệ giữa GPA và Hạnh phúc
        self._calculate_residence_stress_index()        # F. Chỉ số áp lực tài chính theo nơi ở
        self._calculate_correlations()                  # G. Tương quan Pearson
        self._calculate_retention_risk()                # H. Rủi ro bỏ học
        
        print("✅ Phân tích hoàn tất.")
        return self.report

    def _calculate_ahs(self):
        """A. Average Happiness Score (AHS)"""
        hap_cols = [c for c in self.df.columns if c.startswith('hap_')]
        # Tính điểm trung bình của từng SV, sau đó tính trung bình toàn trường
        self.df['individual_ahs'] = self.df[hap_cols].mean(axis=1)
        self.report['ahs_overall'] = round(self.df['individual_ahs'].mean(), 2)

    def _calculate_factor_scores(self):
        """B. Factor Satisfaction Score"""
        factors = {
            'Academic (X1)': [c for c in self.df.columns if c.startswith('aca_')],
            'Environment (X2)': [c for c in self.df.columns if c.startswith('env_')],
            'Social (X3)': [c for c in self.df.columns if c.startswith('soc_')],
            'Finance (X4)': [c for c in self.df.columns if c.startswith('fin_') and c != 'fin_living_cost_worry'] # Exclude reverse question
        }
        scores = {}
        for name, cols in factors.items():
            # Tính trung bình cộng của toàn bộ câu hỏi trong nhóm
            scores[name] = round(self.df[cols].mean(axis=1).mean(), 2) # Calculate mean per row, then mean of that column
        self.report['factor_scores'] = scores

    def _calculate_nhs(self):
        """C. Net Happiness Score (NHS)"""
        # Promoters (4-5), Detractors (1-2) dựa trên AHS cá nhân
        total = len(self.df)
        promoters = len(self.df[self.df['individual_ahs'] >= 4])
        detractors = len(self.df[self.df['individual_ahs'] <= 2])
        
        nhs = ((promoters - detractors) / total) * 100
        self.report['nhs_percentage'] = round(nhs, 2)

    def _calculate_semester_happiness_curve(self):
        """D. Semester Happiness Curve"""
        if 'dem_semester' in self.df.columns and 'individual_ahs' in self.df.columns:
            semester_happiness = self.df.groupby('dem_semester')['individual_ahs'].mean().sort_index().round(2).to_dict()
            self.report['semester_happiness_curve'] = semester_happiness
        else:
            self.report['semester_happiness_curve'] = "Missing 'dem_semester' or 'individual_ahs' column for analysis."

    def _calculate_gpa_happiness_correlation(self):
        """E. GPA-Happiness Correlation"""
        if 'dem_gpa' in self.df.columns and 'individual_ahs' in self.df.columns:
            gpa_bins = [0, 5.0, 6.5, 8.0, 10.0]
            gpa_labels = ['<5.0', '5.0-6.5', '6.5-8.0', '>8.0']
            self.df['gpa_group'] = pd.cut(self.df['dem_gpa'], bins=gpa_bins, labels=gpa_labels, right=False)
            
            gpa_happiness = self.df.groupby('gpa_group', observed=False)['individual_ahs'].mean().round(2).to_dict()
            self.report['gpa_happiness_correlation'] = gpa_happiness
        else:
            self.report['gpa_happiness_correlation'] = "Missing 'dem_gpa' or 'individual_ahs' column for analysis."
            
    def _calculate_residence_stress_index(self):
        """F. Residence Stress Index"""
        if 'dem_residence' in self.df.columns and 'fin_living_cost_worry' in self.df.columns:
            residence_stress = self.df.groupby('dem_residence')['fin_living_cost_worry'].mean().round(2).to_dict()
            self.report['residence_stress_index'] = residence_stress
        else:
            self.report['residence_stress_index'] = "Missing 'dem_residence' or 'fin_living_cost_worry' column for analysis."

    def _calculate_correlations(self):
        """G. Pearson Correlation (r)"""
        # Tính điểm trung bình từng nhóm X cho mỗi SV để tìm tương quan với Hạnh phúc (Y)
        corr_results = {}
        target = self.df['individual_ahs']
        
        factor_groups = {
            'Academic': [c for c in self.df.columns if c.startswith('aca_')],
            'Environment': [c for c in self.df.columns if c.startswith('env_')],
            'Social': [c for c in self.df.columns if c.startswith('soc_')],
            'Finance': [c for c in self.df.columns if c.startswith('fin_') and c != 'fin_living_cost_worry']
        }
        
        for name, cols in factor_groups.items():
            if not self.df[cols].empty:
                factor_mean = self.df[cols].mean(axis=1)
                r = factor_mean.corr(target)
                corr_results[name] = round(r, 2)
            
        self.report['correlations'] = corr_results

    def _calculate_retention_risk(self):
        """H. Retention Risk Index"""
        # Dựa trên câu hỏi 'hap_loyalty_choice' (Sẽ chọn lại FPoly)
        risk_count = len(self.df[self.df['hap_loyalty_choice'] <= 2])
        self.report['retention_risk_rate'] = round((risk_count / len(self.df)) * 100, 2)

        