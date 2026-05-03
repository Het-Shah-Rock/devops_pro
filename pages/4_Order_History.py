import streamlit as st
import pandas as pd
from database import get_connection
import random

st.set_page_config(page_title="Order History - QuickCart", page_icon="🧾", layout="wide")

st.markdown("""
<style>
html, body, .stApp { background: #0a0a0a; color: #f1f1f1; }
div.stButton > button { background: #ff4b2b; color: white; border: none; border-radius: 10px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get('username'):
    st.warning("Please login first.")
    st.page_link("app.py", label="Go to Storefront", icon="🏪")
    st.stop()

st.title("🧾 My Orders")
st.caption(f"Logged in as **{st.session_state.username}**")

conn = get_connection()
orders = pd.read_sql(
    "SELECT * FROM orders WHERE username=? ORDER BY timestamp DESC",
    conn, params=(st.session_state.username,)
)

if len(orders) == 0:
    st.info("You haven't placed any orders yet.")
    st.page_link("app.py", label="Start Shopping!", icon="🛒")
else:
    total_spent = orders['total_amount'].sum()
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Orders", len(orders))
    m2.metric("Total Spent", f"${total_spent:.2f}")
    m3.metric("Last Order", f"#{orders.iloc[0]['id']}")
    st.markdown("---")

    statuses = ["Order Placed", "Preparing Order", "Out for Delivery", "Delivered"]
    status_colors = {"Order Placed":"#38bdf8","Preparing Order":"#fbbf24",
                     "Out for Delivery":"#fbbf24","Delivered":"#00e676"}

    for _, order in orders.iterrows():
        status = statuses[min(random.randint(2, 3), 3)]
        sc = status_colors.get(status, "white")
        with st.expander(f"📦 Order #{order['id']} · {str(order['timestamp'])[:16]} · ${order['total_amount']:.2f}"):
            c1, c2 = st.columns(2)
            c1.markdown(f"**Status:** <span style='color:{sc};font-weight:700'>{status}</span>", unsafe_allow_html=True)
            c1.write(f"**Payment:** {order.get('payment_method','')}")
            c1.write(f"**Coupon:** {order.get('coupon_used','') or 'None'}")
            c2.write(f"**Delivering to:** {order.get('delivery_address','')}")
            c2.write(f"**City:** {order.get('city','')} — {order.get('pincode','')}")
            c2.write(f"**Discount:** -${order.get('discount_amount',0):.2f}")

            items = pd.read_sql(f"""
                SELECT p.emoji as '', p.name as 'Product', oi.quantity as 'Qty',
                       oi.price as 'Unit Price', (oi.quantity*oi.price) as 'Total'
                FROM order_items oi JOIN products p ON oi.product_id=p.id
                WHERE oi.order_id={order['id']}
            """, conn)
            if not items.empty:
                st.dataframe(items, hide_index=True, use_container_width=True)

            if st.button(f"🔄 Reorder this", key=f"reorder_{order['id']}"):
                if 'cart' not in st.session_state:
                    st.session_state.cart = {}
                raw = pd.read_sql(f"""
                    SELECT oi.product_id, oi.quantity FROM order_items oi WHERE oi.order_id={order['id']}
                """, conn)
                for _, row in raw.iterrows():
                    pid = int(row['product_id'])
                    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + int(row['quantity'])
                st.toast("Items added to cart!", icon="✅")

conn.close()
