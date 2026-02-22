"""Trực quan hóa các biểu đồ phân tích từ dữ liệu khảo sát."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render_charts(chart_data, filtered_data=None):
    """Hiển thị biểu đồ theo luồng storytelling: Tổng quan → Đối tượng → Hành trình → Động lực → Tiếng nói → Phụ lục."""
    if not chart_data:
        st.warning("Không có dữ liệu biểu đồ. Vui lòng kiểm tra dữ liệu đầu vào.")
        return

    # ========== CHƯƠNG 1: BỨC TRANH TỔNG QUAN ==========
    # st.markdown("### 📊 1. Bức tranh tổng quan")
    if 'kpi' in chart_data:
        _render_kpi(chart_data['kpi'])

    # ========== CHƯƠNG 2: AI ĐANG NÓI? – ĐỐI TƯỢNG KHẢO SÁT ==========
    # st.markdown("### 👥 2. Đối tượng khảo sát")
    col1, col2 = st.columns(2)
    with col1:
        if 'major_dist' in chart_data:
            _render_major_dist(chart_data['major_dist'])
    with col2:
        if 'semester_dist' in chart_data:
            _render_semester_dist(chart_data['semester_dist'])
    col3, col4 = st.columns(2)
    with col3:
        if 'gpa_dist' in chart_data:
            _render_gpa_dist(chart_data['gpa_dist'])
    with col4:
        if 'residence_dist' in chart_data:
            _render_residence_dist(chart_data['residence_dist'])

    # ========== CHƯƠNG 3: HÀNH TRÌNH – HẠNH PHÚC THAY ĐỔI THẾ NÀO? ==========
    st.markdown("### 🚀 Hành trình hạnh phúc theo thời gian & thành tích")
    col5, col6 = st.columns(2)
    with col5:
        if 'semester_happiness' in chart_data:
            _render_semester_curve(chart_data['semester_happiness'])
    with col6:
        if 'gpa_happiness' in chart_data:
            _render_gpa_happiness(chart_data['gpa_happiness'])
    if 'gpa_ahs_scatter' in chart_data:
        _render_gpa_ahs_scatter(chart_data['gpa_ahs_scatter'])

    # ========== CHƯƠNG 4: ĐỘNG LỰC – NHÂN TỐ NÀO TÁC ĐỘNG? ==========
    st.markdown("### 🎯 Các nhân tố ảnh hưởng đến hạnh phúc")
    col7, col8 = st.columns(2)
    with col7:
        if 'factor_by_major' in chart_data:
            _render_radar_factors(chart_data['factor_by_major'])
    with col8:
        if 'factor_by_major' in chart_data:
            _render_grouped_bar_factors(chart_data['factor_by_major'])
    if 'correlation_matrix' in chart_data:
        _render_correlation_heatmap(chart_data['correlation_matrix'])

    # ========== CHƯƠNG 5: TIẾNG NÓI – SINH VIÊN ƯỚC MONG GÌ? ==========
    st.markdown("### 💬 Tiếng nói sinh viên – Điều ước & mức độ hài lòng")
    col9, col10 = st.columns(2)
    with col9:
        if 'wish_word_counts' in chart_data:
            _render_word_cloud_bar(chart_data['wish_word_counts'])
    with col10:
        if 'likert_dist' in chart_data:
            _render_likert_stacked(chart_data['likert_dist'])
    # Luồng Phản hồi Trực tiếp – bảng phản hồi chi tiết có tìm kiếm
    if filtered_data is not None:
        _render_feedback_stream(filtered_data)

    # ========== CHƯƠNG 6: PHỤ LỤC – DỮ LIỆU PHẢN HỒI ==========
    st.markdown("### 📅 Xu hướng phản hồi")
    if 'response_trend' in chart_data:
        _render_response_trend(chart_data['response_trend'])


def _render_kpi(kpi):
    # st.subheader("📈 Chỉ số tổng hợp")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("AHS Trung bình", f"{kpi.get('ahs_overall', 0):.2f} / 5.0", help="Điểm hài lòng trung bình")
    with c2:
        st.metric("NHS (%)", f"{kpi.get('nhs_pct', 0):.1f}%", help="Hài lòng ròng = Promoters - Detractors")
    with c3:
        st.metric("Tổng phản hồi", kpi.get('total', 0), help=f"Promoters: {kpi.get('promoters',0)}, Detractors: {kpi.get('detractors',0)}")


def _render_major_dist(data):
    st.subheader("📊 Phân bố theo Chuyên ngành")
    df = pd.DataFrame(list(data.items()), columns=["Ngành", "Số lượng"])
    fig = px.bar(df, x="Ngành", y="Số lượng", color="Số lượng", color_continuous_scale="Blues")
    fig.update_layout(showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)


def _render_semester_dist(data):
    st.subheader("📚 Phân bố theo Kỳ học")
    df = pd.DataFrame(list(data.items()), columns=["Kỳ", "Số lượng"])
    fig = px.bar(df, x="Kỳ", y="Số lượng")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def _render_gpa_dist(data):
    st.subheader("📐 Phân phối GPA")
    df = pd.DataFrame({"GPA": data.get("values", [])})
    if df.empty:
        return
    fig = px.histogram(df, x="GPA", nbins=10, range_x=[4, 10])
    fig.add_vline(x=data.get("mean", 0), line_dash="dash", line_color="red", annotation_text=f"TB: {data.get('mean',0):.2f}")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def _render_residence_dist(data):
    st.subheader("🏠 Phân bố Nơi ở")
    df = pd.DataFrame(list(data.items()), columns=["Nơi ở", "Số lượng"])
    fig = px.pie(df, values="Số lượng", names="Nơi ở")
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)


def _render_radar_factors(factor_by_major):
    st.subheader("🕸️ Radar: Điểm nhân tố theo Ngành")
    df = pd.DataFrame(factor_by_major)
    if df.empty or not all(c in df.columns for c in ['aca', 'env', 'soc', 'fin', 'hap']):
        return
    categories = ['aca', 'env', 'soc', 'fin', 'hap']
    labels = {'aca': 'Học thuật', 'env': 'Môi trường', 'soc': 'Xã hội', 'fin': 'Tài chính', 'hap': 'Hạnh phúc'}
    fig = go.Figure()
    colors = px.colors.qualitative.Set1[: len(df)]
    for i, row in df.iterrows():
        vals = [float(row.get(c) or 0) for c in categories]
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=[labels.get(c, c) for c in categories] + [labels.get(categories[0], categories[0])],
            fill='toself', name=row['major'], line_color=colors[i % len(colors)]
        ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 5])), showlegend=True, height=400)
    st.plotly_chart(fig, use_container_width=True)


def _render_grouped_bar_factors(factor_by_major):
    st.subheader("📊 Điểm nhân tố theo Ngành (Grouped Bar)")
    df = pd.DataFrame(factor_by_major)
    if df.empty:
        return
    df_melt = df.melt(id_vars=['major'], value_vars=['aca', 'env', 'soc', 'fin', 'hap'], var_name='Nhân tố', value_name='Điểm')
    label_map = {'aca': 'Học thuật', 'env': 'Môi trường', 'soc': 'Xã hội', 'fin': 'Tài chính', 'hap': 'Hạnh phúc'}
    df_melt['Nhân tố'] = df_melt['Nhân tố'].map(label_map)
    fig = px.bar(df_melt, x='major', y='Điểm', color='Nhân tố', barmode='group')
    fig.update_layout(xaxis_title="Chuyên ngành", yaxis_range=[1, 5])
    st.plotly_chart(fig, use_container_width=True)


def _render_semester_curve(data):
    st.subheader("📈 Đường cong Hạnh phúc theo Kỳ học")
    df = pd.DataFrame(list(data.items()), columns=["Kỳ", "AHS"])
    fig = px.line(df, x="Kỳ", y="AHS", markers=True)
    fig.update_traces(line=dict(color="#f97316", width=3))
    fig.update_layout(yaxis_range=[1, 5], showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def _render_gpa_happiness(data):
    st.subheader("🔗 GPA vs Hạnh phúc (theo nhóm)")
    df = pd.DataFrame(list(data.items()), columns=["Nhóm GPA", "AHS"])
    fig = px.bar(df, x="Nhóm GPA", y="AHS", color="AHS", color_continuous_scale="Viridis")
    fig.update_layout(yaxis_range=[1, 5], showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def _render_gpa_ahs_scatter(data):
    st.subheader("📉 Phân tán GPA vs Điểm Hạnh phúc")
    df = pd.DataFrame({"GPA": data.get("gpa", []), "AHS": data.get("ahs", [])})
    if df.empty:
        return
    fig = px.scatter(df, x="GPA", y="AHS", trendline="ols")
    fig.update_layout(xaxis_title="GPA", yaxis_title="Điểm Hạnh phúc (AHS)", yaxis_range=[1, 5])
    st.plotly_chart(fig, use_container_width=True)


def _render_correlation_heatmap(data):
    st.subheader("🔥 Heatmap Tương quan")
    cols = data.get("columns", [])
    matrix = data.get("matrix", [])
    if not cols or not matrix:
        return
    fig = go.Figure(data=go.Heatmap(z=matrix, x=cols, y=cols, colorscale="RdBu", zmid=0))
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def _render_response_trend(data):
    df = pd.DataFrame(data)
    if df.empty or 'date' not in df.columns:
        return
    fig = px.line(df, x="date", y="count", markers=True)
    fig.update_layout(xaxis_title="Ngày", yaxis_title="Số phản hồi")
    st.plotly_chart(fig, use_container_width=True)


def _render_word_cloud_bar(data):
    st.subheader("💭 Top từ khóa trong Điều ước")
    if not data:
        return
    df = pd.DataFrame(list(data.items()), columns=["Từ", "Số lần"])
    fig = px.bar(df, x="Từ", y="Số lần")
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def _render_feedback_stream(filtered_data):
    """Luồng Phản hồi Trực tiếp – bảng phản hồi chi tiết có tìm kiếm."""
    if filtered_data.empty or "wish" not in filtered_data.columns:
        return
    st.subheader("Luồng Phản hồi Trực tiếp")
    search_query = st.text_input(
        "Tìm kiếm trong phản hồi...",
        placeholder="ví dụ: 'deadline', 'học phí', 'wifi'...",
        key="feedback_search"
    )
    feedback_data = filtered_data[["major", "semester", "wish", "wishSent", "wishCat"]].copy()
    feedback_data["Sinh viên"] = feedback_data["major"] + " / Kỳ " + feedback_data["semester"].astype(str)
    feedback_data.rename(columns={"wish": "Phản hồi", "wishSent": "Sắc thái", "wishCat": "Chủ đề"}, inplace=True)
    display_cols = ["Sinh viên", "Phản hồi", "Sắc thái", "Chủ đề"]
    if search_query:
        feedback_data = feedback_data[feedback_data["Phản hồi"].str.contains(search_query, case=False, na=False)]
    st.dataframe(feedback_data[display_cols], use_container_width=True, height=400)


def _render_likert_stacked(data):
    st.subheader("📊 Phân phối mức độ Hạnh phúc (Likert)")
    if not data:
        return
    df = pd.DataFrame(data)
    label_map = {1: "Hoàn toàn không đồng ý", 2: "Không đồng ý", 3: "Trung lập", 4: "Đồng ý", 5: "Hoàn toàn đồng ý"}
    df["Mức độ"] = df["level"].map(label_map)
    fig = px.bar(df, x="variable", y="count", color="Mức độ", barmode="stack")
    fig.update_layout(xaxis_title="Chỉ số", yaxis_title="Số lượng")
    st.plotly_chart(fig, use_container_width=True)
