import streamlit as st

st.set_page_config(page_title="Order Confirmation", page_icon="✅", layout="centered")

st.title("✅ Order Confirmed!")

if 'last_order_id' not in st.session_state:
    st.warning("No recent orders found.")
    st.page_link("app.py", label="Return to Store", icon="🏪")
    st.stop()

st.balloons()

order_id = st.session_state.last_order_id
total = st.session_state.last_order_total

st.success(f"Thank you for your purchase, {st.session_state.username}!")

st.markdown(f"""
### Order Details
* **Order ID:** `#{order_id}`
* **Total Paid:** `${total:.2f}`
* **Status:** `Processing for Shipment`

An email receipt has been sent to your registered address.
""")

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.page_link("app.py", label="Continue Shopping", icon="🏪")
with col2:
    st.page_link("pages/4_Order_History.py", label="View Order History", icon="🧾")
