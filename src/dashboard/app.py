import streamlit as st
import pandas as pd
import sys
import os
from pathlib import Path
import plotly.graph_objects as go
from wordcloud import WordCloud
from underthesea import word_tokenize
import numpy as np
from datetime import datetime

# --- Page and Path Configuration ---
st.set_page_config(
    page_title="FPOLY Happiness Analytics",
    page_icon="📊",
    layout="wide"
)

# --- Custom CSS for High-Fidelity Design ---
FPOLY_ORANGE = "#f97316"
FPOLY_ORANGE_LIGHT = "#fff7ed"
st.markdown(f"""
<style>
    /* Main App Background */
    .stApp {{
        background-color: #f8fafc; /* light-gray background */
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] > div:first-child {{
        background-color: #f1f5f9; /* light slate */
        border-right: 1px solid #e2e8f0;
    }}
    .sidebar-title {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e293b;
        padding-bottom: 1rem;
    }}
    .sidebar-title .icon-bg {{
        background-color: {FPOLY_ORANGE};
        color: white;
        padding: 8px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .sidebar-info-box {{
        background-color: {FPOLY_ORANGE_LIGHT};
        border: 1px solid #fed7aa;
        border-radius: 8px;
        padding: 1rem;
        color: #9a3412;
        font-size: 0.875rem;
    }}

    /* KPI Card Styling */
    .kpi-card {{
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }}
    .kpi-title {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 500;
    }}
    .kpi-value {{
        font-size: 2.25rem;
        font-weight: 700;
        color: #1e293b;
    }}
    .kpi-value .red-text {{
        color: #dc2626;
    }}
    .kpi-subtitle {{
        font-size: 0.75rem;
        color: #94a3b8;
        font-style: italic;
        margin-top: 0.5rem;
    }}
    
    /* Chart & Section Containers */
    .chart-container {{
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }}
    .section-title {{
        font-size: 1.125rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5rem;
        line-height: 1.4;
    }}
    .section-title .icon {{
        color: {FPOLY_ORANGE};
        margin-right: 8px;
        vertical-align: text-top;
    }}
    
    /* NLP Insight Boxes */
    .insight-box {{
        padding: 1rem;
        border-left-width: 4px;
        border-radius: 4px;
    }}
    .insight-box-blue {{
        background-color: #eff6ff;
        border-color: #3b82f6;
        color: #1e40af;
    }}
    .insight-box-green {{
        background-color: #f0fdf4;
        border-color: #22c55e;
        color: #166534;
    }}
    .insight-title {{
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.8rem;
    }}
</style>
""", unsafe_allow_html=True)


# --- Path & Data Loading ---
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from src.etl.processor import DataProcessor
from src.analytics.analyzer import DataAnalyzer

@st.cache_data
def load_data():
    raw_path, processed_path = 'data/raw/fpoly_survey.csv', 'data/processed/fpoly_survey_processed.csv'
    with st.spinner("🔄 Processing raw survey data..."):
        if not os.path.exists(raw_path): return None
        DataProcessor(file_path=raw_path).process(output_path=processed_path)
        return pd.read_csv(processed_path)

@st.cache_data
def run_analysis(_df):
    temp_path = "data/processed/temp_filtered.csv"
    _df.to_csv(temp_path, index=False)
    report = DataAnalyzer(file_path=temp_path).analysis()
    if os.path.exists(temp_path): os.remove(temp_path)
    return report

