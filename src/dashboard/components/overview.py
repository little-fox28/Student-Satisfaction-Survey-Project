import streamlit as st
import pandas as pd
import plotly.express as px

def render_overview(filtered_data):
    """Renders the overview section with KPIs and factor satisfaction."""
    st.header("📊 Chỉ số Hiệu suất Chính")
    
    col1, col2, col3 = st.columns(3)

    total_students = filtered_data.shape[0]

    # Average Happiness Score (AHS)
    avg_ahs = filtered_data["ahs"].mean()
    col1.metric("Mức độ Hài lòng (AHS)", f"{avg_ahs:.2f} / 5.0", delta=f"{avg_ahs-3.5:.2f} so với điểm giữa")

    # Net Happiness Score (NHS)
    promoters = filtered_data[filtered_data["ahs"] >= 4].shape[0]
    detractors = filtered_data[filtered_data["ahs"] <= 2.5].shape[0]
    nhs_percentage = (((promoters - detractors) / total_students) * 100) if total_students > 0 else 0
    col2.metric("Hài lòng Ròng (NHS)", f"{nhs_percentage:.0f}%", help="Người ủng hộ (AHS>=4) - Người phản đối (AHS<=2.5)")

    # Retention Risk
    risk_percentage = ((filtered_data["risk"].sum() / total_students) * 100) if total_students > 0 else 0
    col3.metric("Rủi ro Nghỉ học", f"{risk_percentage:.1f}%", delta=f"{risk_percentage - 10:.1f}% so với mục tiêu", delta_color="inverse")

    st.subheader("Mức độ Hài lòng theo Yếu tố")
    factor_means = pd.DataFrame({
        "Học thuật (ACA)": filtered_data["factors"].apply(lambda x: x["aca"]),
        "Môi trường (ENV)": filtered_data["factors"].apply(lambda x: x["env"]),
        "Xã hội (SOC)": filtered_data["factors"].apply(lambda x: x["soc"]),
        "Tài chính (FIN)": filtered_data["factors"].apply(lambda x: x["fin"]),
    }).mean()

    factor_df = pd.DataFrame({"Factor": factor_means.index, "Score": factor_means.values})
    fig_factors = px.bar(
        factor_df, y="Factor", x="Score", orientation="h",
        color_discrete_sequence=["#f97316"], range_x=[1, 5],
        labels={"Factor": "", "Score": "Điểm Hài lòng Trung bình (1-5)"},
        text=factor_df['Score'].apply(lambda x: f'{x:.2f}')
    )
    fig_factors.update_layout(
        showlegend=False, plot_bgcolor='rgba(0,0,0,0)',
        yaxis={'categoryorder':'total ascending'}
    )
    fig_factors.update_traces(textposition='outside')
    st.plotly_chart(fig_factors, use_container_width=True)
