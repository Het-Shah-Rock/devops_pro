import streamlit as st

# Setup page configuration
st.set_page_config(page_title="QuickCart - Lightning Fast Delivery!", page_icon="🛍️", layout="wide")

# Custom CSS for UI polishing
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Inter', sans-serif;
    }
    .main-header {
        color: #ff4b4b;
        text-align: center;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0px;
    }
    .sub-header {
        text-align: center;
        color: #6c757d;
        margin-top: -10px;
        margin-bottom: 40px;
    }
    .product-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .price-tag {
        font-size: 1.5rem;
        font-weight: bold;
        color: #28a745;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🛒 QuickCart</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-header'>Groceries delivered in 10 minutes!</h4>", unsafe_allow_html=True)

# Catalog database
products = [
    {"id": 1, "name": "Fresh Apples (1kg)", "price": 4.99, "emoji": "🍎"},
    {"id": 2, "name": "Organic Milk (1L)", "price": 2.49, "emoji": "🥛"},
    {"id": 3, "name": "Whole Wheat Bread", "price": 3.99, "emoji": "🍞"},
    {"id": 4, "name": "Farm Eggs (12-pack)", "price": 4.29, "emoji": "🥚"},
    {"id": 5, "name": "Avocado (Each)", "price": 1.99, "emoji": "🥑"},
    {"id": 6, "name": "Potato Chips", "price": 2.99, "emoji": "🥔"},
]

# Session state to hold cart items
if 'cart' not in st.session_state:
    st.session_state.cart = []

def add_to_cart(product):
    st.session_state.cart.append(product)
    st.toast(f"Added {product['name']} to cart!", icon='✅')

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🛍️ Shop Aisles")
    st.markdown("---")
    
    # Iterate through products in rows of 2
    for i in range(0, len(products), 2):
        row = st.columns(2)
        for j, product in enumerate(products[i:i+2]):
            with row[j]:
                st.markdown(f"""
                <div class="product-card">
                    <h1 style='font-size: 4rem; margin: 0;'>{product['emoji']}</h1>
                    <h3>{product['name']}</h3>
                    <p class="price-tag">${product['price']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Add to Cart", key=f"add_{product['id']}", use_container_width=True):
                    add_to_cart(product)
                st.write("") # Spacer

with col2:
    st.subheader("🛒 Your Cart")
    st.markdown("---")
    
    if len(st.session_state.cart) == 0:
        st.info("Your cart is empty. Start shopping!")
    else:
        total = 0
        for item in st.session_state.cart:
            st.write(f"**{item['emoji']} {item['name']}** - ${item['price']}")
            total += item['price']
            
        st.markdown("---")
        st.markdown(f"<h3 style='text-align: right;'>Total: ${total:.2f}</h3>", unsafe_allow_html=True)
        
        if st.button("checkout & Pay", type="primary", use_container_width=True):
            st.success("Payment successful! Your order is on the way.")
            st.code("Order ID: #QC-9876543")
            st.session_state.cart = []
            st.balloons()
        
        if st.button("Clear Cart", use_container_width=True):
            st.session_state.cart = []
            st.rerun()

st.sidebar.title("DevOps Tech Stack Demo")
st.sidebar.info("""
This application is part of a full CI/CD pipeline using:
- **Git/GitHub** (Version Control)
- **Jenkins** (CI/CD Pipeline)
- **Docker** (Containerization)
- **Kubernetes** (Orchestration)
- **Python/Streamlit** (App)
""")
