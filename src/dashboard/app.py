import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path


_APP_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _APP_DIR.parent.parent
_DATA_PATH = _PROJECT_ROOT / "data" / "processed" / "fpoly_survey_processed.csv"
_CSS_PATH = _APP_DIR / "style.css"
_ICON_PATH = _APP_DIR.parent / "assets" / "teamlogo.jpg"

# Add project root for imports
import sys
sys.path.insert(0, str(_PROJECT_ROOT))

# Import components
from components.sidebar import render_sidebar
from components.charts import render_charts
from src.analytics.analyzer import DataAnalyzer

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="BLOSSOM TEAM",
    page_icon=str(_ICON_PATH) if _ICON_PATH.exists() else None,
    layout="wide",
    initial_sidebar_state="auto"
)

# --- STYLING ---
def load_css(css_path):
    """Loads a CSS file and injects it into the Streamlit app."""
    try:
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {css_path}")

load_css(_CSS_PATH)


# --- DATA & FILTERS ---
# Constants
MAJORS = {
    "IT": "Công nghệ thông tin",
    "Biz": "Kinh tế & Marketing",
    "Design": "Thiết kế đồ họa",
    "Tourism": "Du lịch – Nhà hàng – Khách sạn",
}
SEMESTERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
TEXT_WISHES = [
    {"t": "Trường cần siết chặt hơn về đánh giá năng lực để cho điểm phù hợp.", "c": "Academic", "s": "Neutral"},
    {"t": "Có nhiều cuộc thi hơn cho ngành CNTT để sinh viên thử sức với dự án thực tế.", "c": "Academic", "s": "Positive"},
    {"t": "Ước gì học phí ít hơn.", "c": "Finance", "s": "Negative"},
    {"t": "Lịch học bất tiện, khó chọn lớp vào giờ cao điểm, mong trường khắc phục.", "c": "Academic", "s": "Negative"},
    {"t": "Mong có nhiều buổi thực hành tại doanh nghiệp và đi tour thực tế hơn.", "c": "Academic", "s": "Positive"},
    {"t": "Cải thiện cơ sở vật chất, chất lượng giảng dạy và môi trường học tập.", "c": "Environment", "s": "Positive"},
    {"t": "Wifi cần mạnh hơn và nên có thêm máy lọc nước cho sinh viên.", "c": "Environment", "s": "Negative"},
    {"t": "Giảm deadline để sinh viên bớt áp lực.", "c": "Academic", "s": "Negative"},
    {"t": "Tổ chức nhiều hoạt động tập thể và phát triển các câu lạc bộ.", "c": "Social", "s": "Positive"},
    {"t": "Giảm học phí hoặc có nhiều chương trình học bổng hơn cho sinh viên.", "c": "Finance", "s": "Positive"},
]

