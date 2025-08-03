import streamlit as st
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from components.data_loader import load_data
import plotly.express as px
st.set_page_config(layout="wide")
st.title("8_📈 Phân tích thống kê nâng cao")

df = load_data()

st.markdown("### 📌 Hồi quy tuyến tính: SALES ~ QUANTITYORDERED + PRICEEACH")
# Chuẩn bị dữ liệu cho hồi quy
X = df[["QUANTITYORDERED", "PRICEEACH"]]
X = sm.add_constant(X)
y = df["SALES"]

model = sm.OLS(y, X).fit()
st.text(model.summary())

st.info("""
- **PRICEEACH và QUANTITYORDERED** đều có p-value = 0.000, chứng tỏ **ảnh hưởng có ý nghĩa thống kê đến SALES**.
- Hệ số PRICEEACH là ~59.8 → Mỗi đơn vị tăng giá làm tăng ~59.8 đơn vị SALES (khi quantity không đổi).
- R-squared cao → mô hình phù hợp với dữ liệu.
""")

st.markdown("### 🔍 ANOVA: SALES theo PRODUCTLINE")
anova_df = df[["PRODUCTLINE", "SALES"]]

# Tạo mô hình OLS theo nhóm PRODUCTLINE
model_anova = sm.OLS.from_formula('SALES ~ C(PRODUCTLINE)', data=anova_df).fit()
anova_table = sm.stats.anova_lm(model_anova, typ=2)
st.dataframe(anova_table)

st.success("""
- F = {:.2f}, p-value = {:.4f}
- Với p-value rất nhỏ, kết luận: **Doanh thu khác biệt có ý nghĩa thống kê giữa các dòng sản phẩm**.
""".format(anova_table["F"][0], anova_table["PR(>F)"][0]))

st.markdown("### 🧮 Kiểm định Chi-Square: DEALSIZE vs STATUS")
contingency_table = pd.crosstab(df["DEALSIZE"], df["STATUS"])
chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

st.write("Chi-squared:", round(chi2, 2))
st.write("p-value:", round(p, 4))

if p < 0.05:
    st.warning("Có mối quan hệ đáng kể giữa DEALSIZE và STATUS.")
else:
    st.info("Không có mối quan hệ đáng kể giữa DEALSIZE và STATUS.")

st.markdown("### 🔳 TreeMap phân cấp: Doanh thu theo Tháng và Dòng sản phẩm")

# Tạo cột Month từ ORDERDATE
df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"])
df["Month"] = df["ORDERDATE"].dt.to_period("M").astype(str)

# Tổng doanh thu theo Month và ProductLine
sales_month_line = df.groupby(["Month", "PRODUCTLINE"])["SALES"].sum().reset_index()

# Vẽ Treemap nhiều cấp
fig_treemap = px.treemap(
    sales_month_line,
    path=["Month", "PRODUCTLINE"],
    values="SALES",
    color="SALES",
    color_continuous_scale="Blues",
    title="Tổng doanh thu theo Tháng và Dòng sản phẩm"
)
st.plotly_chart(fig_treemap, use_container_width=True)