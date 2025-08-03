import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from components.data_loader import load_data

st.set_page_config(layout="wide")
st.title("11_📈 Dự đoán doanh thu với Linear Regression")

# Tải dữ liệu
df = load_data()
df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"])

# Tổng doanh thu theo tháng
monthly_sales = df.groupby(pd.Grouper(key="ORDERDATE", freq="M"))["SALES"].sum().reset_index()
monthly_sales.columns = ["Month", "Sales"]

# Thêm cột tháng thứ tự để làm biến X
monthly_sales["MonthIndex"] = np.arange(len(monthly_sales))

# Huấn luyện Linear Regression
X = monthly_sales[["MonthIndex"]]
y = monthly_sales["Sales"]
model = LinearRegression()
model.fit(X, y)

# Dự đoán
monthly_sales["Predicted"] = model.predict(X)

# Đánh giá mô hình
mae = mean_absolute_error(y, monthly_sales["Predicted"])
rmse = np.sqrt(mean_squared_error(y, monthly_sales["Predicted"]))
mape = np.mean(np.abs((y - monthly_sales["Predicted"]) / y)) * 100

# Kết quả đánh giá
st.subheader("📊 Đánh giá mô hình Linear Regression")
st.markdown(f"""
- **MAE**: {mae:.2f}  
- **RMSE**: {rmse:.2f}  
- **MAPE**: {mape:.2f}%
""")

# Vẽ biểu đồ thực tế vs dự đoán
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x="Month", y="Sales", data=monthly_sales, label="Actual", linewidth=2.5)
sns.lineplot(x="Month", y="Predicted", data=monthly_sales, label="Predicted", linestyle="--", color="red", linewidth=2)
plt.title("Actual vs Predicted Sales (Linear Regression)")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
st.pyplot(fig)

# Hiển thị bảng dữ liệu
with st.expander("📋 Dữ liệu chi tiết"):
    st.dataframe(monthly_sales)
st.markdown("""
### 🧠 Diễn giải kết quả mô hình

- Mô hình **Linear Regression** được huấn luyện trên dữ liệu tổng doanh thu theo tháng.
- Mô hình cố gắng tìm một xu hướng **tuyến tính** (đường thẳng) thể hiện sự thay đổi doanh thu theo thời gian.

#### 📈 Kết luận:
- Mặc dù mô hình cho thấy **xu hướng tăng trưởng nhẹ theo thời gian**, nhưng không thể hiện rõ các biến động doanh thu lớn trong thực tế.
- **MAE** và **RMSE** tương đối cao → cho thấy mô hình **dự đoán chưa chính xác** tại nhiều thời điểm (đặc biệt là các tháng cao điểm).
- **MAPE > 20%** là dấu hiệu cho thấy mô hình **không đủ chính xác** cho dự báo thực tế nếu doanh nghiệp cần độ tin cậy cao.

#### ⚠️ Hạn chế:
- Linear Regression không nắm bắt được **tính chu kỳ (seasonality)** hay các biến động bất thường trong dữ liệu.
- Do đó, không phù hợp trong bối cảnh dữ liệu doanh thu có nhiều đỉnh, đáy như trong trường hợp này.
""")