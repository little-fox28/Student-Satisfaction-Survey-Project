import streamlit as st
from pathlib import Path

_ICON_PATH = Path(__file__).resolve().parent.parent.parent / "assets" / "teamlogo.jpg"

def render_sidebar(reset_filters_callback):
    """Renders the sidebar for the dashboard, including logos, titles, and filters."""
    with st.sidebar:
        if _ICON_PATH.exists():
            st.image(str(_ICON_PATH), width=240)
        st.title("Phân tích Mức độ Hài lòng FPOLY")

        st.subheader("⚙️ Bảng điều khiển")

        # Major Filter
        major_options = {"all": "Tất cả ngành", "IT": "💻 CNTT", "Biz": "📈 Kinh tế", "Design": "🎨 Thiết kế", "Tourism": "✈️ Du lịch"}
        st.radio(
            "**Chuyên ngành**",
            options=list(major_options.keys()),
            format_func=lambda x: major_options[x],
            key="major_radio",
            on_change=lambda: st.session_state.update(current_major=st.session_state.major_radio)
        )

        st.write("") # Spacer

        # Semester Filter
        semester_options = {
            "all": "Tất cả kỳ học",
            "freshman": "Năm 1 (Kỳ 1-3) 🐣",
            "junior": "Năm 2 (Kỳ 4-6) 📚",
            "senior": "Năm cuối (Kỳ 7-9) 🎓",
        }
        st.radio(
            "**Giai đoạn học**",
            options=list(semester_options.keys()),
            format_func=lambda x: semester_options[x],
            key="semester_radio",
            on_change=lambda: st.session_state.update(current_semester=st.session_state.semester_radio)
        )

        st.write("") # Spacer
        st.button("Xoá bộ lọc", on_click=reset_filters_callback, use_container_width=True)

        return major_options, semester_options
