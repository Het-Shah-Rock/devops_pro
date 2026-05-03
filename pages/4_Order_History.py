import streamlit as st
import pandas as pd
from database import get_connection
import random

st.set_page_config(page_title="Order History - QuickCart", page_icon="🧾", layout="wide")

st.markdown("""
<style>
html, body, .stApp { background: #0a0a0a; color: #f1f1f1; }
.order-card { background: #111827; border-radius: 14px; padding: 20px; border: 1px solid #1e293b; margin-bottom: 12px; }
.status-placed { color: #38bdf8; }
.status-processing { color: #fbbf24; }
.status-delivered { color: #00e676; }
div.stButton > button { background: #ff4b2b; color: white; border: none; border-radius: 10px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get('username'):
    st.warning("Please login first.")
    st.page_link("app.py", label="Go to Storefront", icon="🏪"); st.stop()

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
    # Summary metrics
    total_spent = orders['total_amount'].sum()
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Orders", len(orders))
    m2.metric("Total Spent", f"${total_spent:.2f}")
    m3.metric("Last Order", f"#{orders.iloc[0]['id']}")

    st.markdown("---")

    for _, order in orders.iterrows():
        # Simulate status progression based on order age
        statuses = ["Order Placed", "Preparing Order", "Out for Delivery", "Delivered"]
        status_idx = random.randint(2, 3)  # Simulate mostly delivered
        status = statuses[status_idx]
        status_color = {"Order Placed":"#38bdf8","Preparing Order":"#fbbf24",
                       "Out for Delivery":"#fbbf24","Delivered":"#00e676"}.get(status,"white")

        with st.expander(f"📦 Order #{order['id']} · {order['timestamp'][:16]} · ${order['total_amount']:.2f} · {status}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Status:** <span style='color:{status_color};font-weight:700'>{status}</span>", unsafe_allow_html=True)
                st.markdown(f"**Payment:** {order['payment_method']}")
                st.markdown(f"**Coupon:** {order.get('coupon_used','None') or 'None'}")
            with c2:
                st.markdown(f"**Delivering to:** {order.get('delivery_address','')}")
                st.markdown(f"**City:** {order.get('city','')} — {order.get('pincode','')}")
                st.markdown(f"**Discount:** -${order.get('discount_amount',0):.2f}")

            # Order items
            items = pd.read_sql(f"""
                SELECT p.emoji, p.name, oi.quantity, oi.price,
                       (oi.quantity * oi.price) as total
                FROM order_items oi JOIN products p ON oi.product_id=p.id
                WHERE oi.order_id={order['id']}
            """, conn)
            if not items.empty:
                st.dataframe(items, hide_index=True, use_container_width=True)

            # Reorder button
            if st.button(f"🔄 Reorder", key=f"reorder_{order['id']}"):
                if 'cart' not in st.session_state: st.session_state.cart = {}
                for _, item in items.iterrows():
                    pid_row = pd.read_sql(f"SELECT id FROM products WHERE name='{item['name']}'", conn)
                    if not pid_row.empty:
                        pid = int(pid_row.iloc[0]['id'])
                        st.session_state.cart[pid] = st.session_state.cart.get(pid,0) + int(item['quantity'])
                st.toast("Items added to cart!", icon="✅")

conn.close()
