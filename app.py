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
    layout="wide",
)

@st.cache_resource
def load_pipeline():
    return joblib.load(PIPELINE_PATH)

@st.cache_data
def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()
pipeline = load_pipeline()

st.title("Demo dự báo lãi suất khoản vay thế chấp nhà ở")

st.markdown("### Giới thiệu")
st.write(
    "Ứng dụng này minh họa mô hình dự báo lãi suất khoản vay thế chấp nhà ở "
    "được xây dựng từ dữ liệu Freddie Mac. "
    "Bạn chỉ cần nhập các thông tin cơ bản của khoản vay. "
    "Các thông tin nâng cao có thể giữ mặc định nếu chưa rõ."
)

st.markdown("### Thông tin mô hình")
st.write(f"**Mô hình cuối cùng:** {config.get('best_model', 'CatBoost')}")
st.write(f"**Đặc tả dữ liệu:** {config.get('best_specification', 'A_loan_only')}")

st.markdown("---")
st.markdown("## 1. Thông tin cơ bản")

c1, c2 = st.columns(2)

with c1:
    credit_score = st.number_input(
        "Điểm tín dụng",
        min_value=300,
        max_value=850,
        value=700,
        help="Điểm phản ánh mức độ uy tín tín dụng của người vay. Điểm càng cao thường càng có lợi.",
    )

    original_dti_ratio = st.number_input(
        "Tỷ lệ nợ trên thu nhập ban đầu (%)",
        min_value=0.0,
        max_value=100.0,
        value=35.0,
        help="Tỷ lệ giữa tổng nghĩa vụ nợ và thu nhập của người vay tại thời điểm vay.",
    )

    original_ltv = st.number_input(
        "Tỷ lệ cho vay trên giá trị tài sản (%)",
        min_value=0.0,
        max_value=120.0,
        value=80.0,
        help="Ví dụ tài sản trị giá 100 thì vay 80, khi đó tỷ lệ này là 80%.",
    )

with c2:
    original_upb = st.number_input(
        "Dư nợ gốc ban đầu",
        min_value=10000,
        max_value=5000000,
        value=250000,
        help="Số tiền vay ban đầu.",
    )

    original_loan_term = st.number_input(
        "Kỳ hạn vay ban đầu (tháng)",
        min_value=12,
        max_value=480,
        value=360,
        help="Ví dụ 360 tháng tương đương 30 năm.",
    )

    loan_purpose_display = st.selectbox(
        "Mục đích vay",
        ["Mua nhà", "Tái cấp vốn", "Khác"],
        help="Chọn mục đích chính của khoản vay.",
    )

loan_purpose_map = {
    "Mua nhà": "P",
    "Tái cấp vốn": "C",
    "Khác": "N",
}
loan_purpose = loan_purpose_map[loan_purpose_display]

with st.expander("2. Thông tin nâng cao (có thể giữ mặc định nếu chưa rõ)", expanded=False):
    c3, c4 = st.columns(2)

    with c3:
        original_cltv = st.number_input(
            "Tỷ lệ cho vay gộp (%)",
            min_value=0.0,
            max_value=150.0,
            value=80.0,
            help="Tương tự tỷ lệ cho vay trên giá trị tài sản, nhưng tính cả các khoản vay liên quan khác.",
        )

        channel_display = st.selectbox(
            "Kênh phát hành",
            ["Bán lẻ", "Qua môi giới", "Khác"],
            help="Kênh mà khoản vay được phát hành.",
        )

        property_type_display = st.selectbox(
            "Loại tài sản",
            ["Nhà ở đơn lẻ", "Căn hộ/PUD", "Condo", "Nhà sản xuất sẵn", "Khác"],
            help="Loại tài sản bảo đảm cho khoản vay.",
        )

        property_state = st.text_input(
            "Bang của tài sản",
            value="CA",
            help="Ví dụ: CA, TX, FL, NY...",
        )

        occupancy_display = st.selectbox(
            "Tình trạng cư trú",
            ["Nhà ở chính", "Nhà ở thứ cấp", "Bất động sản đầu tư"],
            help="Người vay sử dụng tài sản này để ở chính, ở phụ hay đầu tư.",
        )

        number_of_units = st.number_input(
            "Số đơn vị nhà ở",
            min_value=1,
            max_value=4,
            value=1,
            help="Ví dụ nhà đơn lập thường là 1.",
        )

    with c4:
        number_of_borrowers = st.number_input(
            "Số người vay",
            min_value=1,
            max_value=4,
            value=1,
            help="Số người cùng đứng tên khoản vay.",
        )

        mi_percentage = st.number_input(
            "Tỷ lệ bảo hiểm thế chấp (%)",
            min_value=0.0,
            max_value=60.0,
            value=0.0,
            help="Nếu không có bảo hiểm thế chấp thì để 0.",
        )

        super_conforming_display = st.selectbox(
            "Khoản vay vượt chuẩn?",
            ["Không", "Có"],
            index=0,
            help="Cho biết khoản vay có thuộc nhóm vượt chuẩn hay không.",
        )

        interest_only_display = st.selectbox(
            "Khoản vay chỉ trả lãi?",
            ["Không", "Có"],
            index=0,
            help="Nếu giai đoạn đầu chỉ trả lãi thì chọn Có.",
        )

        property_valuation_method = st.selectbox(
            "Phương pháp định giá tài sản",
            [1, 2, 4],
            index=1,
            help="Nếu chưa rõ, giữ mặc định là 2.",
        )

channel_map = {
    "Bán lẻ": "R",
    "Qua môi giới": "B",
    "Khác": "C",
}

property_type_map = {
    "Nhà ở đơn lẻ": "SF",
    "Căn hộ/PUD": "PU",
    "Condo": "CO",
    "Nhà sản xuất sẵn": "MH",
    "Khác": "CP",
}

occupancy_map = {
    "Nhà ở chính": "P",
    "Nhà ở thứ cấp": "S",
    "Bất động sản đầu tư": "I",
}

super_conforming_map = {
    "Không": "N",
    "Có": "Y",
}

interest_only_map = {
    "Không": "N",
    "Có": "Y",
}

channel = channel_map[channel_display]
property_type = property_type_map[property_type_display]
occupancy_status = occupancy_map[occupancy_display]
super_conforming_flag = super_conforming_map[super_conforming_display]
interest_only_indicator = interest_only_map[interest_only_display]

st.info("Nếu bạn không chắc về các thông tin nâng cao, hãy giữ nguyên giá trị mặc định.")

st.markdown("---")

if st.button("Dự báo lãi suất", use_container_width=True):
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
        "property_valuation_method": int(property_valuation_method),
    }])

    y_pred = pipeline.predict(input_data)[0]

    st.success(f"Lãi suất dự báo: {y_pred:.4f}%")
    st.markdown("### Dữ liệu đã đưa vào mô hình")
    st.dataframe(input_data, use_container_width=True)

st.markdown("---")

