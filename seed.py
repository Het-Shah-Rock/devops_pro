from database import get_connection, init_db

PRODUCTS = [
    # name, price, mrp, category, subcategory, stock, emoji, desc, unit, featured, is_deal, discount_pct, rating, reviews
    # ---- FRUITS & VEGETABLES ----
    ("Organic Red Apples", 4.99, 6.99, "Fruits & Vegetables", "Fruits", 150, "🍎", "Fresh, crispy organic red apples sourced from Himalayan farms.", "1 kg", 1, 1, 28, 4.5, 312),
    ("Ripe Bananas", 2.49, 2.99, "Fruits & Vegetables", "Fruits", 200, "🍌", "Sweet, ripe bananas — perfect for smoothies and snacking.", "6 pcs", 1, 0, 16, 4.3, 189),
    ("Avocado", 1.99, 2.49, "Fruits & Vegetables", "Fruits", 80, "🥑", "Creamy Hass avocados, hand-picked for perfect ripeness.", "1 pc", 0, 0, 20, 4.7, 256),
    ("Baby Carrots", 1.49, 1.99, "Fruits & Vegetables", "Vegetables", 120, "🥕", "Tender baby carrots, pre-washed and ready to eat.", "500 g", 0, 1, 25, 4.2, 98),
    ("Broccoli", 2.29, 2.79, "Fruits & Vegetables", "Vegetables", 60, "🥦", "Farm-fresh broccoli crowns, rich in nutrients.", "1 head", 0, 0, 18, 4.4, 134),
    ("Cherry Tomatoes", 3.49, 3.99, "Fruits & Vegetables", "Vegetables", 90, "🍅", "Sweet vine-ripened cherry tomatoes, bursting with flavor.", "250 g", 1, 0, 12, 4.6, 201),
    ("Spinach Leaves", 2.99, 3.49, "Fruits & Vegetables", "Leafy Greens", 70, "🥬", "Tender baby spinach, triple-washed and ready to use.", "200 g", 0, 1, 14, 4.3, 167),
    ("Yellow Bell Pepper", 1.99, 2.49, "Fruits & Vegetables", "Vegetables", 100, "🫑", "Crisp, sweet yellow bell peppers. Great for salads.", "1 pc", 0, 0, 20, 4.5, 88),
    ("Mango (Alphonso)", 6.99, 8.99, "Fruits & Vegetables", "Fruits", 40, "🥭", "King of mangoes — the legendary Alphonso from Ratnagiri.", "3 pcs", 1, 1, 22, 4.9, 543),
    ("Watermelon", 5.99, 7.99, "Fruits & Vegetables", "Fruits", 30, "🍉", "Juicy, seedless watermelon. Perfect for summer.", "1 pc", 0, 1, 25, 4.4, 221),

    # ---- DAIRY & EGGS ----
    ("Full Cream Milk", 3.99, 4.49, "Dairy & Eggs", "Milk", 50, "🥛", "Farm-fresh full cream milk, pasteurized and homogenized.", "1 L", 1, 0, 11, 4.6, 432),
    ("Farm Eggs (Brown)", 4.29, 4.99, "Dairy & Eggs", "Eggs", 100, "🥚", "Free-range, cage-free brown eggs from happy hens.", "12 pcs", 1, 0, 14, 4.7, 567),
    ("Amul Butter", 3.49, 3.99, "Dairy & Eggs", "Butter", 75, "🧈", "Creamy, salted Amul butter. India's favourite.", "100 g", 0, 0, 12, 4.8, 890),
    ("Greek Yogurt", 1.79, 2.29, "Dairy & Eggs", "Yogurt", 90, "🥣", "Thick, creamy Greek-style yogurt, rich in protein.", "200 g", 1, 1, 21, 4.5, 312),
    ("Mozzarella Cheese", 5.99, 6.99, "Dairy & Eggs", "Cheese", 40, "🧀", "Fresh mozzarella — perfect for pizzas and salads.", "200 g", 0, 0, 14, 4.6, 198),
    ("Paneer (Cottage Cheese)", 4.49, 4.99, "Dairy & Eggs", "Cheese", 55, "🧀", "Fresh, soft paneer — the staple of Indian cooking.", "200 g", 1, 0, 10, 4.7, 621),

    # ---- BAKERY ----
    ("Whole Wheat Bread", 3.49, 3.99, "Bakery", "Bread", 45, "🍞", "Freshly baked 100% whole wheat bread loaf.", "400 g", 1, 0, 12, 4.5, 289),
    ("Butter Croissants", 4.00, 4.99, "Bakery", "Pastry", 30, "🥐", "Flaky, buttery French-style croissants, freshly baked.", "2 pcs", 0, 1, 19, 4.6, 156),
    ("Multigrain Bagels", 5.99, 6.99, "Bakery", "Bread", 25, "🥯", "Hearty multigrain bagels with sesame seeds.", "4 pcs", 0, 0, 14, 4.4, 89),
    ("Chocolate Muffin", 2.49, 2.99, "Bakery", "Muffins", 60, "🧁", "Double chocolate chip muffin, moist and indulgent.", "1 pc", 1, 1, 16, 4.8, 342),

    # ---- MEAT & SEAFOOD ----
    ("Chicken Breast", 7.99, 9.99, "Meat & Seafood", "Poultry", 40, "🍗", "Tender, boneless chicken breast. High protein, low fat.", "500 g", 1, 1, 20, 4.5, 387),
    ("Mutton Biryani Cut", 14.99, 17.99, "Meat & Seafood", "Mutton", 20, "🥩", "Fresh mutton pieces, cleaned and cut for biryani.", "500 g", 0, 0, 16, 4.6, 201),
    ("Atlantic Salmon Fillet", 12.99, 14.99, "Meat & Seafood", "Fish", 15, "🐟", "Fresh Atlantic salmon fillet. Rich in Omega-3.", "200 g", 1, 0, 13, 4.7, 167),
    ("Tiger Prawns", 10.99, 12.99, "Meat & Seafood", "Seafood", 20, "🦐", "Jumbo tiger prawns, cleaned and deveined.", "250 g", 0, 1, 15, 4.6, 213),

    # ---- SNACKS & DRINKS ----
    ("Lay's Classic Chips", 1.99, 2.49, "Snacks & Drinks", "Chips", 100, "🥔", "Crunchy Lay's salted potato chips. Family pack.", "82 g", 0, 1, 20, 4.3, 678),
    ("Dark Chocolate (70%)", 3.49, 3.99, "Snacks & Drinks", "Chocolate", 80, "🍫", "Rich 70% cocoa dark chocolate. Smooth and intense.", "100 g", 1, 0, 12, 4.8, 445),
    ("Roasted Mixed Nuts", 8.99, 10.99, "Snacks & Drinks", "Nuts", 60, "🥜", "Premium roasted cashews, almonds, walnuts and pistachios.", "200 g", 0, 0, 18, 4.7, 312),
    ("Tropicana OJ (1L)", 3.99, 4.49, "Snacks & Drinks", "Juice", 70, "🧃", "100% freshly squeezed orange juice, no added sugar.", "1 L", 1, 1, 11, 4.5, 234),
    ("Cold Brew Coffee", 4.49, 5.49, "Snacks & Drinks", "Coffee", 40, "☕", "Smooth, rich cold brew concentrate. Low acidity.", "500 ml", 1, 0, 18, 4.6, 189),
    ("Sparkling Water (6-pack)", 5.99, 6.99, "Snacks & Drinks", "Water", 80, "💧", "Natural mineral sparkling water. Zero calories.", "6 x 500ml", 0, 0, 14, 4.4, 98),

    # ---- HOUSEHOLD ----
    ("Ariel Detergent Pod", 9.99, 11.99, "Household", "Laundry", 50, "🧺", "Concentrated detergent pods for deep clean every wash.", "20 pcs", 0, 0, 16, 4.6, 321),
    ("Dettol Handwash", 3.49, 3.99, "Household", "Hygiene", 90, "🧴", "Original Dettol antibacterial liquid handwash.", "250 ml", 0, 1, 12, 4.7, 567),
    ("Colgate Toothpaste", 2.99, 3.49, "Household", "Hygiene", 100, "🦷", "Total 12 protection toothpaste for complete oral care.", "150 g", 0, 0, 14, 4.5, 445),
    ("Paper Towels (6-roll)", 8.99, 10.99, "Household", "Cleaning", 40, "🧻", "Ultra-absorbent 3-ply paper towels.", "6 rolls", 0, 0, 18, 4.4, 212),

    # ---- ELECTRONICS ----
    ("USB-C Charging Cable", 9.99, 14.99, "Electronics", "Cables", 60, "🔌", "6ft nylon braided USB-C cable. 60W fast charge.", "1 pc", 0, 1, 33, 4.5, 876),
    ("Wireless Earbuds", 49.99, 79.99, "Electronics", "Audio", 15, "🎧", "True wireless earbuds with active noise cancellation.", "1 pair", 1, 1, 37, 4.6, 543),
    ("Phone Stand", 7.99, 12.99, "Electronics", "Accessories", 45, "📱", "Adjustable aluminum phone stand for desk use.", "1 pc", 0, 1, 38, 4.4, 234),
]

COUPONS = [
    ("WELCOME10", 10, 0, 1000),
    ("SAVE20", 20, 50, 500),
    ("FLAT50", 15, 100, 200),
    ("QUICKCART", 25, 200, 100),
]

def seed_db():
    init_db()
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        c.executemany('''
            INSERT INTO products (name, price, mrp, category, subcategory, stock, emoji, description, unit,
                is_featured, is_deal, discount_pct, rating, review_count)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', PRODUCTS)
        print(f"Seeded {len(PRODUCTS)} products.")

    c.execute("SELECT COUNT(*) FROM coupons")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO coupons (code, discount_pct, min_order, max_uses) VALUES (?,?,?,?)", COUPONS)
        print("Seeded coupons.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_db()
