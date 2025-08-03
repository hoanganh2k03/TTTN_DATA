import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
from prophet.plot import plot_plotly
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_error, mean_squared_error
from components.data_loader import load_data

st.set_page_config(layout="wide")
st.title("10_📈 Dự báo doanh thu theo tháng")

df = load_data()

# Tiền xử lý
df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"])
monthly_sales = df.groupby(pd.Grouper(key="ORDERDATE", freq="M"))["SALES"].sum().reset_index()
monthly_sales.columns = ["ds", "y"]

# Phân tích chuỗi thời gian
st.markdown("### 🔍 Decomposition chuỗi thời gian (Multiplicative)")

decomposition = seasonal_decompose(monthly_sales.set_index("ds")["y"], model="multiplicative")
fig, ax = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
decomposition.observed.plot(ax=ax[0], title="Observed")
decomposition.trend.plot(ax=ax[1], title="Trend")
decomposition.seasonal.plot(ax=ax[2], title="Seasonal")
decomposition.resid.plot(ax=ax[3], title="Residual")
plt.tight_layout()
st.pyplot(fig)

# Huấn luyện mô hình Prophet
st.markdown("### 📊 Dự báo doanh thu với Prophet (multiplicative seasonality)")
model = Prophet(seasonality_mode="multiplicative", yearly_seasonality=True)
model.fit(monthly_sales)

future = model.make_future_dataframe(periods=24, freq="M")
forecast = model.predict(future)

st.plotly_chart(plot_plotly(model, forecast), use_container_width=True)

# Đánh giá mô hình
predicted = forecast.iloc[:len(monthly_sales)]
y_true = monthly_sales["y"].values
y_pred = predicted["yhat"].values

mae = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

st.markdown("### 📐 Đánh giá mô hình dự báo")
st.success(f"**MAE:** {mae:.2f} | **RMSE:** {rmse:.2f} | **MAPE:** {mape:.2f}%")

# So sánh thực tế vs dự đoán
st.markdown("### 📉 Biểu đồ So sánh Actual vs Predicted")
fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.lineplot(x=predicted["ds"], y=y_true, label="Actual", linewidth=2.5)
sns.lineplot(x=predicted["ds"], y=y_pred, label="Predicted", linestyle="--", color="red", linewidth=2)
plt.title("Actual vs Predicted Sales")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.grid(True)
plt.legend()
st.pyplot(fig2)
