import streamlit as st
import pandas as pd
import plotly.express as px

def render_journey(filtered_data, semesters):
    """Renders the student journey section with trend and radar charts."""
    st.header("🚀 Hành trình Trải nghiệm Sinh viên")
    col1, col2 = st.columns([0.55, 0.45])

    with col1:
        st.subheader("Xu hướng qua các Kỳ học")
        semester_trend = filtered_data.groupby("semester")["ahs"].mean().reindex(semesters)
        fig_trend = px.line(
            semester_trend, labels={"index": "Kỳ học", "value": "AHS"},
            title="Điểm Hài lòng Trung bình (AHS) qua các Kỳ học"
        )
        fig_trend.update_traces(mode="lines+markers", marker=dict(size=10), line=dict(color="#f97316", width=3))
        fig_trend.update_layout(
            yaxis_range=[max(2, semester_trend.min() - 0.5 if not semester_trend.empty else 2), min(5, semester_trend.max() + 0.5 if not semester_trend.empty else 5)],
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col2:
        st.subheader("Biểu đồ Radar theo Chuyên ngành")
        factors_df = pd.json_normalize(filtered_data['factors'])
        factors_df['major'] = filtered_data['major']
        radar_data = factors_df.groupby('major')[['aca', 'env', 'soc', 'fin']].mean().reset_index()
        radar_data_melted = radar_data.melt(id_vars='major', value_name='Score', var_name='variable')
        factor_labels = {'aca': 'Học thuật', 'env': 'Môi trường', 'soc': 'Xã hội', 'fin': 'Tài chính'}
        radar_data_melted['variable'] = radar_data_melted['variable'].map(factor_labels)

        fig_radar = px.line_polar(
            radar_data_melted, r="Score", theta="variable", color="major", line_close=True,
            range_r=[2.5, 5], title="Phân tích So sánh các Yếu tố",
            color_discrete_map={"IT": "#3b82f6", "Biz": "#f97316", "Design": "#10b981", "Tourism": "#ef4444"},
        )
        fig_radar.update_traces(fill='toself', opacity=0.7)
        st.plotly_chart(fig_radar, use_container_width=True)
