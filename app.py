import streamlit as st

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

st.title("📊 Sales Dashboard - Trang chủ")

st.markdown("""
Chào mừng bạn đến với **Sales Dashboard**!  
Ứng dụng này được xây dựng bằng **Streamlit + Plotly** nhằm trực quan hóa dữ liệu bán hàng.

---

### 📁 Các trang chính:
- **Tổng quan**: Xem các chỉ số quan trọng như tổng doanh thu, trung bình đơn hàng...
- **Doanh thu theo tháng**: Phân tích doanh thu theo thời gian.
- **Biểu đồ chi tiết**: Các biểu đồ theo dòng sản phẩm, quốc gia, khách hàng...
- **Giới thiệu**: Mô tả và thông tin dự án.

---

👉 Dùng menu bên trái để chuyển trang.
""")
