import streamlit as st
import pandas as pd
import plotly.express as px
from components.data_loader import load_data

st.set_page_config(layout="wide")
st.title("4_📊 Tổng quan doanh thu")

# Load dữ liệu
df = load_data()

# KPIs
total_sales = df["SALES"].sum()
min_sales = df["SALES"].min()
std_sales = df["SALES"].std()
avg_sales = df["SALES"].mean()
max_sales = df["SALES"].max()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💰 Tổng doanh thu", f"{total_sales:,.2f}")
col2.metric("📉 Doanh thu nhỏ nhất", f"{min_sales:,.2f}")
col3.metric("📈 Độ lệch chuẩn", f"{std_sales:,.2f}")
col4.metric("📦 Trung bình theo đơn", f"{avg_sales:,.2f}")
col5.metric("🏆 Doanh thu cao nhất", f"{max_sales:,.2f}")

st.markdown("---")

# Biểu đồ
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Phân phối doanh thu (Histogram)")
    fig_hist = px.histogram(df, x="SALES", nbins=30,
                            title="Phân phối doanh thu",
                            labels={"SALES": "Doanh thu"},
                            color_discrete_sequence=["#007BFF"])
    st.plotly_chart(fig_hist, use_container_width=True)

with col_right:
    st.subheader("📦 Phân bố doanh thu (Box Plot)")
    fig_box = px.box(df, y="SALES", points="outliers", title="Phân bố doanh thu (Box Plot)",
                     color_discrete_sequence=["#00BFFF"])
    st.plotly_chart(fig_box, use_container_width=True)
