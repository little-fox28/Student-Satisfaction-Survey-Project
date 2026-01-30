import pandas as pd
from underthesea import word_tokenize
from collections import Counter
import os

class DataAnalyzer:
    def __init__(self, file_path: str):
        """
        Khởi tạo với DataFrame đã qua xử lý ETL (sạch và đã đảo điểm).
        """
        self.df = pd.DataFrame(pd.read_csv(file_path))
        self.report = {}
        self.stopwords = self._load_stopwords()

    def _load_stopwords(self):
        """Loads Vietnamese stopwords from a file."""
        # Correctly resolve path relative to this script's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        stopwords_path = os.path.join(current_dir, 'vietnamese_stopwords.txt')
        if os.path.exists(stopwords_path):
            with open(stopwords_path, 'r', encoding='utf-8') as f:
                return set(f.read().splitlines())
        return set()

    def analysis(self):
        """
        Method chính thực hiện toàn bộ các hướng phân tích chiến lược.
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
        self._analyze_wishes()                          # I. Phân tích điều ước (NLP)
        
        print("✅ Phân tích hoàn tất.")
        return self.report

    def _calculate_ahs(self):
        """A. Average Happiness Score (AHS)"""
        hap_cols = [c for c in self.df.columns if c.startswith('hap_')]
        if not hap_cols: return
        self.df['individual_ahs'] = self.df[hap_cols].mean(axis=1)
        self.report['ahs_overall'] = round(self.df['individual_ahs'].mean(), 2)

    def _calculate_factor_scores(self):
        """B. Factor Satisfaction Score"""
        factors = {
            'Academic (X1)': [c for c in self.df.columns if c.startswith('aca_')],
            'Environment (X2)': [c for c in self.df.columns if c.startswith('env_')],
            'Social (X3)': [c for c in self.df.columns if c.startswith('soc_')],
            'Finance (X4)': [c for c in self.df.columns if c.startswith('fin_') and c != 'fin_living_cost_worry']
        }
        scores = {}
        for name, cols in factors.items():
            if cols:
                scores[name] = round(self.df[cols].mean(axis=1).mean(), 2)
        self.report['factor_scores'] = scores

    def _calculate_nhs(self):
        """C. Net Happiness Score (NHS)"""
        if 'individual_ahs' not in self.df.columns: return
        total = len(self.df)
        if total == 0: return
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
            self.report['semester_happiness_curve'] = {}

    def _calculate_gpa_happiness_correlation(self):
        """E. GPA-Happiness Correlation"""
        if 'dem_gpa' in self.df.columns and 'individual_ahs' in self.df.columns:
            gpa_bins = [0, 5.0, 6.5, 8.0, 10.0]
            gpa_labels = ['<5.0', '5.0-6.5', '6.5-8.0', '>8.0']
            self.df['gpa_group'] = pd.cut(self.df['dem_gpa'], bins=gpa_bins, labels=gpa_labels, right=False)
            
            gpa_happiness = self.df.groupby('gpa_group', observed=False)['individual_ahs'].mean().round(2).to_dict()
            self.report['gpa_happiness_correlation'] = gpa_happiness
        else:
            self.report['gpa_happiness_correlation'] = {}
            
    def _calculate_residence_stress_index(self):
        """F. Residence Stress Index"""
        if 'dem_residence' in self.df.columns and 'fin_living_cost_worry' in self.df.columns:
            residence_stress = self.df.groupby('dem_residence')['fin_living_cost_worry'].mean().round(2).to_dict()
            self.report['residence_stress_index'] = residence_stress
        else:
            self.report['residence_stress_index'] = {}

    def _calculate_correlations(self):
        """G. Pearson Correlation (r) and Top Correlated Factor"""
        if 'individual_ahs' not in self.df.columns: 
            self.report['correlations'] = {}
            self.report['top_correlated_factor'] = None
            return

        corr_results = {}
        target = self.df['individual_ahs']
        
        factor_groups = {
            'Academic': [c for c in self.df.columns if c.startswith('aca_')],
            'Environment': [c for c in self.df.columns if c.startswith('env_')],
            'Social': [c for c in self.df.columns if c.startswith('soc_')],
            'Finance': [c for c in self.df.columns if c.startswith('fin_') and c != 'fin_living_cost_worry']
        }
        
        for name, cols in factor_groups.items():
            if cols and not self.df[cols].empty:
                factor_mean = self.df[cols].mean(axis=1)
                r = factor_mean.corr(target)
                corr_results[name] = round(r, 2)
        
        self.report['correlations'] = corr_results
        
        if corr_results:
            top_factor = max(corr_results, key=corr_results.get)
            self.report['top_correlated_factor'] = top_factor
        else:
            self.report['top_correlated_factor'] = None

    def _calculate_retention_risk(self):
        """H. Retention Risk Index"""
        if 'hap_loyalty_choice' not in self.df.columns or len(self.df) == 0:
            self.report['retention_risk_rate'] = 0
            return
            
        risk_count = len(self.df[self.df['hap_loyalty_choice'] <= 2])
        self.report['retention_risk_rate'] = round((risk_count / len(self.df)) * 100, 2)

    def _analyze_wishes(self):
        """I. Analyze student wishes using NLP."""
        if 'wish' not in self.df.columns:
            self.report['wish_analysis'] = {}
            return

        text = ' '.join(self.df['wish'].dropna().astype(str))
        if not text.strip():
            self.report['wish_analysis'] = {}
            return

        tokens = word_tokenize(text.lower())
        
        # Filter out stopwords and non-alpha words
        filtered_tokens = [token for token in tokens if token.isalpha() and token not in self.stopwords]
        
        word_counts = Counter(filtered_tokens)
        
        # Get top 5 most common keywords
        self.report['wish_analysis'] = dict(word_counts.most_common(5))

        