import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="Shopping Cart", page_icon="🛒", layout="centered")

st.title("🛒 Your Shopping Cart")

if 'cart' not in st.session_state or not st.session_state.cart:
    st.info("Your cart is empty. Go back to the Storefront to add items.")
    st.page_link("app.py", label="Return to Store", icon="🏪")
    st.stop()

if not st.session_state.get('username'):
    st.warning("Please login at the storefront to checkout.")
    st.page_link("app.py", label="Return to Store", icon="🔐")
    st.stop()

conn = get_connection()
products_df = pd.read_sql("SELECT * FROM products", conn)

st.markdown("---")

total = 0
for pid, qty in list(st.session_state.cart.items()):
    p = products_df[products_df['id'] == pid].iloc[0]
    item_total = p['price'] * qty
    total += item_total
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"**{p['emoji']} {p['name']}**")
    with col2:
        st.write(f"{qty}x @ ${p['price']}")
    with col3:
        st.markdown(f"<span style='color:#00ffaa;'>${item_total:.2f}</span>", unsafe_allow_html=True)
        if st.button("❌ Remove", key=f"del_{pid}", use_container_width=True):
            del st.session_state.cart[pid]
            st.rerun()

st.markdown("---")
st.markdown(f"<h2 style='text-align: right; color:#ff4b4b;'>Total: ${total:.2f}</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("🗑️ Clear Cart", use_container_width=True):
        st.session_state.cart = {}
        st.rerun()

with col2:
    if st.button("💳 Proceed to Checkout", type="primary", use_container_width=True):
        if total > 0:
            # Process checkout and save to DB
            c = conn.cursor()
            c.execute("INSERT INTO orders (username, total_amount) VALUES (?, ?)", (st.session_state.username, total))
            order_id = c.lastrowid
            
            for pid, qty in st.session_state.cart.items():
                p = products_df[products_df['id'] == pid].iloc[0]
                c.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)", 
                            (order_id, pid, qty, p['price']))
                # Reduce stock
                c.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, pid))
                
            conn.commit()
            
            # Save order details in session state for the confirmation page
            st.session_state.last_order_id = order_id
            st.session_state.last_order_total = total
            st.session_state.cart = {} # Empty the cart
            
            # Navigate to confirmation
            st.switch_page("pages/2_Order_Confirmation.py")

conn.close()
