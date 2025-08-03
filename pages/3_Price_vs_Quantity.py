import streamlit as st
import pandas as pd
import plotly.express as px
from components.data_loader import load_data

st.title("3_💲 Phân tích đơn giá (PRICEEACH) và số lượng đặt hàng (QUANTITYORDERED)")

# Load data
df = load_data()

# --- Chia thành 2 cột: Biểu đồ trái và phải ---
col1, col2 = st.columns(2)

# --- Biểu đồ histogram PRICEEACH ---
with col1:
    st.subheader("📊 Phân phối đơn giá (PRICEEACH)")
    fig_price = px.histogram(df, x="PRICEEACH", nbins=30,
                              title="Histogram của PRICEEACH",
                              labels={"PRICEEACH": "Đơn giá"})
    st.plotly_chart(fig_price, use_container_width=True)

# --- Biểu đồ Heatmap giữa PRICEEACH và QUANTITYORDERED ---
with col2:
    st.subheader("🔥 Ma trận mật độ: PRICEEACH vs QUANTITYORDERED")

    fig_heatmap = px.density_heatmap(df, x="PRICEEACH", y="QUANTITYORDERED",
                                     nbinsx=30, nbinsy=30,
                                     color_continuous_scale="Blues",
                                     title="Heatmap mật độ giữa đơn giá và số lượng")
    st.plotly_chart(fig_heatmap, use_container_width=True)
