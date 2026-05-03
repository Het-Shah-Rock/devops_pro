import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="Cart - QuickCart", page_icon="🛒", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, .stApp { background: #0a0a0a; font-family: 'Inter', sans-serif; color: #f1f1f1; }
div.stButton > button { background: #ff4b2b; color: white; border: none; border-radius: 10px; padding: 10px; font-weight: 600; }
div.stButton > button:hover { background: #e03520; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get('username'):
    st.warning("Please login on the Storefront first.")
    st.page_link("app.py", label="Go to Storefront", icon="🏪")
    st.stop()

if not st.session_state.get('cart'):
    st.info("Your cart is empty.")
    st.page_link("app.py", label="Continue Shopping", icon="🛒")
    st.stop()

conn = get_connection()
all_products = pd.read_sql("SELECT * FROM products", conn)

st.title("🛒 Your Cart")

# Delivery Address
with st.expander("📍 Delivery Address", expanded=True):
    c1, c2, c3 = st.columns(3)
    addr = c1.text_input("Address", value=st.session_state.get('address',''), placeholder="House No, Street")
    city = c2.text_input("City", value=st.session_state.get('city','Mumbai'))
    pin  = c3.text_input("Pincode", value=st.session_state.get('pincode','400001'))
    if st.button("Save Address"):
        st.session_state.address = addr
        st.session_state.city = city
        st.session_state.pincode = pin
        st.toast("Address saved!", icon="✅")

st.markdown("---")
subtotal = 0.0

for pid, qty in list(st.session_state.cart.items()):
    p_rows = all_products[all_products['id'] == pid]
    if p_rows.empty: continue
    p = p_rows.iloc[0]
    item_total = p['price'] * qty
    subtotal += item_total
    c1, c2, c3, c4 = st.columns([1, 4, 2, 1])
    c1.markdown(f"<div style='font-size:2.2rem;text-align:center'>{p['emoji']}</div>", unsafe_allow_html=True)
    c2.markdown(f"**{p['name']}**")
    c2.caption(f"{p['unit']} · {p['category']}")
    with c3:
        q1, q2, q3 = st.columns(3)
        if q1.button("−", key=f"dec_{pid}"):
            if st.session_state.cart[pid] > 1: st.session_state.cart[pid] -= 1
            else: del st.session_state.cart[pid]
            st.rerun()
        q2.markdown(f"<p style='text-align:center;font-weight:700;padding:6px 0'>{qty}</p>", unsafe_allow_html=True)
        if q3.button("＋", key=f"inc_{pid}"):
            st.session_state.cart[pid] += 1; st.rerun()
    c4.markdown(f"<p style='color:#00e676;font-weight:700'>${item_total:.2f}</p>", unsafe_allow_html=True)
    if c4.button("🗑", key=f"rm_{pid}"):
        del st.session_state.cart[pid]; st.rerun()
    st.divider()

# Coupon
st.markdown("#### 🎟️ Coupon Code")
cc1, cc2 = st.columns([3,1])
coupon_input = cc1.text_input("Coupon", placeholder="e.g. SAVE20", label_visibility="collapsed")
if cc2.button("Apply", use_container_width=True) and coupon_input:
    c = conn.cursor()
    row = c.execute("SELECT * FROM coupons WHERE code=? AND is_active=1", (coupon_input.upper(),)).fetchone()
    if not row: st.error("Invalid coupon.")
    elif subtotal < row['min_order']: st.warning(f"Min order ${row['min_order']:.2f} required.")
    elif row['uses'] >= row['max_uses']: st.error("Coupon fully redeemed.")
    else:
        st.session_state.applied_coupon = coupon_input.upper()
        st.session_state.coupon_pct = row['discount_pct']
        st.success(f"✅ {coupon_input.upper()} applied — {row['discount_pct']}% off!")
        st.rerun()

discount_amount = 0.0
if st.session_state.get('applied_coupon'):
    discount_amount = subtotal * st.session_state.coupon_pct / 100
    st.success(f"🎟️ **{st.session_state.applied_coupon}** ({st.session_state.coupon_pct}% off) → -${discount_amount:.2f}")
    if st.button("Remove Coupon"):
        st.session_state.applied_coupon = None; st.session_state.coupon_pct = 0; st.rerun()

delivery_fee = 0.0 if subtotal >= 30 else 2.99
total = subtotal - discount_amount + delivery_fee

st.markdown("---")
st.markdown("#### 📊 Order Summary")
s1, s2 = st.columns(2)
s1.markdown("Subtotal\nDiscount\nDelivery\n**Total**")
s2.markdown(f"${subtotal:.2f}\n-${discount_amount:.2f}\n{'FREE 🎉' if delivery_fee==0 else f'${delivery_fee:.2f}'}\n**${total:.2f}**")

st.markdown("---")
payment = st.radio("💳 Payment", ["UPI / GPay", "Credit / Debit Card", "Cash on Delivery"], horizontal=True)

if st.button("🚀 Place Order", type="primary", use_container_width=True):
    if not st.session_state.get('address'):
        st.error("Please enter your delivery address.")
    else:
        db = get_connection(); c = db.cursor()
        c.execute('''INSERT INTO orders (username, total_amount, discount_amount, coupon_used,
                    delivery_address, city, pincode, payment_method) VALUES (?,?,?,?,?,?,?,?)''',
                  (st.session_state.username, total, discount_amount,
                   st.session_state.get('applied_coupon',''),
                   st.session_state.address, st.session_state.city,
                   st.session_state.pincode, payment))
        order_id = c.lastrowid
        for pid, qty in st.session_state.cart.items():
            p = all_products[all_products['id']==pid].iloc[0]
            c.execute("INSERT INTO order_items (order_id,product_id,quantity,price) VALUES (?,?,?,?)",
                      (order_id, pid, qty, p['price']))
            c.execute("UPDATE products SET stock=stock-? WHERE id=?", (qty, pid))
        if st.session_state.get('applied_coupon'):
            c.execute("UPDATE coupons SET uses=uses+1 WHERE code=?", (st.session_state.applied_coupon,))
        db.commit(); db.close()
        st.session_state.last_order_id = order_id
        st.session_state.last_order_total = total
        st.session_state.cart = {}
        st.session_state.applied_coupon = None
        st.session_state.coupon_pct = 0
        st.switch_page("pages/2_Order_Confirmation.py")

st.button("← Continue Shopping", on_click=lambda: st.switch_page("app.py"))
conn.close()
