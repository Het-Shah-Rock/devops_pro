import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="QuickCart Store", page_icon="🛍️", layout="wide")

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
# Show Cart Summary in sidebar
total_items = sum(st.session_state.cart.values())
st.sidebar.info(f"🛒 **Cart:** {total_items} items")
st.sidebar.page_link("pages/1_Cart.py", label="Go to Cart", icon="🛒")

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

def add_to_cart(pid):
    if not st.session_state.username:
        st.toast("Please log in to add items!", icon='⚠️')
        return
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
    st.toast("Item added to cart! Go to the Cart page to checkout.", icon='✅')

if len(filtered_df) == 0:
    st.warning("No products found.")
    
for i in range(0, len(filtered_df), 4):
    row = st.columns(4)
    for j, (_, product) in enumerate(filtered_df.iloc[i:i+4].iterrows()):
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
            
            btn_disabled = product['stock'] <= 0
            btn_label = "Add to Cart 🛒" if not btn_disabled else "Out of Stock ❌"
            if st.button(btn_label, key=f"add_{product['id']}", disabled=btn_disabled, use_container_width=True):
                add_to_cart(product['id'])
            st.write("") 

conn.close()
