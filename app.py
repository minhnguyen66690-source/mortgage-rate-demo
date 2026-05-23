
import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
PIPELINE_PATH = MODEL_DIR / "final_pipeline.joblib"
CONFIG_PATH = MODEL_DIR / "feature_config.json"

st.set_page_config(
    page_title="Demo dự báo lãi suất khoản vay thế chấp",
    page_icon="📈",
    layout="wide"
)

@st.cache_resource
def load_pipeline():
    return joblib.load(PIPELINE_PATH)

@st.cache_data
def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

st.title("Demo dự báo lãi suất khoản vay thế chấp nhà ở")
st.caption("Ứng dụng minh họa học thuật cho đề tài dự báo lãi suất khoản vay thế chấp")

config = load_config()
pipeline = load_pipeline()

st.markdown("### Thông tin mô hình")
st.write(f"**Mô hình cuối cùng:** {config['best_model']}")
st.write(f"**Đặc tả dữ liệu:** {config['best_specification']}")
st.write("**Biến đầu vào của mô hình:**")
st.write(config["features_used"])

st.markdown("---")
st.markdown("## Nhập thông tin khoản vay")

col1, col2, col3 = st.columns(3)

with col1:
    credit_score = st.number_input("Điểm tín dụng", min_value=300, max_value=850, value=700)
    original_dti_ratio = st.number_input("Tỷ lệ nợ trên thu nhập ban đầu", min_value=0.0, max_value=100.0, value=35.0)
    original_ltv = st.number_input("Tỷ lệ cho vay trên giá trị tài sản", min_value=0.0, max_value=120.0, value=80.0)
    original_cltv = st.number_input("Tỷ lệ cho vay gộp", min_value=0.0, max_value=150.0, value=80.0)
    original_upb = st.number_input("Dư nợ gốc ban đầu", min_value=10000, max_value=5000000, value=250000)

with col2:
    original_loan_term = st.number_input("Kỳ hạn vay ban đầu (tháng)", min_value=12, max_value=480, value=360)
    loan_purpose = st.selectbox("Mục đích vay", ["P", "C", "N"])
    channel = st.selectbox("Kênh phát hành", ["R", "B", "C", "T"])
    property_type = st.selectbox("Loại tài sản", ["SF", "PU", "CO", "MH", "CP"])
    property_state = st.text_input("Bang của tài sản", value="CA")

with col3:
    occupancy_status = st.selectbox("Tình trạng cư trú", ["P", "S", "I"])
    number_of_units = st.number_input("Số đơn vị nhà ở", min_value=1, max_value=4, value=1)
    number_of_borrowers = st.number_input("Số người vay", min_value=1, max_value=4, value=1)
    mi_percentage = st.number_input("Tỷ lệ bảo hiểm thế chấp", min_value=0.0, max_value=60.0, value=0.0)
    super_conforming_flag = st.selectbox("Cờ vượt chuẩn", ["Y", "N"])
    interest_only_indicator = st.selectbox("Cờ chỉ trả lãi", ["Y", "N"])
    property_valuation_method = st.text_input("Phương pháp định giá tài sản", value="A")

if st.button("Dự báo lãi suất"):
    input_data = pd.DataFrame([{
        "credit_score": credit_score,
        "original_dti_ratio": original_dti_ratio,
        "original_ltv": original_ltv,
        "original_cltv": original_cltv,
        "original_upb": original_upb,
        "original_loan_term": original_loan_term,
        "loan_purpose": loan_purpose,
        "channel": channel,
        "property_type": property_type,
        "property_state": property_state.strip().upper(),
        "occupancy_status": occupancy_status,
        "number_of_units": number_of_units,
        "number_of_borrowers": number_of_borrowers,
        "mi_percentage": mi_percentage,
        "super_conforming_flag": super_conforming_flag,
        "interest_only_indicator": interest_only_indicator,
        "property_valuation_method": property_valuation_method.strip().upper(),
    }])

    y_pred = pipeline.predict(input_data)[0]

    st.success(f"Lãi suất dự báo: {y_pred:.4f}%")
    st.markdown("### Dữ liệu đã đưa vào mô hình")
    st.dataframe(input_data, use_container_width=True)

st.markdown("---")
st.info("Đây là ứng dụng minh họa học thuật. Không dùng cho quyết định tín dụng thực tế.")
