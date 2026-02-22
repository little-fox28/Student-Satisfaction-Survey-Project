import pandas as pd
import numpy as np
from underthesea import word_tokenize
from collections import Counter
import os

import statsmodels.api as sm

# Mapping chuyên ngành tiếng Việt → mã ngắn cho biểu đồ
MAJOR_LABELS = {
    "Ngành Công Nghệ Thông Tin": "CNTT",
    "Thiết kế đồ họa": "Thiết kế",
    "Quản Trị Kinh Doanh & Marketing": "KT-Marketing",
    "Du lịch – Nhà hàng – Khách sạn": "Du lịch",
    "Logistics & Y tế": "Logistics",
    "Công nghệ kỹ thuật – Cơ khí – Điện tử": "Cơ khí-Điện tử",
    "Khác": "Khác",
    "Ngôn ngữ": "Ngôn ngữ",
}


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

    # ==================== CHART DATA COMPUTATION ====================
    def get_chart_data(self, df=None):
        """
        Tính toán dữ liệu sẵn sàng cho biểu đồ.
        Nếu df=None thì dùng self.df (đã load từ file).
        Trả về dict với các key: major_dist, semester_dist, gpa_dist, residence_dist,
        factor_by_major, semester_happiness, gpa_happiness, correlation_matrix,
        response_trend, wish_word_counts, likert_dist.
        """
        data = df if df is not None else self.df
        if data.empty:
            return {}

        out = {}
        hap_cols = [c for c in data.columns if c.startswith('hap_')]
        aca_cols = [c for c in data.columns if c.startswith('aca_')]
        env_cols = [c for c in data.columns if c.startswith('env_')]
        soc_cols = [c for c in data.columns if c.startswith('soc_')]
        fin_cols = [c for c in data.columns if c.startswith('fin_')]
        factor_cols = {'aca': aca_cols, 'env': env_cols, 'soc': soc_cols, 'fin': fin_cols, 'hap': hap_cols}

        # 1. Phân bố theo ngành
        if 'dem_major' in data.columns:
            major_counts = data['dem_major'].value_counts()
            out['major_dist'] = {MAJOR_LABELS.get(k, k): int(v) for k, v in major_counts.items()}

        # 2. Phân bố theo kỳ học
        if 'dem_semester' in data.columns:
            sem_counts = data['dem_semester'].value_counts().sort_index()
            out['semester_dist'] = {int(k): int(v) for k, v in sem_counts.items()}

        # 3. Phân phối GPA (bins cho histogram)
        if 'dem_gpa' in data.columns:
            gpa = data['dem_gpa'].dropna()
            out['gpa_dist'] = {
                'values': gpa.tolist(),
                'bins': [4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
                'mean': float(gpa.mean()),
            }

        # 4. Phân bố nơi ở
        if 'dem_residence' in data.columns:
            res_counts = data['dem_residence'].value_counts()
            out['residence_dist'] = res_counts.to_dict()

        # 5. Điểm các nhân tố theo ngành
        if 'dem_major' in data.columns and factor_cols['aca']:
            individual_ahs = data[hap_cols].mean(axis=1) if hap_cols else None
            factor_by_major = []
            for maj in data['dem_major'].unique():
                subset = data[data['dem_major'] == maj]
                def safe_mean(cols):
                    if not cols: return None
                    v = subset[cols].mean().mean()
                    return None if pd.isna(v) else round(float(v), 2)

                row = {
                    'major': MAJOR_LABELS.get(maj, maj),
                    'aca': safe_mean(aca_cols),
                    'env': safe_mean(env_cols),
                    'soc': safe_mean(soc_cols),
                    'fin': safe_mean(fin_cols),
                    'hap': safe_mean(hap_cols),
                    'count': int(len(subset)),
                }
                factor_by_major.append(row)
            out['factor_by_major'] = factor_by_major

        # 6. Đường cong hạnh phúc theo kỳ
        if 'dem_semester' in data.columns and hap_cols:
            data_copy = data.copy()
            data_copy['_ahs'] = data_copy[hap_cols].mean(axis=1)
            curve = data_copy.groupby('dem_semester')['_ahs'].mean().sort_index()
            out['semester_happiness'] = {int(k): round(float(v), 2) for k, v in curve.items()}

        # 7. Tương quan GPA - Hạnh phúc
        if 'dem_gpa' in data.columns and hap_cols:
            data_copy = data.copy()
            data_copy['_ahs'] = data_copy[hap_cols].mean(axis=1)
            gpa_bins = [0, 5.0, 6.5, 8.0, 10.0]
            gpa_labels = ['<5.0', '5.0-6.5', '6.5-8.0', '>8.0']
            data_copy['_gpa_group'] = pd.cut(
                data_copy['dem_gpa'], bins=gpa_bins, labels=gpa_labels, right=False
            )
            gpa_hap = data_copy.groupby('_gpa_group', observed=False)['_ahs'].mean()
            out['gpa_happiness'] = {str(k): round(float(v), 2) for k, v in gpa_hap.items()}
            out['gpa_ahs_scatter'] = {
                'gpa': data_copy['dem_gpa'].tolist(),
                'ahs': data_copy['_ahs'].tolist(),
            }

        # 8. Ma trận tương quan
        if hap_cols:
            data_copy = data.copy()
            data_copy['ahs'] = data_copy[hap_cols].mean(axis=1)
            num_cols = aca_cols + env_cols + soc_cols + fin_cols + ['ahs']
            num_cols = [c for c in num_cols if c in data_copy.columns]
            if num_cols:
                corr = data_copy[num_cols].corr()
                out['correlation_matrix'] = {
                    'columns': list(corr.columns),
                    'matrix': corr.values.tolist(),
                }

        # 9. Xu hướng phản hồi theo thời gian
        if 'timestamp' in data.columns:
            data_copy = data.copy()
            data_copy['timestamp'] = pd.to_datetime(data_copy['timestamp'], errors='coerce')
            data_copy = data_copy.dropna(subset=['timestamp'])
            if not data_copy.empty:
                data_copy['_date'] = data_copy['timestamp'].dt.date
                trend = data_copy.groupby('_date').size().reset_index(name='count')
                trend['date'] = trend['_date'].astype(str)
                out['response_trend'] = trend[['date', 'count']].to_dict('records')

        # 10. Word cloud từ điều ước
        if 'wish' in data.columns:
            text = ' '.join(data['wish'].dropna().astype(str))
            if text.strip():
                tokens = word_tokenize(text.lower())
                filtered = [t for t in tokens if t.isalpha() and t not in self.stopwords and len(t) > 2]
                wc = Counter(filtered)
                out['wish_word_counts'] = dict(wc.most_common(20))

        # 11. Phân phối mức độ Likert (hap)
        if hap_cols:
            likert_data = []
            for col in hap_cols:
                for val, cnt in data[col].value_counts().sort_index().items():
                    likert_data.append({'variable': col.replace('hap_', ''), 'level': int(val), 'count': int(cnt)})
            out['likert_dist'] = likert_data

        # 12. KPI tổng hợp
        if hap_cols:
            ahs_all = data[hap_cols].mean(axis=1)
            promoters = int((ahs_all >= 4).sum())
            detractors = int((ahs_all <= 2).sum())
            total = len(data)
            out['kpi'] = {
                'ahs_overall': round(float(ahs_all.mean()), 2),
                'nhs_pct': round((promoters - detractors) / total * 100, 1) if total > 0 else 0,
                'total': total,
                'promoters': promoters,
                'detractors': detractors,
            }

        return out

        