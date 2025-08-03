import streamlit as st
import pandas as pd
import plotly.express as px
from components.data_loader import load_data

st.set_page_config(layout="wide")
st.title("6_👥 Tổng quan khách hàng")

df = load_data()

# TreeMap: Doanh thu theo khách hàng
st.markdown("### 🔳 TreeMap: Doanh thu theo tên khách hàng")
fig_tree = px.treemap(
    df.groupby("CUSTOMERNAME")["SALES"].sum().sort_values(ascending=False).head(10).reset_index(),
    path=["CUSTOMERNAME"],
    values="SALES",
    color="SALES",
    color_continuous_scale="Blues",
    title="Doanh thu theo khách hàng"
)
st.plotly_chart(fig_tree, use_container_width=True)

# Biểu đồ doanh thu theo quốc gia
st.markdown("### 🌍 Doanh thu theo quốc gia (COUNTRY)")
sales_by_country = df.groupby("COUNTRY")["SALES"].sum().sort_values(ascending=False).head(10).reset_index()
fig_country_sales = px.bar(
    sales_by_country,
    x="COUNTRY",
    y="SALES",
    title="Tổng doanh thu theo quốc gia",
    color_discrete_sequence=["#2196F3"]
)
st.plotly_chart(fig_country_sales, use_container_width=True)

# Biểu đồ số lượng khách hàng theo quốc gia
st.markdown("### 📊 Số lượng khách hàng theo quốc gia")
customer_count = df[["CUSTOMERNAME", "COUNTRY"]].drop_duplicates().groupby("COUNTRY").count().sort_values("CUSTOMERNAME", ascending=False).head(10).reset_index()
customer_count.columns = ["COUNTRY", "CUSTOMER_COUNT"]

fig_customer = px.bar(
    customer_count,
    x="COUNTRY",
    y="CUSTOMER_COUNT",
    title="Số lượng khách hàng theo quốc gia",
    color_discrete_sequence=["#4CAF50"]
)
st.plotly_chart(fig_customer, use_container_width=True)
