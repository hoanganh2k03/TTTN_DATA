import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
from components.data_loader import load_data

st.set_page_config(layout="wide")
st.title("12_💡 Phân tích tác động tăng giá đến doanh thu (Random Forest)")

# 1. Đọc dữ liệu
df = load_data()

# 2. Chọn các cột đặc trưng (features) và biến mục tiêu (target)
features = ['PRICEEACH', 'PRODUCTLINE', 'MONTH_ID', 'YEAR_ID', 'COUNTRY', 'PRODUCTCODE', 'CUSTOMERNAME', 'DEALSIZE']
target = 'QUANTITYORDERED'
X = df[features]
y = df[target]

# 3. Tách dữ liệu train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Phân loại đặc trưng số & phân loại
numeric_features = ['PRICEEACH', 'MONTH_ID', 'YEAR_ID']
categorical_features = ['PRODUCTLINE', 'COUNTRY', 'PRODUCTCODE', 'CUSTOMERNAME', 'DEALSIZE']

# 5. Pipeline tiền xử lý + mô hình
preprocessor = ColumnTransformer([
    ('num', 'passthrough', numeric_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
])

model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# 6. Huấn luyện mô hình
model.fit(X_train, y_train)

# 7. Dự đoán trên tập test để đánh giá
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

st.subheader("🎯 Đánh giá mô hình Random Forest")
st.markdown(f"- **MAE (Mean Absolute Error)**: `{mae:.2f}` đơn vị sản phẩm")

# 8. Dự đoán toàn bộ dữ liệu gốc
df["PredictedQuantity"] = model.predict(X)

# 9. Tính doanh thu gốc
df["OriginalRevenue"] = df["PRICEEACH"] * df["QUANTITYORDERED"]

# 10. Tăng giá lên 10% và dự đoán lại
X_new = X.copy()
X_new["PRICEEACH"] = X_new["PRICEEACH"] * 1.1  # tăng giá 10%
df["NewPrice"] = X_new["PRICEEACH"]
df["PredictedQuantity_New"] = model.predict(X_new)
df["NewRevenue"] = df["NewPrice"] * df["PredictedQuantity_New"]

# 11. Tổng doanh thu
original_revenue_total = df["OriginalRevenue"].sum()
new_revenue_total = df["NewRevenue"].sum()
revenue_diff = new_revenue_total - original_revenue_total

st.subheader("📈 So sánh doanh thu trước và sau khi tăng giá 10%")
st.markdown(f"""
- **Doanh thu gốc (thực tế)**: `{original_revenue_total:,.2f}`
- **Doanh thu sau khi tăng giá (dự đoán)**: `{new_revenue_total:,.2f}`
- **Chênh lệch**: `{revenue_diff:,.2f}`
""")

# 12. Tách thành 2 DataFrame
df_original = df[["PRICEEACH", "QUANTITYORDERED", "PredictedQuantity", "OriginalRevenue"]].copy()
df_new = df[["NewPrice", "PredictedQuantity_New", "NewRevenue"]].copy()

# 13. Hiển thị dữ liệu đầu
st.subheader("📋 So sánh dữ liệu đầu")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**🔹 Dữ liệu gốc**")
    st.dataframe(df_original.head(10))

with col2:
    st.markdown("**🔸 Dữ liệu sau tăng giá 10%**")
    st.dataframe(df_new.head(10))
with st.expander("📘 Diễn giải cách tính"):
    st.markdown("""
**1. Mục tiêu**  
Phân tích tác động của việc tăng giá bán sản phẩm (**PRICEEACH**) đến tổng doanh thu bằng mô hình học máy.

---

**2. Dự đoán số lượng bán (QUANTITYORDERED)**  
- Dùng **Random Forest Regressor** để dự đoán số lượng bán ra dựa vào các yếu tố như:
  - Giá sản phẩm, dòng sản phẩm, tháng, năm, quốc gia, mã sản phẩm, tên khách hàng, và kích cỡ đơn hàng.
- Mô hình được huấn luyện trên 80% dữ liệu và kiểm tra trên 20% để đánh giá độ chính xác.

---

**3. Tính doanh thu gốc**
- Doanh thu thật = `PRICEEACH * QUANTITYORDERED`
- Đây là doanh thu đã xảy ra trong thực tế.

---

**4. Tính doanh thu dự đoán (sau khi tăng giá)**
- Tăng `PRICEEACH` thêm 10%: `NewPrice = PRICEEACH * 1.1`
- Dùng mô hình để dự đoán lại số lượng bán với mức giá mới: `PredictedQuantity_New`
- Tính doanh thu mới: `NewRevenue = NewPrice * PredictedQuantity_New`

---

**5. So sánh**
- Tổng doanh thu gốc: tổng tất cả các dòng `OriginalRevenue`
- Tổng doanh thu sau tăng giá: tổng tất cả `NewRevenue`
- Chênh lệch = Doanh thu sau tăng giá – Doanh thu gốc

---

**6. Ý nghĩa**
- Nếu doanh thu mới **cao hơn** doanh thu gốc ⇒ Tăng giá 10% là **có lợi**
- Nếu doanh thu mới **thấp hơn** ⇒ Có thể mất khách hàng ⇒ **Không nên tăng giá**

> ⚠️ Đây chỉ là dự đoán, còn phụ thuộc vào độ chính xác mô hình và giả định rằng các yếu tố khác không thay đổi.
    """)