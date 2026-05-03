import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="My Profile - QuickCart", page_icon="👤", layout="centered")

st.markdown("""
<style>
html, body, .stApp { background: #0a0a0a; color: #f1f1f1; }
div.stButton > button { background: #ff4b2b; color: white; border: none; border-radius: 10px; font-weight: 600; }
.profile-header { background: linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:16px; padding:30px; text-align:center; margin-bottom:20px;
    border:1px solid #2a2a4e; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get('username'):
    st.warning("Please login first.")
    st.page_link("app.py", label="Go to Storefront", icon="🏪"); st.stop()

username = st.session_state.username
conn = get_connection()

user_row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
user = dict(user_row) if user_row else {}

orders_count = conn.execute("SELECT COUNT(*) FROM orders WHERE username=?", (username,)).fetchone()[0]
total_spent = conn.execute("SELECT SUM(total_amount) FROM orders WHERE username=?", (username,)).fetchone()[0] or 0.0

st.markdown(f"""
<div class="profile-header">
  <div style="font-size:4rem">👤</div>
  <h2 style="margin:8px 0">@{username}</h2>
  <p style="color:#94a3b8">{user.get('email','') or 'Add your email below'}</p>
</div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
m1.metric("Total Orders", orders_count)
m2.metric("Total Spent", f"${total_spent:.2f}")
m3.metric("Member Since", str(user.get('created_at',''))[:10])

st.markdown("---")
st.subheader("✏️ Edit Profile")

with st.form("profile_form"):
    full_name = st.text_input("Full Name", value=user.get('full_name','') or '')
    email     = st.text_input("Email", value=user.get('email','') or '', placeholder="you@example.com")
    phone     = st.text_input("Phone", value=user.get('phone','') or '', placeholder="+91 98765 43210")
    address   = st.text_input("Delivery Address", value=user.get('address','') or '', placeholder="Flat/House No, Street, Area")
    c1, c2   = st.columns(2)
    city     = c1.text_input("City", value=user.get('city','Mumbai') or 'Mumbai')
    pincode  = c2.text_input("Pincode", value=user.get('pincode','400001') or '400001')
    
    if st.form_submit_button("💾 Save Profile", use_container_width=True):
        conn.execute('''UPDATE users SET full_name=?, email=?, phone=?, address=?, city=?, pincode=?
                        WHERE username=?''', (full_name, email, phone, address, city, pincode, username))
        conn.commit()
        # Also sync to session state for cart/order use
        st.session_state.address = address
        st.session_state.city = city
        st.session_state.pincode = pincode
        st.success("Profile updated successfully!")
        st.rerun()

st.markdown("---")
st.subheader("🎟️ Your Coupons")
coupons_df = pd.read_sql("SELECT code, discount_pct, min_order, max_uses, uses FROM coupons WHERE is_active=1", conn)
coupons_df['Remaining Uses'] = coupons_df['max_uses'] - coupons_df['uses']
coupons_df.columns = ['Coupon Code','Discount %','Min Order $','Max Uses','Uses','Remaining']
st.dataframe(coupons_df, hide_index=True, use_container_width=True)
st.caption("Use these codes at checkout to save on your orders!")

conn.close()
