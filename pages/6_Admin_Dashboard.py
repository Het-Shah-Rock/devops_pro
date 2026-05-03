import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(page_title="Admin Dashboard - QuickCart", page_icon="📊", layout="wide")

st.markdown("""
<style>
html, body, .stApp { background: #0a0a0a; color: #f1f1f1; }
div.stButton > button { background: #ff4b2b; color:white; border:none; border-radius:10px; font-weight:600; }
</style>
""", unsafe_allow_html=True)

if st.session_state.get('username') != 'admin':
    st.error("🔒 Access Denied: Admin only.")
    st.info("Login as **admin** from the storefront.")
    st.stop()

conn = get_connection()

st.title("📊 Admin Control Panel")
st.caption("QuickCart Enterprise Management System")

tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📦 Inventory", "🧾 Orders", "🎟️ Coupons"])

with tab1:
    orders_df = pd.read_sql("SELECT * FROM orders", conn)
    products_df = pd.read_sql("SELECT * FROM products", conn)

    total_rev = orders_df['total_amount'].sum() if len(orders_df) else 0
    total_discount = orders_df['discount_amount'].sum() if len(orders_df) else 0
    low_stock = len(products_df[products_df['stock'] < 10])
    out_of_stock = len(products_df[products_df['stock'] == 0])

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Orders", len(orders_df))
    m2.metric("Total Revenue", f"${total_rev:.2f}")
    m3.metric("Discounts Given", f"${total_discount:.2f}")
    m4.metric("Low Stock Items", low_stock, delta="⚠️ Alert" if low_stock>0 else "OK", delta_color="inverse")
    m5.metric("Out of Stock", out_of_stock, delta="❌ Critical" if out_of_stock>0 else "OK", delta_color="inverse")

    if len(orders_df) > 0:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Revenue by Category")
            items_df = pd.read_sql("""
                SELECT p.category, SUM(oi.quantity * oi.price) as revenue
                FROM order_items oi JOIN products p ON oi.product_id=p.id
                GROUP BY p.category ORDER BY revenue DESC
            """, conn)
            if not items_df.empty:
                st.bar_chart(items_df.set_index('category')['revenue'])
        with col2:
            st.subheader("🥇 Top Selling Products")
            top_products = pd.read_sql("""
                SELECT p.emoji, p.name, SUM(oi.quantity) as units_sold,
                       SUM(oi.quantity * oi.price) as revenue
                FROM order_items oi JOIN products p ON oi.product_id=p.id
                GROUP BY p.name ORDER BY units_sold DESC LIMIT 8
            """, conn)
            if not top_products.empty:
                st.dataframe(top_products, hide_index=True, use_container_width=True)

with tab2:
    st.subheader("📦 Product Inventory Manager")
    products_df = pd.read_sql("SELECT id, emoji, name, category, price, mrp, stock, is_deal, is_featured, discount_pct FROM products ORDER BY stock ASC", conn)

    col1, col2, col3 = st.columns(3)
    cat_filter = col1.selectbox("Filter Category", ["All"] + products_df['category'].unique().tolist())
    stock_filter = col2.selectbox("Stock Status", ["All", "Low Stock (<10)", "Out of Stock"])
    
    filtered = products_df
    if cat_filter != "All": filtered = filtered[filtered['category']==cat_filter]
    if stock_filter == "Low Stock (<10)": filtered = filtered[filtered['stock'] < 10]
    elif stock_filter == "Out of Stock": filtered = filtered[filtered['stock'] == 0]

    st.dataframe(filtered, hide_index=True, use_container_width=True)

    st.markdown("---")
    st.subheader("📥 Restock Product")
    r1, r2, r3 = st.columns(3)
    product_options = {f"{row['emoji']} {row['name']}": row['id'] for _, row in products_df.iterrows()}
    selected_product = r1.selectbox("Select Product", list(product_options.keys()))
    restock_qty = r2.number_input("Add Quantity", min_value=1, max_value=1000, value=50)
    if r3.button("✅ Restock", use_container_width=True):
        pid = product_options[selected_product]
        conn.execute("UPDATE products SET stock=stock+? WHERE id=?", (restock_qty, pid))
        conn.commit()
        st.success(f"Added {restock_qty} units to {selected_product}!")
        st.rerun()

with tab3:
    st.subheader("🧾 All Customer Orders")
    all_orders = pd.read_sql("""
        SELECT id, username, total_amount, discount_amount, coupon_used,
               delivery_address, city, payment_method, status, timestamp
        FROM orders ORDER BY timestamp DESC
    """, conn)
    
    if len(all_orders) == 0:
        st.info("No orders yet.")
    else:
        status_options = ["Order Placed", "Preparing Order", "Out for Delivery", "Delivered", "Cancelled"]
        
        for _, order in all_orders.iterrows():
            with st.expander(f"Order #{order['id']} | {order['username']} | ${order['total_amount']:.2f} | {order['timestamp'][:16]}"):
                c1, c2 = st.columns(2)
                c1.write(f"**Customer:** {order['username']}")
                c1.write(f"**City:** {order['city']}")
                c1.write(f"**Payment:** {order['payment_method']}")
                c2.write(f"**Coupon:** {order['coupon_used'] or 'None'}")
                c2.write(f"**Discount:** ${order['discount_amount']:.2f}")
                
                new_status = st.selectbox("Update Status:", status_options, 
                                           index=status_options.index(order['status']) if order['status'] in status_options else 0,
                                           key=f"status_{order['id']}")
                if st.button("Update", key=f"upd_{order['id']}"):
                    conn.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order['id']))
                    conn.commit()
                    st.success("Status updated!")

with tab4:
    st.subheader("🎟️ Coupon Management")
    coupons = pd.read_sql("SELECT * FROM coupons", conn)
    st.dataframe(coupons, hide_index=True, use_container_width=True)

    st.markdown("---")
    st.subheader("➕ Add New Coupon")
    n1, n2, n3, n4 = st.columns(4)
    new_code = n1.text_input("Code", placeholder="SUMMER30")
    new_pct = n2.number_input("Discount %", 1, 90, 10)
    new_min = n3.number_input("Min Order $", 0.0, 1000.0, 0.0)
    new_max = n4.number_input("Max Uses", 1, 10000, 100)
    if st.button("Create Coupon"):
        try:
            conn.execute("INSERT INTO coupons (code, discount_pct, min_order, max_uses) VALUES (?,?,?,?)",
                         (new_code.upper(), new_pct, new_min, new_max))
            conn.commit()
            st.success(f"Coupon {new_code.upper()} created!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

conn.close()
