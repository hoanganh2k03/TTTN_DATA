import streamlit as st
import pandas as pd
import plotly.express as px
from components.data_loader import load_data

st.set_page_config(layout="wide")
st.title("5_📦 Tổng quan sản phẩm")

df = load_data()

# KPI
col1, col2 = st.columns(2)
col1.metric("🔢 Tổng số lượng sản phẩm", f"{df['QUANTITYORDERED'].sum():,.0f}")
col2.metric("📊 Trung bình số lượng theo đơn", f"{df['QUANTITYORDERED'].mean():.2f}")

# Histogram số lượng đặt hàng
st.markdown("### 📈 Phân phối số lượng đặt hàng")
fig_qtty = px.histogram(df, x="QUANTITYORDERED", nbins=40,
                        title="Phân phối QUANTITYORDERED",
                        color_discrete_sequence=["#2196F3"])
st.plotly_chart(fig_qtty, use_container_width=True)

# Box plot giá sản phẩm
st.markdown("### 💲 Phân phối đơn giá sản phẩm (PRICEEACH)")
fig_price = px.box(df, y="PRICEEACH", title="Box Plot PRICEEACH",
                   color_discrete_sequence=["#00BCD4"])
st.plotly_chart(fig_price, use_container_width=True)

# Tổng doanh thu theo dòng sản phẩm
st.markdown("### 🛍️ Doanh thu theo dòng sản phẩm (PRODUCTLINE)")
sales_by_productline = df.groupby("PRODUCTLINE")["SALES"].sum().sort_values(ascending=False).reset_index()
fig_prod = px.bar(sales_by_productline, x="SALES", y="PRODUCTLINE",
                  orientation='h', title="Tổng doanh thu theo PRODUCTLINE",
                  color_discrete_sequence=["#4CAF50"])
st.plotly_chart(fig_prod, use_container_width=True)

# Pareto chart
st.markdown("### 📈 Biểu đồ Pareto (Doanh thu theo PRODUCTLINE)")
sales_by_productline["CUMSUM"] = sales_by_productline["SALES"].cumsum()
sales_by_productline["CUMPER"] = 100 * sales_by_productline["CUMSUM"] / sales_by_productline["SALES"].sum()

fig_pareto = px.bar(sales_by_productline, x="PRODUCTLINE", y="SALES", title="Pareto Chart theo PRODUCTLINE",
                    labels={"SALES": "Tổng doanh thu"}, color_discrete_sequence=["#9C27B0"])

fig_pareto.add_scatter(x=sales_by_productline["PRODUCTLINE"], y=sales_by_productline["CUMPER"],
                       mode="lines+markers", name="Tỷ lệ tích lũy (%)", yaxis="y2")

fig_pareto.update_layout(
    yaxis=dict(title="Tổng doanh thu"),
    yaxis2=dict(overlaying="y", side="right", title="Tỷ lệ tích lũy (%)", range=[0, 110]),
    legend=dict(x=0.85, y=1.15, orientation="h")
)

st.plotly_chart(fig_pareto, use_container_width=True)

# Doanh thu theo PRODUCTCODE
st.markdown("### 🔢 Doanh thu theo mã sản phẩm (PRODUCTCODE)")
fig_code = px.bar(
    df.groupby("PRODUCTCODE")["SALES"].sum().sort_values(ascending=False).reset_index(),
    x="PRODUCTCODE",
    y="SALES",
    title="Tổng doanh thu theo PRODUCTCODE",
    color_discrete_sequence=["#FF5722"]
)
st.plotly_chart(fig_code, use_container_width=True)
