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

# 1. Tải dữ liệu
df = load_data()
df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"])

# 2. Tổng doanh thu theo tháng
monthly_sales = df.groupby(pd.Grouper(key="ORDERDATE", freq="M"))["SALES"].sum().reset_index()
monthly_sales.columns = ["Month", "Sales"]

# 3. Thêm chỉ số tháng để làm biến độc lập
monthly_sales["MonthIndex"] = np.arange(len(monthly_sales))

# 4. Huấn luyện mô hình Linear Regression
X = monthly_sales[["MonthIndex"]]
y = monthly_sales["Sales"]
model = LinearRegression()
model.fit(X, y)

# 5. Dự đoán trên dữ liệu hiện tại
monthly_sales["Predicted"] = model.predict(X)

# 6. Đánh giá mô hình
mae = mean_absolute_error(y, monthly_sales["Predicted"])
rmse = np.sqrt(mean_squared_error(y, monthly_sales["Predicted"]))
mape = np.mean(np.abs((y - monthly_sales["Predicted"]) / y)) * 100

# 7. Dự đoán 24 tháng tiếp theo
last_month = monthly_sales["Month"].max()
future_months = pd.date_range(start=last_month + pd.DateOffset(months=1), periods=24, freq='M')
future_month_index = np.arange(len(monthly_sales), len(monthly_sales) + len(future_months))

future_df = pd.DataFrame({
    "Month": future_months,
    "MonthIndex": future_month_index
})
future_df["Sales"] = np.nan
future_df["Predicted"] = model.predict(future_df[["MonthIndex"]])

# 8. Gộp dữ liệu hiện tại và tương lai
all_data = pd.concat([monthly_sales, future_df], ignore_index=True)

# 9. Hiển thị đánh giá mô hình
st.subheader("📊 Đánh giá mô hình Linear Regression")
st.markdown(f"""
- **MAE**: {mae:,.2f}  
- **RMSE**: {rmse:,.2f}  
- **MAPE**: {mape:.2f}%
""")

# 10. Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x="Month", y="Sales", data=all_data, label="Actual", linewidth=2.5)
sns.lineplot(x="Month", y="Predicted", data=all_data, label="Predicted", linestyle="--", color="red", linewidth=2)
plt.axvline(x=last_month, color='gray', linestyle=':', label='Start of Forecast')
plt.title("Actual & Forecasted Sales (Linear Regression)")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
st.pyplot(fig)

# 11. Hiển thị bảng dữ liệu
with st.expander("📋 Dữ liệu chi tiết (bao gồm dự báo)"):
    st.dataframe(all_data.tail(36))

# 12. Diễn giải kết quả
st.markdown("""
### 🧠 Diễn giải kết quả mô hình

- Mô hình **Linear Regression** được huấn luyện trên dữ liệu tổng doanh thu theo tháng.
- Mô hình cố gắng tìm một xu hướng **tuyến tính** (đường thẳng) thể hiện sự thay đổi doanh thu theo thời gian.
- Đã **dự đoán thêm 24 tháng tiếp theo** sử dụng mô hình tuyến tính.

#### 📈 Kết luận:
- Mặc dù mô hình cho thấy **xu hướng tăng trưởng nhẹ theo thời gian**, nhưng không thể hiện rõ các biến động doanh thu lớn trong thực tế.
- **MAE** và **RMSE** tương đối cao → cho thấy mô hình **dự đoán chưa chính xác** tại nhiều thời điểm (đặc biệt là các tháng cao điểm).
- **MAPE > 20%** là dấu hiệu cho thấy mô hình **không đủ chính xác** cho dự báo thực tế nếu doanh nghiệp cần độ tin cậy cao.

#### ⚠️ Hạn chế:
- Linear Regression không nắm bắt được **tính chu kỳ (seasonality)** hay các biến động bất thường trong dữ liệu.
- Do đó, không phù hợp trong bối cảnh dữ liệu doanh thu có nhiều đỉnh, đáy như trong trường hợp này.
""")
