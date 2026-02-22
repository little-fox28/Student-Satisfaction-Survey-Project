import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render_analysis(filtered_data, major_options):
    """Renders the AI-driven analysis section with summary and action matrix."""
    st.header("🔍 Trung tâm Phân tích bằng AI")

    st.subheader("✨ Tóm tắt từ AI")
    total_students = filtered_data.shape[0]
    avg_ahs_summary = filtered_data["ahs"].mean()
    pos_pct = round((filtered_data[filtered_data["wishSent"] == "Positive"].shape[0] / total_students) * 100) if total_students > 0 else 0
    major_name = major_options.get(st.session_state.current_major, 'tất cả sinh viên')
    
    ai_summary_text = f"""
    Đối với **{major_name}**, điểm hài lòng trung bình là **{avg_ahs_summary:.2f}/5.0**. 
    Một điểm mạnh chính là **Hoạt động Cộng đồng & Xã hội**, thể hiện qua **{pos_pct}%** phản hồi tích cực. 
    Tuy nhiên, vấn đề chính vẫn là **Áp lực học tập & Deadline**, đặc biệt đối với sinh viên năm 2 và năm cuối. 
    Các vấn đề về tài chính cũng là một nguyên nhân đáng kể gây ra các phản hồi tiêu cực.
    """
    st.markdown(
        f'<div class="ai-summary"><div class="ai-summary-header">💡 Phân tích từ AI</div>{ai_summary_text}</div>',
        unsafe_allow_html=True
    )

    st.subheader("🎯 Ma trận Mức độ Ưu tiên Hành động")
    factor_means = pd.DataFrame({
        "Học thuật (ACA)": filtered_data["factors"].apply(lambda x: x.get("aca")),
        "Môi trường (ENV)": filtered_data["factors"].apply(lambda x: x.get("env")),
        "Xã hội (SOC)": filtered_data["factors"].apply(lambda x: x.get("soc")),
        "Tài chính (FIN)": filtered_data["factors"].apply(lambda x: x.get("fin")),
    }).mean()
    
    factors_matrix = [
        {"name": "Học thuật", "x": factor_means.get('Học thuật (ACA)', 3), "y": 0.65, "color": "#3b82f6"},
        {"name": "Môi trường", "x": factor_means.get('Môi trường (ENV)', 3), "y": 0.25, "color": "#10b981"},
        {"name": "Xã hội", "x": factor_means.get('Xã hội (SOC)', 3), "y": 0.45, "color": "#f59e0b"},
        {"name": "Tài chính", "x": factor_means.get('Tài chính (FIN)', 3), "y": 0.82, "color": "#ef4444"},
    ]
    avg_satisfaction = np.mean([f['x'] for f in factors_matrix])
    avg_impact = np.mean([f['y'] for f in factors_matrix])

    fig_matrix = go.Figure(data=go.Scatter(
        x=[f["x"] for f in factors_matrix], y=[f["y"] for f in factors_matrix],
        text=[f"<b>{f['name']}</b>" for f in factors_matrix], mode="markers+text",
        textposition="bottom center",
        marker=dict(size=30, color=[f["color"] for f in factors_matrix], line=dict(color="white", width=2))
    ))
    fig_matrix.update_layout(
        title="Phân tích Tác động vs. Mức độ Hài lòng",
        xaxis=dict(title="Điểm Hài lòng", range=[1, 5], zeroline=False),
        yaxis=dict(title="Tác động đến AHS (Tương quan)", range=[0, 1], zeroline=False),
        plot_bgcolor='rgba(0,0,0,0)', height=500,
        shapes=[
            dict(type="line", x0=avg_satisfaction, y0=0, x1=avg_satisfaction, y1=1, line=dict(color="grey", width=1, dash="dot")),
            dict(type="line", x0=1, y0=avg_impact, x1=5, y1=avg_impact, line=dict(color="grey", width=1, dash="dot")),
        ]
    )
    # Quadrant annotations
    fig_matrix.add_annotation(x=1.1, y=0.95, text="<b>Tập trung ở đây</b><br>Hài lòng thấp, Tác động cao", showarrow=False, align="left", font=dict(color="#ef4444"))
    fig_matrix.add_annotation(x=4.9, y=0.95, text="<b>Duy trì</b><br>Hài lòng cao, Tác động cao", showarrow=False, align="right", font=dict(color="#10b981"))
    fig_matrix.add_annotation(x=1.1, y=0.05, text="<b>Ưu tiên thấp</b><br>Hài lòng thấp, Tác động thấp", showarrow=False, align="left", font=dict(color="grey"))
    fig_matrix.add_annotation(x=4.9, y=0.05, text="<b>Theo dõi</b><br>Hài lòng cao, Tác động thấp", showarrow=False, align="right", font=dict(color="#3b82f6"))
    st.plotly_chart(fig_matrix, use_container_width=True)
