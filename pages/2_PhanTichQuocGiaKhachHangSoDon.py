import streamlit as st
import pandas as pd
import plotly.express as px
from components.data_loader import load_data

st.title("2_🌍 Phân tích theo Quốc gia, Khách hàng và Kích cỡ đơn hàng")

# Load dữ liệu
df = load_data()

# --- Tạo lưới trên: 2 cột cho biểu đồ ngang ---
col1, col2 = st.columns(2)

with col1:
    country_sales = df.groupby("COUNTRY")["SALES"].sum().reset_index().sort_values("SALES", ascending=False)
    fig_country = px.bar(country_sales, x="SALES", y="COUNTRY", orientation='h',
                         title="Doanh thu theo quốc gia")
    st.plotly_chart(fig_country, use_container_width=True)

with col2:
    customer_sales = df.groupby("CUSTOMERNAME")["SALES"].sum().reset_index().sort_values("SALES", ascending=False).head(10)
    fig_customer = px.bar(customer_sales, x="SALES", y="CUSTOMERNAME", orientation='h',
                          title="Top 10 khách hàng theo doanh thu")
    st.plotly_chart(fig_customer, use_container_width=True)

# --- Dòng thứ 2: Biểu đồ vòng (donut chart) ---
st.markdown("### 📦 Phân bổ số đơn hàng theo kích cỡ DEALSIZE")

deal_counts = df["DEALSIZE"].value_counts().reset_index()
deal_counts.columns = ["DEALSIZE", "COUNT"]
fig_dealsize = px.pie(deal_counts, names="DEALSIZE", values="COUNT", hole=0.4,
                      title="Số lượng đơn hàng theo DEALSIZE")
st.plotly_chart(fig_dealsize, use_container_width=True)