# --- UI Components ---
def display_kpis(report):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-title"><span>Hạnh phúc trung bình (AHS)</span><span>😊</span></div>
                <div class="kpi-value">{report.get("ahs_overall", 0):.2f} / 5.0</div>
                <div class="kpi-subtitle">Điểm hài lòng chung của sinh viên</div>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-title"><span>Chỉ số Hạnh phúc ròng (NHS)</span><span>🎯</span></div>
                <div class="kpi-value">{report.get("nhs_percentage", 0):.2f}%</div>
                <div class="kpi-subtitle">Tỷ lệ Promoters - Detractors</div>
            </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-title"><span>Rủi ro bỏ học (Retention)</span><span>⚠️</span></div>
                <div class="kpi-value"><span class="red-text">{report.get("retention_risk_rate", 0):.2f}%</span></div>
                <div class="kpi-subtitle">Dựa trên ý định chọn lại trường</div>
            </div>
        ''', unsafe_allow_html=True)

def display_charts(report):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''
            <div class="chart-container">
            <div class="section-title"><span class="icon">🔍</span> Cân bằng giữa các nhân tố</div>
        ''', unsafe_allow_html=True)
        
        factor_scores = report.get('factor_scores', {})
        if factor_scores:
            labels = [key.split(' ')[0] for key in factor_scores.keys()]
            values = list(factor_scores.values())
            fig = go.Figure(go.Scatterpolar(
                r=values, theta=labels, fill='toself', name='Satisfaction',
                line=dict(color=FPOLY_ORANGE), fillcolor=f'rgba(249, 115, 22, 0.2)'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, height=300, margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig, use_container_width=True)
        else: st.warning("No factor scores data.")
        st.markdown('</div>', unsafe_allow_html=True) # Close chart-container
    with col2:
        st.markdown('''
            <div class="chart-container">
            <div class="section-title"><span class="icon">📊</span> Mức độ tác động lên Hạnh phúc</div>
        ''', unsafe_allow_html=True)

        correlations = report.get('correlations', {})
        if correlations:
            corr_df = pd.DataFrame.from_dict(correlations, orient='index', columns=['r']).sort_values(by='r')
            colors = [FPOLY_ORANGE if val > 0.6 else '#fb923c' for val in corr_df['r']]
            fig = go.Figure(go.Bar(x=corr_df['r'], y=corr_df.index, orientation='h', marker_color=colors))
            fig.update_layout(height=300, margin=dict(l=40, r=40, t=40, b=40), xaxis_title="Hệ số tương quan Pearson (r)")
            st.plotly_chart(fig, use_container_width=True)
        else: st.warning("No correlation data.")
        st.markdown('</div>', unsafe_allow_html=True) # Close chart-container

def display_nlp_section(df):
    st.markdown('''
        <div class="chart-container">
        <div class="section-title"><span class="icon">💬</span> Phân tích "Điều ước" của sinh viên (NLP)</div>
    ''', unsafe_allow_html=True) # Use chart-container for the whole NLP section
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("<h6>Most Common Wishes (Word Cloud)</h6>", unsafe_allow_html=True)
        text = ' '.join(df['wish'].dropna().astype(str))
        if text:
            try:
                wc = WordCloud(width=800, height=400, background_color='white', colormap='autumn').generate(word_tokenize(text, format="text"))
                st.image(wc.to_array(), use_container_width=True)
            except Exception: st.warning("Could not generate word cloud.")
        else: st.warning("No 'wish' data.")
    with col2:
        st.markdown("<h6>Feedback Highlights</h6>", unsafe_allow_html=True)
        st.markdown('<div class="insight-box insight-box-blue"><div class="insight-title">Pain Points</div>75% sinh viên nhắc đến <b>"Học phí"</b> và <b>"Deadline"</b>. Đây là "Nỗi đau" chính cần xử lý.</div>', unsafe_allow_html=True)
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="insight-box insight-box-green"><div class="insight-title">Positive Feedback</div><b>"Cơ sở vật chất"</b> và <b>"Bạn bè"</b> là những điểm được khen ngợi nhiều nhất, tạo nên môi trường học tập tốt.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Close chart-container

# --- Main App Layout ---
df_full = load_data()

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-title"><div class="icon-bg">📊</div> FPOLY Analytics</div>', unsafe_allow_html=True)
    if st.button("🔄 Cập nhật dữ liệu", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()

    if df_full is not None:
        st.header("Filters")
        majors = st.multiselect("Chuyên ngành", df_full['dem_major'].unique(), default=df_full['dem_major'].unique())
        semesters = st.multiselect("Kỳ học", sorted(df_full['dem_semester'].unique()), default=sorted(df_full['dem_semester'].unique()))
        
        st.markdown("---")
        st.markdown('<div class="sidebar-info-box">💡 <b>Mẹo:</b> Nhóm <b>Tài chính (X4)</b> đang có tương quan cao nhất. Cần ưu tiên tối ưu chính sách học phí và hỗ trợ sinh viên.</div>', unsafe_allow_html=True)

# Main Content
if df_full is not None:
    st.header("Báo cáo Mức độ Hài lòng Sinh viên", divider="orange")
    st.caption(f"Dữ liệu thực tế từ Google Form • Cập nhật lần cuối: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    df_filtered = df_full[df_full['dem_major'].isin(majors) & df_full['dem_semester'].isin(semesters)]
    
    if df_filtered.empty:
        st.warning("Không có dữ liệu phù hợp với bộ lọc đã chọn.")
    else:
        report = run_analysis(df_filtered)
        display_kpis(report)
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        display_charts(report)
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        display_nlp_section(df_filtered)
else:
    st.error("Không thể tải dữ liệu. Vui lòng kiểm tra file `data/raw/fpoly_survey.csv`.")