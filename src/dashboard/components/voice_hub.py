import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def render_voice_hub(filtered_data):
    """Renders the student voice hub with word cloud, theme chart, and feedback stream."""
    st.header("💬 Diễn đàn Tiếng nói Sinh viên")

    col1_ai, col2_ai = st.columns(2)
    with col1_ai:
        st.subheader("💭 Đám mây 'Điều ước'")
        # Ensure 'wish' column exists and is not empty
        if "wish" in filtered_data and not filtered_data.wish.dropna().empty:
            keywords_data = filtered_data["wish"].str.extractall(r'([A-Za-zÀ-ỹ]+)').iloc[:, 0].value_counts()
            
            # Filter common stopwords and short words
            stopwords = ["và", "là", "có", "để", "cho", "hơn", "em", "mình", "của", "ạ", "rất", "mong", "trường"]
            keywords_data = keywords_data[~keywords_data.index.isin(stopwords)]
            keywords_data = keywords_data[keywords_data.index.str.len() > 2]
            
            keywords_data = keywords_data.head(15) # Limit to top 15 keywords
            
            keywords = []
            if not keywords_data.empty:
                max_size = keywords_data.max()
                color_map = {"Deadline": "#ef4444", "Học phí": "#f59e0b", "Máy lạnh": "#3b82f6", "Giảng viên": "#10b981", "CLB": "#10b981", "LMS": "#ef4444"}
                size_map = {5: "3.5rem", 4: "3rem", 3: "2.5rem", 2: "2rem", 1: "1.5rem"}
                
                for word, count in keywords_data.items():
                    size_level = int(np.ceil(count / max_size * 4)) + 1
                    keywords.append(f"<span style='font-size: {size_map.get(size_level, '1rem')}; color: {color_map.get(word, '#334155')}; font-weight: 700; line-height: 1.2;'>{word}</span>")

            st.markdown(f"<div class='word-cloud'>{''.join(keywords)}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='word-cloud'>Không có điều ước nào để hiển thị.</div>", unsafe_allow_html=True)

    with col2_ai:
        st.subheader("Phân loại Chủ đề bằng AI")
        if "wishCat" in filtered_data and not filtered_data.wishCat.dropna().empty:
            themes_count = filtered_data["wishCat"].value_counts().reset_index()
            themes_count.columns = ["Chủ đề", "Số lượng"]
            fig_themes = px.pie(
                themes_count, values="Số lượng", names="Chủ đề", title="Phân bổ các Chủ đề Phản hồi",
                color_discrete_sequence=px.colors.sequential.Oranges_r
            )
            fig_themes.update_traces(textposition="inside", textinfo="percent+label", marker=dict(line=dict(color='#ffffff', width=2)))
            fig_themes.update_layout(showlegend=False)
            st.plotly_chart(fig_themes, use_container_width=True)
        else:
            st.info("Không có dữ liệu chủ đề để hiển thị.")

    st.subheader("Luồng Phản hồi Trực tiếp")
    search_query = st.text_input("Tìm kiếm trong phản hồi...", placeholder="ví dụ: 'deadline', 'thư viện', ...")
    
    feedback_data = filtered_data[["major", "semester", "wish", "wishSent", "wishCat"]].copy()
    feedback_data["Sinh viên"] = feedback_data["major"] + "/Kỳ " + feedback_data["semester"].astype(str)
    feedback_data.rename(columns={"wish": "Phản hồi", "wishSent": "Sắc thái", "wishCat": "Chủ đề AI"}, inplace=True)
    
    display_cols = ["Sinh viên", "Phản hồi", "Sắc thái", "Chủ đề AI"]

    if search_query:
        feedback_data = feedback_data[feedback_data["Phản hồi"].str.contains(search_query, case=False, na=False)]

    st.dataframe(feedback_data[display_cols], use_container_width=True, height=400)
