import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="QuickCart - 10-Min Delivery", page_icon="🛒", layout="wide")

# ========= GLOBAL CSS =========
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, .stApp { background-color: #0a0a0a; font-family: 'Inter', sans-serif; color: #f1f1f1; }
.hero { background: linear-gradient(135deg, #ff416c, #ff4b2b);
    padding: 40px 30px; border-radius: 20px; margin-bottom: 30px; }
.hero h1 { font-size: 2.8rem; font-weight: 800; color: white; margin: 0; }
.hero p { color: rgba(255,255,255,0.85); font-size: 1.15rem; margin: 8px 0 20px 0; }
.cat-card { background: #1a1a2e; border-radius: 14px; padding: 18px;
    text-align: center; cursor: pointer; transition: all 0.2s;
    border: 1px solid #2a2a3e; }
.cat-card:hover { border-color: #ff4b2b; transform: translateY(-3px); }
.prod-card { background: #111827; border-radius: 14px; padding: 18px;
    border: 1px solid #1e293b; transition: all 0.25s; height: 100%; }
.prod-card:hover { border-color: #ff4b2b; box-shadow: 0 8px 30px rgba(255,75,43,0.15); }
.price-now { font-size: 1.35rem; font-weight: 700; color: #00e676; }
.price-mrp { font-size: 0.85rem; color: #888; text-decoration: line-through; }
.badge-deal { background: #ff4b2b; color: white; border-radius: 6px;
    padding: 2px 8px; font-size: 0.75rem; font-weight: 600; }
.badge-featured { background: #7c3aed; color: white; border-radius: 6px;
    padding: 2px 8px; font-size: 0.75rem; font-weight: 600; }
.delivery-tag { background: #0d2137; border: 1px solid #1a4a6e;
    border-radius: 8px; padding: 8px 14px; color: #38bdf8; font-size: 0.85rem; }
.section-title { font-size: 1.5rem; font-weight: 700; margin: 20px 0 12px 0; }
div.stButton > button { background: #ff4b2b; color: white; border: none;
    border-radius: 10px; padding: 10px; font-weight: 600; width: 100%; }
div.stButton > button:hover { background: #e03520; }
.star { color: #fbbf24; }
</style>
""", unsafe_allow_html=True)

# ========= SESSION STATE =========
for key, val in [('cart', {}), ('username', None), ('address', ''), ('city', 'Mumbai'), ('pincode', '400001')]:
    if key not in st.session_state:
        st.session_state[key] = val

# ========= SIDEBAR =========
with st.sidebar:
    st.markdown("## 🛒 QuickCart")
    st.markdown("---")
    if not st.session_state.username:
        st.subheader("🔐 Login")
        user = st.text_input("Username", placeholder="e.g. rahul123")
        if st.button("Login / Register"):
            if user.strip():
                conn = get_connection()
                conn.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (user.strip(),))
                conn.commit()
                conn.close()
                st.session_state.username = user.strip()
                st.rerun()
    else:
        st.success(f"👋 Hey, **{st.session_state.username}**!")
        if st.button("Logout"):
            st.session_state.username = None
            st.session_state.cart = {}
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"### 📍 Delivering to")
    st.markdown(f"**{st.session_state.city}** — {st.session_state.pincode}")
    st.markdown('<p class="delivery-tag">⚡ Delivery in <strong>10-15 mins</strong></p>', unsafe_allow_html=True)
    st.markdown("---")
    total_items = sum(st.session_state.cart.values())
    if total_items > 0:
        st.markdown(f"### 🛍️ Cart: {total_items} items")
        st.page_link("pages/1_Cart.py", label="View Cart & Checkout →", icon="🛒")

# ========= FETCH DATA =========
conn = get_connection()
all_products = pd.read_sql("SELECT * FROM products", conn)
conn.close()

# ========= HERO BANNER =========
st.markdown("""
<div class="hero">
  <h1>⚡ Groceries in 10 Minutes</h1>
  <p>Fresh produce, daily essentials, snacks & more — delivered to your door faster than you can say "hungry".</p>
  <span style="background:rgba(255,255,255,0.2);padding:8px 18px;border-radius:20px;color:white;font-weight:600;">
    🚀 Free delivery on orders above $30
  </span>
</div>
""", unsafe_allow_html=True)

# ========= SEARCH =========
search = st.text_input("🔍 Search products, brands, categories...", placeholder="Try 'apples', 'milk', 'chips'...")

if search:
    results = all_products[all_products['name'].str.contains(search, case=False) |
                            all_products['category'].str.contains(search, case=False)]
    st.markdown(f"### 🔍 Results for \"{search}\" ({len(results)} found)")
    def add_to_cart(pid):
        if not st.session_state.username:
            st.toast("Please login first!", icon="⚠️"); return
        st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
        st.toast("Added to cart!", icon="✅")

    for i in range(0, len(results), 4):
        cols = st.columns(4)
        for j, (_, p) in enumerate(results.iloc[i:i+4].iterrows()):
            with cols[j]:
                badges = ""
                if p['is_deal']: badges += f'<span class="badge-deal">🔥 {p["discount_pct"]}% OFF</span> '
                if p['is_featured']: badges += '<span class="badge-featured">⭐ Featured</span>'
                st.markdown(f"""<div class="prod-card">
                    <div style="text-align:center;font-size:3rem;">{p['emoji']}</div>
                    <div style="margin:6px 0">{badges}</div>
                    <p style="font-weight:600;margin:6px 0;font-size:0.95rem;">{p['name']}</p>
                    <p style="color:#888;font-size:0.8rem;">{p['unit']}</p>
                    <span class="star">{'★' * int(p['rating'])}{'☆' * (5-int(p['rating']))}</span>
                    <span style="color:#888;font-size:0.8rem;"> ({p['review_count']})</span><br>
                    <span class="price-now">${p['price']:.2f}</span>
                    <span class="price-mrp"> MRP ${p['mrp']:.2f}</span>
                </div>""", unsafe_allow_html=True)
                if st.button("Add to Cart", key=f"s_{p['id']}", use_container_width=True):
                    add_to_cart(p['id'])
    st.stop()

# ========= CATEGORIES =========
st.markdown('<p class="section-title">🏪 Shop by Category</p>', unsafe_allow_html=True)
categories = all_products['category'].unique().tolist()
cat_emojis = {"Fruits & Vegetables":"🥦", "Dairy & Eggs":"🥛", "Bakery":"🍞",
              "Meat & Seafood":"🍗", "Snacks & Drinks":"🍿", "Household":"🧹", "Electronics":"📱"}
cols = st.columns(len(categories))
selected_cat = st.session_state.get("selected_cat", "All")
for i, cat in enumerate(categories):
    with cols[i]:
        emoji = cat_emojis.get(cat, "📦")
        short = cat.split("&")[0].strip()
        if st.button(f"{emoji}\n{short}", key=f"cat_{i}", use_container_width=True):
            st.session_state.selected_cat = cat
            st.rerun()

# ========= DEALS STRIP =========
st.markdown('<p class="section-title">🔥 Today\'s Hot Deals</p>', unsafe_allow_html=True)
deals = all_products[all_products['is_deal'] == 1].head(6)

def add_to_cart(pid):
    if not st.session_state.username:
        st.toast("Please login first!", icon="⚠️"); return
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
    st.toast("Added to cart!", icon="✅")

deal_cols = st.columns(len(deals))
for i, (_, p) in enumerate(deals.iterrows()):
    with deal_cols[i]:
        st.markdown(f"""<div class="prod-card" style="border-color:#ff4b2b22;">
            <div style="text-align:center;font-size:2.5rem;">{p['emoji']}</div>
            <span class="badge-deal">🔥 {p['discount_pct']}% OFF</span>
            <p style="font-weight:600;font-size:0.9rem;margin:6px 0;">{p['name']}</p>
            <span class="price-now">${p['price']:.2f}</span>
            <span class="price-mrp"> ${p['mrp']:.2f}</span>
        </div>""", unsafe_allow_html=True)
        if st.button(f"Add", key=f"deal_{p['id']}", use_container_width=True):
            add_to_cart(p['id'])

# ========= FEATURED PRODUCTS =========
st.markdown('<p class="section-title">⭐ Featured Products</p>', unsafe_allow_html=True)
featured = all_products[all_products['is_featured'] == 1].head(8)
for i in range(0, len(featured), 4):
    row_cols = st.columns(4)
    for j, (_, p) in enumerate(featured.iloc[i:i+4].iterrows()):
        with row_cols[j]:
            badges = ""
            if p['is_deal']: badges += f'<span class="badge-deal">🔥 {p["discount_pct"]}% OFF</span> '
            badges += '<span class="badge-featured">⭐ Featured</span>'
            st.markdown(f"""<div class="prod-card">
                <div style="text-align:center;font-size:3.5rem;">{p['emoji']}</div>
                <div style="margin:6px 0;">{badges}</div>
                <p style="font-weight:600;margin:6px 0;">{p['name']}</p>
                <p style="color:#888;font-size:0.82rem;">{p['unit']} · {p['subcategory']}</p>
                <p style="color:#aaa;font-size:0.82rem;height:36px;overflow:hidden;">{p['description'][:70]}...</p>
                <span class="star">{'★' * int(p['rating'])}{'☆' * (5-int(p['rating']))}</span>
                <span style="color:#888;font-size:0.8rem;"> ({p['review_count']})</span><br>
                <span class="price-now">${p['price']:.2f}</span>
                <span class="price-mrp"> MRP ${p['mrp']:.2f}</span>
            </div>""", unsafe_allow_html=True)
            if st.button("+ Add to Cart", key=f"feat_{p['id']}", use_container_width=True):
                add_to_cart(p['id'])
            st.write("")

# ========= BROWSE BY CATEGORY =========
st.markdown("---")
display_cat = st.session_state.get("selected_cat", "All")
st.markdown(f'<p class="section-title">📦 All Products — {display_cat}</p>', unsafe_allow_html=True)

cat_filter = st.radio("Category:", ["All"] + categories, horizontal=True,
                       index=(["All"] + categories).index(display_cat) if display_cat in categories else 0)
if cat_filter != display_cat:
    st.session_state.selected_cat = cat_filter

filtered = all_products if cat_filter == "All" else all_products[all_products['category'] == cat_filter]

for i in range(0, len(filtered), 4):
    row_cols = st.columns(4)
    for j, (_, p) in enumerate(filtered.iloc[i:i+4].iterrows()):
        with row_cols[j]:
            badges = ""
            if p['is_deal']: badges += f'<span class="badge-deal">🔥 {p["discount_pct"]}% OFF</span> '
            if p['is_featured']: badges += '<span class="badge-featured">⭐</span>'
            qty = st.session_state.cart.get(p['id'], 0)
            st.markdown(f"""<div class="prod-card">
                <div style="text-align:center;font-size:3rem;">{p['emoji']}</div>
                <div style="margin:4px 0;">{badges}</div>
                <p style="font-weight:600;margin:6px 0;font-size:0.92rem;">{p['name']}</p>
                <p style="color:#888;font-size:0.8rem;">{p['unit']}</p>
                <span class="star">{'★'*int(p['rating'])}{'☆'*(5-int(p['rating']))}</span>
                <span style="color:#888;font-size:0.78rem;"> ({p['review_count']})</span><br>
                <span class="price-now">${p['price']:.2f}</span>
                <span class="price-mrp"> ${p['mrp']:.2f}</span>
                <p style="color:#ffa500;font-size:0.78rem;">Stock: {p['stock']}</p>
            </div>""", unsafe_allow_html=True)
            disabled = p['stock'] <= 0
            if qty == 0:
                if st.button("+ Add", key=f"all_{p['id']}", disabled=disabled, use_container_width=True):
                    add_to_cart(p['id'])
            else:
                c1, c2, c3 = st.columns([1,2,1])
                with c1:
                    if st.button("−", key=f"dec_{p['id']}"):
                        if st.session_state.cart[p['id']] > 1:
                            st.session_state.cart[p['id']] -= 1
                        else:
                            del st.session_state.cart[p['id']]
                        st.rerun()
                with c2:
                    st.markdown(f"<p style='text-align:center;margin:8px 0;font-weight:700;color:#00e676'>{qty}</p>", unsafe_allow_html=True)
                with c3:
                    if st.button("＋", key=f"inc_{p['id']}"):
                        add_to_cart(p['id'])
                        st.rerun()
            st.write("")
