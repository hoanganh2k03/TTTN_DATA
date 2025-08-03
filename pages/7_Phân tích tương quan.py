import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from components.data_loader import load_data

st.set_page_config(layout="wide")
st.title("7_📊 Phân tích tương quan")

df = load_data()

# Tính toán hệ số tương quan
correlation_matrix = df[["SALES", "QUANTITYORDERED", "PRICEEACH"]].corr()

# Vẽ heatmap tương quan
st.markdown("### 🔥 Heatmap: Mối tương quan giữa Sales, Quantity, Price")
fig_corr, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(correlation_matrix, annot=True, cmap="RdBu_r", center=0, ax=ax)
st.pyplot(fig_corr)

# Giải thích
st.info("""
- **SALES** có tương quan dương mạnh với cả **QUANTITYORDERED** (`0.55`) và **PRICEEACH** (`0.66`) vì SALES = PRICEEACH × QUANTITYORDERED.
- **QUANTITYORDERED** và **PRICEEACH** gần như **không có tương quan** (0.004), cho thấy mức giá không ảnh hưởng rõ ràng đến số lượng mua.
""")

# Vẽ scatter plot giữa PRICEEACH và QUANTITYORDERED
st.markdown("### 📉 Mối quan hệ giữa Giá (PriceEach) và Số lượng đặt hàng (QuantityOrdered)")
fig_scatter = px.scatter(
    df, x="PRICEEACH", y="QUANTITYORDERED", trendline="ols",
    title="PRICE vs QUANTITYORDERED", opacity=0.6
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Diễn giải thêm
st.warning("""
- Như biểu đồ thể hiện, **không có xu hướng rõ ràng giữa giá và số lượng** – đường xu hướng khá phẳng.
- Điều này gợi ý rằng khách hàng có thể **không quá nhạy cảm với giá** trong dữ liệu hiện tại (hoặc các yếu tố khác như sản phẩm, thương hiệu ảnh hưởng nhiều hơn).
""")
