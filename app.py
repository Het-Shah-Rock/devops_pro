import streamlit as st
import json
import time

st.set_page_config(page_title="QuickCart Pro", page_icon="🛍️", layout="wide")

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
</style>
""", unsafe_allow_html=True)

# ====== FEATURE 1: MOCK DATABASE ======
products = [
    {"id": 1, "name": "Fresh Apples (1kg)", "price": 4.99, "category": "Grocery", "stock": 50, "emoji": "🍎"},
    {"id": 2, "name": "Organic Milk (1L)", "price": 2.49, "category": "Dairy", "stock": 20, "emoji": "🥛"},
    {"id": 3, "name": "Whole Wheat Bread", "price": 3.99, "category": "Bakery", "stock": 15, "emoji": "🍞"},
    {"id": 4, "name": "Wireless AirPods", "price": 129.99, "category": "Electronics", "stock": 5, "emoji": "🎧"},
    {"id": 5, "name": "Avocado (Each)", "price": 1.99, "category": "Grocery", "stock": 100, "emoji": "🥑"},
    {"id": 6, "name": "Potato Chips", "price": 2.99, "category": "Snacks", "stock": 35, "emoji": "🥔"},
    {"id": 7, "name": "OLED Smart TV", "price": 899.99, "category": "Electronics", "stock": 2, "emoji": "📺"},
    {"id": 8, "name": "Dark Chocolate", "price": 4.49, "category": "Snacks", "stock": 10, "emoji": "🍫"}
]

if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ====== FEATURE 2 & 3: AUTHENTICATION & SIDEBAR ======
st.sidebar.title("🔐 User Account")
if not st.session_state.logged_in:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.sidebar.success(f"Welcome back, {username}!")
            st.rerun()
else:
    st.sidebar.success("✅ Logged in as User")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.cart = []
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.title("⚙️ Filters")

# ====== FEATURE 4: CATEGORY FILTERING ======
categories = ["All"] + sorted(list(set([p['category'] for p in products])))
selected_category = st.sidebar.selectbox("Filter by Category", categories)

# ====== FEATURE 5: SEARCH BAR ======
st.title("🛒 QuickCart Pro Edition")
search_query = st.text_input("🔍 Search for products...", "")

# Filtering Logic
filtered_products = [p for p in products if (selected_category == "All" or p['category'] == selected_category)]
if search_query:
    filtered_products = [p for p in filtered_products if search_query.lower() in p['name'].lower()]

col1, col2 = st.columns([2.5, 1])

# ====== FEATURE 6: DYNAMIC INVENTORY & ALERTS ======
def add_to_cart(product):
    if not st.session_state.logged_in:
        st.toast("Please log in to add items to cart!", icon='⚠️')
        return
    st.session_state.cart.append(product)
    st.toast(f"Added {product['name']} to cart!", icon='✅')

with col1:
    st.subheader(f"📦 Products ({len(filtered_products)} items found)")
    if len(filtered_products) == 0:
        st.warning("No products found matching your search.")
        
    for i in range(0, len(filtered_products), 3):
        row = st.columns(3)
        for j, product in enumerate(filtered_products[i:i+3]):
            with row[j]:
                st.markdown(f"""
                <div class="product-card">
                    <h1 style='font-size: 3.5rem; margin: 0;'>{product['emoji']}</h1>
                    <h4>{product['name']}</h4>
                    <p class="price-tag">${product['price']}</p>
                    <p class="stock-tag">Only {product['stock']} left in stock!</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Add to Cart 🛒", key=f"add_{product['id']}", use_container_width=True):
                    add_to_cart(product)
                st.write("") 

# ====== FEATURE 7: CHECKOUT PROCESSING SIMULATION ======
with col2:
    st.subheader("🛒 Your Cart")
    st.markdown("---")
    
    if len(st.session_state.cart) == 0:
        st.info("Your cart is empty.")
    else:
        total = 0
        for item in st.session_state.cart:
            st.markdown(f"**{item['emoji']} {item['name']}** <br> <span style='color:#00ffaa;'>${item['price']}</span>", unsafe_allow_html=True)
            total += item['price']
            
        st.markdown("---")
        st.markdown(f"<h3 style='text-align: right; color:#ff4b4b;'>Total: ${total:.2f}</h3>", unsafe_allow_html=True)
        
        if st.button("💳 Secure Checkout", type="primary", use_container_width=True):
            with st.spinner("Processing Payment..."):
                time.sleep(2) # Simulate API call
            st.success("Payment successful! Order shipped.")
            st.balloons()
            st.session_state.cart = []
        
        if st.button("🗑️ Clear Cart", use_container_width=True):
            st.session_state.cart = []
            st.rerun()

# ====== FEATURE 8: APP METRICS SYSTEM ======
st.markdown("---")
st.caption("Backend Server Metrics (DevOps Monitoring Simulator)")
m1, m2, m3, m4 = st.columns(4)
m1.metric(label="Server Uptime", value="99.98%", delta="0.02%")
m2.metric(label="Active Users", value="1,204", delta="+14")
m3.metric(label="API Latency", value="42ms", delta="-5ms")
m4.metric(label="DB Queries/sec", value="850", delta="120")
