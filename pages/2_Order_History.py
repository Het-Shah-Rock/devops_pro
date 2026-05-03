import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="Order History", page_icon="🧾", layout="centered")

st.title("🧾 Your Order History")

username = st.session_state.get("username")

if not username:
    st.warning("Please login at the storefront to view your order history.")
    st.stop()

conn = get_connection()

orders = pd.read_sql(f"SELECT * FROM orders WHERE username = '{username}' ORDER BY timestamp DESC", conn)

if len(orders) == 0:
    st.info("You haven't placed any orders yet.")
else:
    for _, order in orders.iterrows():
        with st.expander(f"Order #{order['id']} - {order['timestamp']} - ${order['total_amount']:.2f}"):
            st.write(f"**Status:** {order['status']}")
            
            # Fetch items
            items = pd.read_sql(f"""
                SELECT p.name, p.emoji, oi.quantity, oi.price
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = {order['id']}
            """, conn)
            
            st.table(items)

conn.close()
