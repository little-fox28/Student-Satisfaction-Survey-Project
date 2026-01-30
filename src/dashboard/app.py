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

# --- Constants ---
FPOLY_ORANGE = "#f97316"

# --- Asset Loading ---
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("src/dashboard/style.css")


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
                <div class="kpi-value">
                    {report.get("ahs_overall", 0):.2f} / 5.0
                </div>
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
        with st.container(border=True):
            st.markdown('<div class="section-title"><span class="icon">🔍</span> Cân bằng giữa các nhân tố</div>', unsafe_allow_html=True)
            factor_scores = report.get('factor_scores', {})
            if factor_scores:
                labels = [key.split(' ')[0] for key in factor_scores.keys()]
                values = list(factor_scores.values())
                fig = go.Figure(go.Scatterpolar(
                    r=values, theta=labels, fill='toself', name='Satisfaction',
                    line=dict(color=FPOLY_ORANGE), fillcolor=f'rgba(249, 115, 22, 0.2)'
                ))
                fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, height=300, margin=dict(l=40, r=40, t=40, b=40), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            else: st.warning("No factor scores data.")

    with col2:
        with st.container(border=True):
            st.markdown('<div class="section-title"><span class="icon">📊</span> Mức độ tác động lên Hạnh phúc</div>', unsafe_allow_html=True)
            correlations = report.get('correlations', {})
            if correlations:
                corr_df = pd.DataFrame.from_dict(correlations, orient='index', columns=['r']).sort_values(by='r')
                colors = [FPOLY_ORANGE if val > 0.6 else '#fb923c' for val in corr_df['r']]
                fig = go.Figure(go.Bar(x=corr_df['r'], y=corr_df.index, orientation='h', marker_color=colors))
                fig.update_layout(height=300, margin=dict(l=40, r=40, t=40, b=40), xaxis_title="Hệ số tương quan Pearson (r)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            else: st.warning("No correlation data.")

def display_nlp_section(df, report):
    with st.container(border=True):
        st.markdown('<div class="section-title"><span class="icon">💬</span> Phân tích "Điều ước" của sinh viên (NLP)</div>', unsafe_allow_html=True)

        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.markdown("<h6>Most Common Wishes (Word Cloud)</h6>", unsafe_allow_html=True)
            text = ' '.join(df['wish'].dropna().astype(str))
            if text:
                try:
                    # Make wordcloud background transparent to inherit container color
                    wc = WordCloud(width=800, height=400, background_color=None, mode='RGBA', colormap='autumn').generate(word_tokenize(text, format="text"))
                    st.image(wc.to_array(), use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not generate word cloud: {e}")
            else:
                st.info("Không có dữ liệu 'điều ước' để phân tích.")
        with col2:
            st.markdown("<h6>Chủ đề được quan tâm hàng đầu</h6>", unsafe_allow_html=True)
            top_wishes = report.get('wish_analysis', {})
            if top_wishes:
                # Display top keywords in a formatted way
                html = '<div class="insight-box insight-box-blue"><div class="insight-title">Top Keywords</div><ul>'
                for word, count in top_wishes.items():
                    html += f"<li><b>{word.capitalize()}</b>: {count} lượt</li>"
                html += "</ul></div>"
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.info("Không có từ khóa nổi bật nào được tìm thấy.")

# --- Main App Layout ---
df_full = load_data()

# Use a container for the main content
main_container = st.container()

# Sidebar MUST be defined before the main content that depends on its filters
with st.sidebar:
    st.markdown('<div class="sidebar-title"><div class="icon-bg">📊</div> FPOLY Analytics</div>', unsafe_allow_html=True)
    if st.button("🔄 Cập nhật dữ liệu", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()

    # --- Filters ---
    if df_full is not None:
        st.header("Filters")
        # These widgets are the single source of truth for filtering
        majors = st.multiselect("Chuyên ngành", df_full['dem_major'].unique(), default=df_full['dem_major'].unique())
        semesters = st.multiselect("Kỳ học", sorted(df_full['dem_semester'].unique()), default=sorted(df_full['dem_semester'].unique()))
    else:
        # Create empty placeholders if data loading fails
        majors = []
        semesters = []

# --- Data Filtering and Analysis ---
if df_full is not None:
    df_filtered = df_full[df_full['dem_major'].isin(majors) & df_full['dem_semester'].isin(semesters)]
    
    if not df_filtered.empty:
        # Run analysis on the filtered data
        report = run_analysis(df_filtered)
    else:
        # Create an empty report if there's no data
        report = {}
else:
    df_filtered = pd.DataFrame()
    report = {}

# --- Dynamic Sidebar Content (after analysis) ---
with st.sidebar:
    st.markdown("---")
    top_factor = report.get('top_correlated_factor')
    if top_factor:
        tip_message = f'''<div class="sidebar-info-box">💡 <b>Mẹo:</b> Nhóm <b>{top_factor}</b> đang có tương quan cao nhất tới mức độ hạnh phúc. Cần ưu tiên phân tích và tối ưu các yếu tố trong nhóm này.</div>'''
    else:
        tip_message = '''<div class="sidebar-info-box">💡 <b>Mẹo:</b> Chọn bộ lọc để xem phân tích chi tiết hoặc khi có đủ dữ liệu.</div>'''
    st.markdown(tip_message, unsafe_allow_html=True)


# --- Main Content Display ---
with main_container:
    if df_full is not None:
        st.header("Báo cáo Mức độ Hài lòng Sinh viên", divider="orange")
        st.caption(f"Dữ liệu thực tế từ Google Form • Cập nhật lần cuối: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        if df_filtered.empty:
            st.warning("Không có dữ liệu phù hợp với bộ lọc đã chọn.")
        else:
            display_kpis(report)
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            display_charts(report)
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            display_nlp_section(df_filtered, report)
    else:
        st.error("Không thể tải dữ liệu. Vui lòng kiểm tra file `data/raw/fpoly_survey.csv`.")