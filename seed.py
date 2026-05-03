import sqlite3
from database import get_connection, init_db

# Real-world product catalog (30+ items)
PRODUCTS = [
    # Groceries & Produce
    ("Fresh Organic Apples (1kg)", 4.99, "Produce", 150, "🍎", "Locally sourced organic apples."),
    ("Bananas (Bunch)", 2.49, "Produce", 200, "🍌", "Sweet and ripe yellow bananas."),
    ("Avocado (Each)", 1.99, "Produce", 80, "🥑", "Hass avocados, perfect for guacamole."),
    ("Carrots (1kg)", 1.49, "Produce", 120, "🥕", "Crunchy and fresh carrots."),
    ("Broccoli (Head)", 2.29, "Produce", 60, "🥦", "Fresh broccoli crowns."),
    # Dairy & Eggs
    ("Whole Milk (1 Gallon)", 3.99, "Dairy", 50, "🥛", "Farm fresh whole milk."),
    ("Large Eggs (1 Dozen)", 4.29, "Dairy", 100, "🥚", "Free-range brown eggs."),
    ("Cheddar Cheese (Block)", 5.49, "Dairy", 40, "🧀", "Aged sharp cheddar cheese."),
    ("Greek Yogurt (Plain)", 1.29, "Dairy", 90, "🥣", "High protein plain greek yogurt."),
    # Bakery
    ("Whole Wheat Bread", 3.49, "Bakery", 45, "🍞", "Freshly baked whole wheat loaf."),
    ("Croissant (2-Pack)", 4.00, "Bakery", 30, "🥐", "Buttery and flaky french croissants."),
    ("Bagels (6-Pack)", 5.99, "Bakery", 25, "🥯", "Everything bagels."),
    # Meat & Seafood
    ("Chicken Breast (1lb)", 6.99, "Meat", 40, "🍗", "Boneless, skinless chicken breasts."),
    ("Beef Steak (Ribeye)", 14.99, "Meat", 20, "🥩", "Prime cut ribeye steak."),
    ("Fresh Salmon (8oz)", 9.99, "Meat", 15, "🐟", "Wild caught Atlantic salmon."),
    # Pantry & Snacks
    ("Potato Chips (Family Size)", 3.99, "Snacks", 100, "🥔", "Classic salted potato chips."),
    ("Dark Chocolate Bar", 2.99, "Snacks", 150, "🍫", "70% cocoa dark chocolate."),
    ("Mixed Nuts (Jar)", 8.99, "Snacks", 60, "🥜", "Roasted and salted premium mixed nuts."),
    ("Pasta (Spaghetti)", 1.99, "Pantry", 200, "🍝", "Italian style spaghetti pasta."),
    ("Tomato Sauce", 2.49, "Pantry", 180, "🥫", "Classic marinara sauce."),
    ("Olive Oil (500ml)", 7.99, "Pantry", 50, "🫒", "Extra virgin olive oil."),
    # Beverages
    ("Spring Water (24-Pack)", 5.99, "Beverages", 80, "💧", "Natural spring water."),
    ("Orange Juice (1L)", 4.49, "Beverages", 60, "🧃", "100% freshly squeezed orange juice."),
    ("Craft Coffee Beans (12oz)", 12.99, "Beverages", 40, "☕", "Artisan roasted arabica coffee."),
    ("Green Tea (Box)", 3.99, "Beverages", 70, "🍵", "Organic green tea bags."),
    # Electronics & Home
    ("Wireless Earbuds", 89.99, "Electronics", 15, "🎧", "Noise-canceling bluetooth earbuds."),
    ("Smart Watch", 199.99, "Electronics", 10, "⌚", "Fitness tracking smartwatch."),
    ("AA Batteries (10-Pack)", 8.99, "Home", 200, "🔋", "Long-lasting alkaline batteries."),
    ("Paper Towels (6 Rolls)", 12.99, "Home", 50, "🧻", "Ultra-absorbent paper towels."),
    ("Dish Soap", 3.49, "Home", 90, "🧼", "Tough on grease dishwashing liquid.")
]

def seed_db():
    init_db()
    conn = get_connection()
    c = conn.cursor()
    
    # Check if products already exist
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        c.executemany('''
            INSERT INTO products (name, price, category, stock, emoji, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', PRODUCTS)
        print(f"Seeded {len(PRODUCTS)} products into the database.")
    else:
        print("Database already contains products. Skipping seed.")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_db()
