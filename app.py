import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="QuickCart Enterprise", page_icon="🛍️", layout="wide")

# ================= DESIGN SYSTEM =================
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .product-card {
        background-color: #1e2127; border-radius: 15px; padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5); text-align: center;
        transition: transform 0.3s ease; border: 1px solid #333;
    }
    .product-card:hover { transform: translateY(-5px); border-color: #ff4b4b; }
    .price-tag { font-size: 1.8rem; font-weight: bold; color: #00ffaa; }
    .stock-tag { font-size: 0.9rem; color: #ffa500; }
    .category-tag { font-size: 0.8rem; background: #333; padding: 2px 8px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ====== SESSION STATE ======
if 'cart' not in st.session_state:
    st.session_state.cart = {} # dictionary of product_id: quantity
if 'username' not in st.session_state:
    st.session_state.username = None

# ====== AUTHENTICATION ======
st.sidebar.title("🔐 Account")
if not st.session_state.username:
    user = st.sidebar.text_input("Username")
    if st.sidebar.button("Login"):
        if user:
            st.session_state.username = user
            st.rerun()
else:
    st.sidebar.success(f"Logged in as **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        st.session_state.username = None
        st.session_state.cart = {}
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("Navigate to the **Admin Dashboard** or **Order History** using the sidebar above!")

# ====== DATABASE FETCH ======
conn = get_connection()
products_df = pd.read_sql("SELECT * FROM products", conn)

st.title("🛒 QuickCart Storefront")
search_query = st.text_input("🔍 Search our catalog of 30+ products...", "")

categories = ["All"] + sorted(products_df['category'].unique().tolist())
selected_category = st.radio("Filter by Category:", categories, horizontal=True)

# Filtering Logic
mask = pd.Series([True]*len(products_df))
if selected_category != "All":
    mask = mask & (products_df['category'] == selected_category)
if search_query:
    mask = mask & (products_df['name'].str.contains(search_query, case=False))

filtered_df = products_df[mask]

col1, col2 = st.columns([3, 1])

def add_to_cart(pid):
    if not st.session_state.username:
        st.toast("Please log in to add items!", icon='⚠️')
        return
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
    st.toast("Item added to cart!", icon='✅')

with col1:
    if len(filtered_df) == 0:
        st.warning("No products found.")
        
    for i in range(0, len(filtered_df), 3):
        row = st.columns(3)
        for j, (_, product) in enumerate(filtered_df.iloc[i:i+3].iterrows()):
            with row[j]:
                st.markdown(f"""
                <div class="product-card">
                    <h1 style='font-size: 4rem; margin: 0;'>{product['emoji']}</h1>
                    <span class="category-tag">{product['category']}</span>
                    <h4>{product['name']}</h4>
                    <p style="color: #bbb; font-size: 0.9em; height: 40px;">{product['description']}</p>
                    <p class="price-tag">${product['price']:.2f}</p>
                    <p class="stock-tag">Stock: {product['stock']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Button placement directly under the card via Streamlit
                btn_disabled = product['stock'] <= 0
                btn_label = "Add to Cart 🛒" if not btn_disabled else "Out of Stock ❌"
                if st.button(btn_label, key=f"add_{product['id']}", disabled=btn_disabled, use_container_width=True):
                    add_to_cart(product['id'])
                st.write("") 

with col2:
    st.subheader("🛒 Your Cart")
    st.markdown("---")
    
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = 0
        for pid, qty in st.session_state.cart.items():
            # fetch product info
            p = products_df[products_df['id'] == pid].iloc[0]
            item_total = p['price'] * qty
            total += item_total
            st.markdown(f"**{p['emoji']} {p['name']}**")
            st.markdown(f"{qty}x @ ${p['price']} = <span style='color:#00ffaa;'>${item_total:.2f}</span>", unsafe_allow_html=True)
            st.markdown("---")
            
        st.markdown(f"<h3 style='text-align: right; color:#ff4b4b;'>Total: ${total:.2f}</h3>", unsafe_allow_html=True)
        
        if st.button("💳 Secure Checkout", type="primary", use_container_width=True):
            if total > 0:
                # Save Order to DB
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
                st.success(f"Order #{order_id} placed successfully!")
                st.balloons()
                st.session_state.cart = {}
            else:
                st.error("Cart is empty")
        
        if st.button("🗑️ Clear Cart", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()

conn.close()
