import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")

st.title("📊 Enterprise Admin Dashboard")

if st.session_state.get("username") != "admin":
    st.error("Access Denied: You must be logged in as 'admin' to view this page.")
    st.info("Go to the storefront and login as 'admin'.")
    st.stop()

conn = get_connection()

# Metrics
st.subheader("System Metrics")
total_orders = pd.read_sql("SELECT COUNT(*) as count FROM orders", conn).iloc[0]['count']
total_revenue = pd.read_sql("SELECT SUM(total_amount) as total FROM orders", conn).iloc[0]['total']
total_revenue = total_revenue if total_revenue else 0
low_stock = pd.read_sql("SELECT COUNT(*) as count FROM products WHERE stock < 10", conn).iloc[0]['count']

m1, m2, m3 = st.columns(3)
m1.metric("Total Orders", total_orders)
m2.metric("Total Revenue", f"${total_revenue:.2f}")
m3.metric("Low Stock Items", low_stock, delta="- Critical", delta_color="inverse")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Inventory Status")
    inventory_df = pd.read_sql("SELECT id, name, category, stock, price FROM products ORDER BY stock ASC", conn)
    st.dataframe(inventory_df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("🧾 Recent Orders")
    orders_df = pd.read_sql("SELECT id, username, total_amount, timestamp, status FROM orders ORDER BY timestamp DESC LIMIT 10", conn)
    st.dataframe(orders_df, use_container_width=True, hide_index=True)

conn.close()
