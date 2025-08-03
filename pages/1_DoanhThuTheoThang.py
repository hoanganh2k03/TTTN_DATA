import streamlit as st
import pandas as pd
import plotly.express as px
from components.data_loader import load_data

# Tiêu đề trang
st.title("📈1_ Doanh thu theo tháng")

# Load dữ liệu
df = load_data()

# Kiểm tra dữ liệu đã có cột MONTH chưa, nếu chưa thì thêm
if "MONTH" not in df.columns:
    df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"])
    df["MONTH"] = df["ORDERDATE"].dt.to_period("M").astype(str)

# Gom doanh thu theo tháng
monthly_sales = df.groupby("MONTH")["SALES"].sum().reset_index()

# Biểu đồ
fig = px.line(monthly_sales, x="MONTH", y="SALES",
              title="📆 Tổng doanh thu theo tháng",
              markers=True)

# Hiển thị biểu đồ
st.plotly_chart(fig, use_container_width=True)
