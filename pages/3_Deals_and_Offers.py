import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="Deals - QuickCart", page_icon="🔥", layout="wide")

st.markdown("""
<style>
html, body, .stApp { background: #0a0a0a; font-family: 'Inter', sans-serif; color: #f1f1f1; }
.deal-card { background: #111827; border-radius: 14px; padding: 20px;
    border: 1px solid #ff4b2b44; transition: all 0.25s; }
.deal-card:hover { border-color: #ff4b2b; transform: translateY(-4px); box-shadow: 0 8px 30px rgba(255,75,43,0.2); }
.badge-deal { background: #ff4b2b; color: white; border-radius: 6px; padding: 3px 10px; font-size: 0.8rem; font-weight:700; }
.price-now { font-size: 1.4rem; font-weight: 700; color: #00e676; }
.price-mrp { font-size: 0.85rem; color: #888; text-decoration: line-through; }
div.stButton > button { background: #ff4b2b; color: white; border: none; border-radius: 10px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(135deg,#b91c1c,#ff4b2b); border-radius:16px; padding:30px; margin-bottom:24px; text-align:center">
  <h1 style="color:white;margin:0">🔥 Today's Hot Deals</h1>
  <p style="color:rgba(255,255,255,0.85);margin:8px 0">Limited time offers — grab them before they're gone!</p>
  <p style="color:#fbbf24;font-weight:600">🕐 Deals refresh every 24 hours</p>
</div>
""", unsafe_allow_html=True)

# Coupon banner
st.markdown("""
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px">
  <div style="background:#1a2e1a;border:1px solid #00e676;border-radius:10px;padding:12px 20px;flex:1">
    <p style="color:#00e676;font-weight:700;margin:0">🎟️ WELCOME10</p>
    <p style="color:#94a3b8;margin:0;font-size:0.85rem">10% off on your first order</p>
  </div>
  <div style="background:#1a1a2e;border:1px solid #7c3aed;border-radius:10px;padding:12px 20px;flex:1">
    <p style="color:#a78bfa;font-weight:700;margin:0">🎟️ SAVE20</p>
    <p style="color:#94a3b8;margin:0;font-size:0.85rem">20% off on orders above $50</p>
  </div>
  <div style="background:#1a2820;border:1px solid #fbbf24;border-radius:10px;padding:12px 20px;flex:1">
    <p style="color:#fbbf24;font-weight:700;margin:0">🎟️ QUICKCART</p>
    <p style="color:#94a3b8;margin:0;font-size:0.85rem">25% off on orders above $200</p>
  </div>
  <div style="background:#1e1a10;border:1px solid #f59e0b;border-radius:10px;padding:12px 20px;flex:1">
    <p style="color:#f59e0b;font-weight:700;margin:0">🎟️ FLAT50</p>
    <p style="color:#94a3b8;margin:0;font-size:0.85rem">15% off on orders above $100</p>
  </div>
</div>
""", unsafe_allow_html=True)

conn = get_connection()
deals_df = pd.read_sql("SELECT * FROM products WHERE is_deal=1 ORDER BY discount_pct DESC", conn)
conn.close()

def add_to_cart(pid):
    if not st.session_state.get('username'):
        st.toast("Please login first!", icon="⚠️"); return
    if 'cart' not in st.session_state: st.session_state.cart = {}
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
    st.toast("Added to cart!", icon="✅")

st.markdown(f"### 🛍️ {len(deals_df)} deals available today")

# Sort options
sort_by = st.selectbox("Sort by:", ["Biggest Discount", "Lowest Price", "Highest Rating", "Best Seller"])
if sort_by == "Biggest Discount": deals_df = deals_df.sort_values('discount_pct', ascending=False)
elif sort_by == "Lowest Price": deals_df = deals_df.sort_values('price')
elif sort_by == "Highest Rating": deals_df = deals_df.sort_values('rating', ascending=False)
elif sort_by == "Best Seller": deals_df = deals_df.sort_values('review_count', ascending=False)

for i in range(0, len(deals_df), 4):
    cols = st.columns(4)
    for j, (_, p) in enumerate(deals_df.iloc[i:i+4].iterrows()):
        savings = p['mrp'] - p['price']
        with cols[j]:
            st.markdown(f"""<div class="deal-card">
                <div style="text-align:center;font-size:3.5rem;">{p['emoji']}</div>
                <span class="badge-deal">🔥 {p['discount_pct']}% OFF</span>
                <p style="font-weight:700;margin:8px 0;font-size:0.95rem;">{p['name']}</p>
                <p style="color:#888;font-size:0.82rem;">{p['unit']} · {p['category']}</p>
                <span style="color:#fbbf24">{'★' * int(p['rating'])}{'☆' * (5-int(p['rating']))}</span>
                <span style="color:#888;font-size:0.8rem"> ({p['review_count']})</span><br>
                <span class="price-now">${p['price']:.2f}</span>
                <span class="price-mrp"> ${p['mrp']:.2f}</span>
                <p style="color:#00e676;font-size:0.85rem;margin:4px 0">You save ${savings:.2f}!</p>
                <p style="color:#ffa500;font-size:0.78rem;margin:0">Only {p['stock']} left</p>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Add to Cart 🛒", key=f"deal_{p['id']}", use_container_width=True):
                add_to_cart(p['id'])
            st.write("")
