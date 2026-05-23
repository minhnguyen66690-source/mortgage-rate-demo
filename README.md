# Demo dự báo lãi suất khoản vay thế chấp nhà ở

Đây là ứng dụng demo học thuật cho đề tài:

Dự đoán lãi suất khoản vay thế chấp nhà ở kết hợp đặc trưng khoản vay và bối cảnh thị trường

## Mô hình sử dụng
- Mô hình cuối cùng: CatBoost
- Đặc tả tốt nhất: A_loan_only
- Triển khai thực tế trên web bằng cách lưu toàn bộ pipeline cuối cùng

## Chức năng
Người dùng nhập thông tin khoản vay:
- điểm tín dụng
- tỷ lệ nợ trên thu nhập
- tỷ lệ cho vay
- kỳ hạn vay
- mục đích vay
- tình trạng cư trú
- và các biến khoản vay liên quan

Ứng dụng sẽ trả ra:
- lãi suất dự báo

## Cấu trúc thư mục
mortgage_rate_demo/
- app.py
- requirements.txt
- README.md
- models/
  - final_pipeline.joblib
  - feature_config.json

## Cách chạy local
pip install -r requirements.txt
streamlit run app.py

## Lưu ý
Ứng dụng này chỉ phục vụ mục đích học tập và minh họa học thuật.
Không sử dụng cho quyết định tín dụng thực tế.
