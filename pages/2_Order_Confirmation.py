import streamlit as st
import pandas as pd
from database import get_connection
import time

st.set_page_config(page_title="Order Confirmed! - QuickCart", page_icon="✅", layout="centered")

st.markdown("""
<style>
html, body, .stApp { background: #0a0a0a; color: #f1f1f1; }
.confirm-box { background: linear-gradient(135deg, #0d2137, #0a1628);
    border: 1px solid #1a4a6e; border-radius: 20px; padding: 40px; text-align: center; }
.track-step { display: flex; align-items: center; gap: 14px;
    padding: 14px; background: #111827; border-radius: 10px; margin-bottom: 8px; }
.step-done { border-left: 4px solid #00e676; }
.step-active { border-left: 4px solid #fbbf24; }
.step-pending { border-left: 4px solid #374151; opacity: 0.5; }
div.stButton > button { background: #ff4b2b; color: white; border: none; border-radius: 10px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

if 'last_order_id' not in st.session_state:
    st.warning("No recent order found.")
    st.page_link("app.py", label="Go Shopping", icon="🏪"); st.stop()

order_id = st.session_state.last_order_id
total = st.session_state.last_order_total

st.balloons()

st.markdown(f"""
<div class="confirm-box">
  <div style="font-size:4rem">✅</div>
  <h1 style="color:#00e676;margin:10px 0">Order Confirmed!</h1>
  <p style="color:#94a3b8;font-size:1.1rem">Thank you, <strong style="color:white">{st.session_state.get('username','')}</strong>!</p>
  <div style="background:#0f2a3d;border-radius:12px;padding:16px;margin:20px 0">
    <p style="margin:4px 0;font-size:1.3rem;font-weight:700">Order <span style="color:#38bdf8">#{order_id}</span></p>
    <p style="color:#94a3b8;margin:4px 0">Total Paid: <span style="color:#00e676;font-weight:700">${total:.2f}</span></p>
    <p style="color:#94a3b8;margin:4px 0">Delivering to: {st.session_state.get('city','')}, {st.session_state.get('pincode','')}</p>
  </div>
  <div style="background:#fbbf2420;border:1px solid #fbbf24;border-radius:10px;padding:12px">
    <p style="color:#fbbf24;font-size:1.1rem;font-weight:700;margin:0">⏱️ Estimated Delivery: 10-15 Minutes</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📍 Live Order Tracking")

tracking_steps = [
    ("✅", "step-done", "Order Placed", "Your order has been received and confirmed."),
    ("🔄", "step-active", "Preparing Order", "Our team is carefully picking your items."),
    ("🛵", "step-pending", "Out for Delivery", "A delivery partner will be assigned soon."),
    ("🏠", "step-pending", "Delivered", "Enjoy your order!"),
]

for icon, css, title, desc in tracking_steps:
    st.markdown(f"""<div class="track-step {css}">
        <span style="font-size:1.8rem">{icon}</span>
        <div>
          <p style="font-weight:700;margin:0">{title}</p>
          <p style="color:#94a3b8;margin:0;font-size:0.85rem">{desc}</p>
        </div>
    </div>""", unsafe_allow_html=True)

# Show ordered items from DB
conn = get_connection()
try:
    items = pd.read_sql(f"""
        SELECT p.emoji, p.name, oi.quantity, oi.price
        FROM order_items oi JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = {order_id}
    """, conn)
    if not items.empty:
        st.markdown("---")
        st.markdown("### 🧾 Items in this Order")
        items['Total'] = items['quantity'] * items['price']
        items.columns = ['', 'Product', 'Qty', 'Unit Price', 'Total']
        st.dataframe(items, hide_index=True, use_container_width=True)
except: pass
conn.close()

st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    st.page_link("app.py", label="Continue Shopping", icon="🏪")
with c2:
    st.page_link("pages/4_Order_History.py", label="View All Orders", icon="🧾")