def main():
    """Main function to run the Streamlit dashboard."""
    if not _DATA_PATH.exists():
        st.error(f"Data file not found: {_DATA_PATH}. Run the ETL pipeline in main.ipynb first.")
        return

    # Mapping chuyên ngành (dùng chung cho filter và chart)
    major_mapping = {
        "Ngành Công Nghệ Thông Tin": "IT",
        "Thiết kế đồ họa": "Design",
        "Quản Trị Kinh Doanh & Marketing": "Biz",
        "Du lịch – Nhà hàng – Khách sạn": "Tourism",
        "Logistics & Y tế": "Biz",
        "Công nghệ kỹ thuật – Cơ khí – Điện tử": "IT",
        "Khác": "Biz",
        "Ngôn ngữ": "Biz",
    }

    # Load raw data CHO BIỂU ĐỒ (giữ nguyên cột gốc: dem_major, hap_*, aca_*, timestamp...)
    raw_for_charts = pd.read_csv(_DATA_PATH)
    raw_for_charts["major_key"] = raw_for_charts["dem_major"].map(major_mapping).fillna("IT")
    raw_for_charts["semester_num"] = pd.to_numeric(raw_for_charts["dem_semester"], errors="coerce")
    raw_for_charts = raw_for_charts.dropna(subset=["semester_num"])
    raw_for_charts["semester_num"] = raw_for_charts["semester_num"].astype(int)

    raw_data = pd.read_csv(_DATA_PATH)

    # Data Transformations (cho các component hiện tại)
    raw_data.rename(columns={
        "dem_major": "major",
        "dem_semester": "semester",
        "dem_gpa": "ahs",
        "wish": "wish_text" # Rename original wish to wish_text to avoid conflict
    }, inplace=True)

    raw_data["major"] = raw_data["major"].map(major_mapping).fillna("IT")

    # Convert semester to numeric, coercing errors to NaN
    raw_data['semester'] = pd.to_numeric(raw_data['semester'], errors='coerce')
    # Drop rows where semester is NaN after conversion
    raw_data.dropna(subset=['semester'], inplace=True)
    raw_data['semester'] = raw_data['semester'].astype(int)

    # Create 'factors' dictionary column
    def calculate_factors(row):
        aca_cols = ["aca_curriculum_fit", "aca_deadline_pressure", "aca_teaching_quality", "aca_lms_stability"]
        env_cols = ["env_facilities", "env_utilities", "env_dynamic_culture"]
        soc_cols = ["soc_friendship_support", "soc_activity_integration", "soc_family_support"]
        fin_cols = ["fin_tuition_value", "fin_living_cost_worry", "fin_job_prospects"]
        hap_cols = ["hap_general_satisfaction", "hap_school_energy", "hap_meaningful_life", "hap_loyalty_choice"]

        factors_dict = {
            "aca": row[aca_cols].mean(),
            "env": row[env_cols].mean(),
            "soc": row[soc_cols].mean(),
            "fin": row[fin_cols].mean(),
            "hap": row[hap_cols].mean(),
        }
        return factors_dict

    raw_data["factors"] = raw_data.apply(calculate_factors, axis=1)

    # Create 'risk' column (randomly for now)
    raw_data["risk"] = np.random.choice([0, 1], size=len(raw_data), p=[0.88, 0.12])

    # Create 'wish' (text), 'wishCat', and 'wishSent' columns
    # Assign 'wish_text' to 'wish' and randomly assign 'wishCat' and 'wishSent' from TEXT_WISHES
    raw_data["wish"] = raw_data["wish_text"]
    raw_data.drop(columns=["wish_text"], inplace=True) # Drop the temporary column

    # Fill NaN values in 'wish' with an empty string to avoid errors with choices
    raw_data['wish'].fillna('', inplace=True)

    # Ensure all TEXT_WISHES categories are covered, or add a default
    if not TEXT_WISHES:
        st.error("TEXT_WISHES constant is empty. Cannot assign wish categories.")
        # Provide a fallback if TEXT_WISHES is empty
        raw_data["wishCat"] = "Unknown"
        raw_data["wishSent"] = "Neutral"
    else:
        wish_choices = [(w["c"], w["s"]) for w in TEXT_WISHES]
        # Use a more robust way to assign wishCat and wishSent
        # For now, let's randomly assign or map them if a pattern is found
        # Given the original TEXT_WISHES is a fixed list, let's just make it random for now
        # until actual sentiment analysis or categorization is implemented.
        random_choices = np.random.choice(len(wish_choices), size=len(raw_data))
        raw_data["wishCat"] = [wish_choices[i][0] for i in random_choices]
        raw_data["wishSent"] = [wish_choices[i][1] for i in random_choices]

    # Drop original columns that are now aggregated into 'factors' or are no longer needed
    columns_to_drop = [
        "timestamp", "dem_residence",
        "hap_general_satisfaction", "hap_school_energy", "hap_meaningful_life", "hap_loyalty_choice",
        "aca_curriculum_fit", "aca_deadline_pressure", "aca_teaching_quality", "aca_lms_stability",
        "env_facilities", "env_utilities", "env_dynamic_culture",
        "soc_friendship_support", "soc_activity_integration", "soc_family_support",
        "fin_tuition_value", "fin_living_cost_worry", "fin_job_prospects"
    ]
    raw_data.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    # Initialize session state for filters
    if "current_major" not in st.session_state:
        st.session_state.current_major = "all"
    if "current_semester" not in st.session_state:
        st.session_state.current_semester = "all"
    if "current_semester" not in st.session_state:
        st.session_state.current_semester = "all"

    def reset_filters():
        st.session_state.current_major = "all"
        st.session_state.current_semester = "all"

    def filter_data(data):
        df = data.copy()
        if st.session_state.current_major != "all":
            df = df[df["major"] == st.session_state.current_major]
        
        semester_map = {
            "freshman": (df["semester"] <= 3),
            "junior": (df["semester"] >= 4) & (df["semester"] <= 6),
            "senior": (df["semester"] >= 7)
        }
        if st.session_state.current_semester in semester_map:
            df = df[semester_map[st.session_state.current_semester]]
        
        return df

    def filter_raw_for_charts(data):
        """Áp dụng cùng bộ lọc cho dữ liệu raw (có major_key, semester_num)."""
        df = data.copy()
        if st.session_state.current_major != "all":
            df = df[df["major_key"] == st.session_state.current_major]
        semester_map = {
            "freshman": (df["semester_num"] <= 3),
            "junior": (df["semester_num"] >= 4) & (df["semester_num"] <= 6),
            "senior": (df["semester_num"] >= 7),
        }
        if st.session_state.current_semester in semester_map:
            df = df[semester_map[st.session_state.current_semester]]
        return df

    # --- Render App ---
    render_sidebar(reset_filters)
    filtered_data = filter_data(raw_data)
    filtered_raw_for_charts = filter_raw_for_charts(raw_for_charts)

    if not filtered_data.empty:
        st.header("📈 Biểu đồ Phân tích Chi tiết")
        analyzer = DataAnalyzer(str(_DATA_PATH))
        chart_data = analyzer.get_chart_data(df=filtered_raw_for_charts)
        render_charts(chart_data, filtered_data=filtered_data)
    else:
        st.warning("Không có dữ liệu cho bộ lọc đã chọn. Vui lòng thử lại.")

if __name__ == "__main__":
    main()
