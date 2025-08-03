import streamlit as st
import pandas as pd
import plotly.express as px
from components.data_loader import load_data

# Cấu hình layout
st.set_page_config(layout="wide")
st.title("9_📊 Các yếu tố ảnh hưởng đến doanh thu")

# Load dữ liệu
df = load_data()

# ======== PHÂN TÍCH TRUNG BÌNH DOANH THU THEO DEALSIZE =========
st.markdown("### 🏷️ Ảnh hưởng của DEALSIZE đến SALES")

sales_by_dealsize = df.groupby("DEALSIZE")["SALES"].mean().reset_index()
avg_sales = df["SALES"].mean()

sales_by_dealsize["Impact"] = sales_by_dealsize["SALES"].apply(
    lambda x: "⬆️ Tăng" if x > avg_sales else "⬇️ Giảm"
)
sales_by_dealsize = sales_by_dealsize.sort_values("SALES", ascending=False)

fig_dealsize = px.bar(
    sales_by_dealsize,
    x="DEALSIZE",
    y="SALES",
    color="Impact",
    color_discrete_map={"⬆️ Tăng": "green", "⬇️ Giảm": "red"},
    title="Trung bình doanh thu theo DEALSIZE"
)
st.plotly_chart(fig_dealsize, use_container_width=True)

# ======== PHÂN TÍCH TRUNG BÌNH DOANH THU THEO PRODUCTLINE =========
st.markdown("### 🚗 Ảnh hưởng của PRODUCTLINE đến SALES")

sales_by_productline = df.groupby("PRODUCTLINE")["SALES"].mean().reset_index()
sales_by_productline["Impact"] = sales_by_productline["SALES"].apply(
    lambda x: "⬆️ Tăng" if x > avg_sales else "⬇️ Giảm"
)
sales_by_productline = sales_by_productline.sort_values("SALES", ascending=False)

fig_productline = px.bar(
    sales_by_productline,
    x="PRODUCTLINE",
    y="SALES",
    color="Impact",
    color_discrete_map={"⬆️ Tăng": "green", "⬇️ Giảm": "red"},
    title="Trung bình doanh thu theo PRODUCTLINE"
)
st.plotly_chart(fig_productline, use_container_width=True)

# ======== TÓM TẮT DIỄN GIẢI =========
st.markdown("### 📌 Tóm tắt ảnh hưởng:")

col1, col2 = st.columns(2)

with col1:
    st.success("**Làm tăng SALES so với trung bình:**")
    for _, row in sales_by_dealsize[sales_by_dealsize["Impact"] == "⬆️ Tăng"].iterrows():
        st.markdown(f"- DEALSIZE **{row['DEALSIZE']}**: {round(row['SALES']):,}")
    for _, row in sales_by_productline[sales_by_productline["Impact"] == "⬆️ Tăng"].iterrows():
        st.markdown(f"- PRODUCTLINE **{row['PRODUCTLINE']}**: {round(row['SALES']):,}")

with col2:
    st.error("**Làm giảm SALES so với trung bình:**")
    for _, row in sales_by_dealsize[sales_by_dealsize["Impact"] == "⬇️ Giảm"].iterrows():
        st.markdown(f"- DEALSIZE **{row['DEALSIZE']}**: {round(row['SALES']):,}")
    for _, row in sales_by_productline[sales_by_productline["Impact"] == "⬇️ Giảm"].iterrows():
        st.markdown(f"- PRODUCTLINE **{row['PRODUCTLINE']}**: {round(row['SALES']):,}")

# ======== BẢNG CHÉO STATUS vs DEALSIZE =========
st.markdown("### 🔁 Phân phối trạng thái đơn hàng theo DEALSIZE")

# Thêm tổng hàng và cột bằng margins=True
status_dealsize = pd.crosstab(df["STATUS"], df["DEALSIZE"], margins=True, margins_name="Total")
st.dataframe(status_dealsize)

# ======== GỢI Ý DIỄN GIẢI =========
st.warning(f"""
- Đơn hàng có DEALSIZE **Large** chủ yếu ở trạng thái **Shipped** ({status_dealsize.loc['Shipped', 'Large']} đơn).
- DEALSIZE **Small** có nhiều đơn bị **Cancelled**, **Resolved**, hoặc **In Process**.
- Tổng cộng có **{status_dealsize.loc['Total', 'Total']}** đơn hàng, trong đó **{status_dealsize.loc['Shipped', 'Total']}** đơn là **Shipped**.
""")

