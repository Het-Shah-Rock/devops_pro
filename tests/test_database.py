import sqlite3
import pytest
import sys
import os

# Add project root to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_connection, init_db

@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    """Create a fresh in-memory database for every test."""
    test_db = str(tmp_path / "test_quickcart.db")
    monkeypatch.setenv("DB_PATH", test_db)
    init_db()
    yield test_db

class TestDatabase:
    """Unit Tests for Database Layer"""

    def test_db_connection(self):
        """Test: Database connection is established."""
        conn = get_connection()
        assert conn is not None
        conn.close()

    def test_products_table_exists(self):
        """Test: Products table is created on init."""
        conn = get_connection()
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
        assert cursor.fetchone() is not None
        conn.close()

    def test_orders_table_exists(self):
        """Test: Orders table is created on init."""
        conn = get_connection()
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
        assert cursor.fetchone() is not None
        conn.close()

    def test_insert_and_retrieve_product(self):
        """Test: Can insert a product and read it back."""
        conn = get_connection()
        conn.execute(
            "INSERT INTO products (name, price, category, stock, emoji, description) VALUES (?,?,?,?,?,?)",
            ("Test Apple", 1.99, "Produce", 50, "🍎", "Test description")
        )
        conn.commit()
        row = conn.execute("SELECT * FROM products WHERE name = 'Test Apple'").fetchone()
        assert row is not None
        assert row["price"] == 1.99
        assert row["stock"] == 50
        conn.close()

    def test_insert_order(self):
        """Test: Can create an order for a user."""
        conn = get_connection()
        conn.execute("INSERT INTO orders (username, total_amount) VALUES (?, ?)", ("testuser", 14.99))
        conn.commit()
        row = conn.execute("SELECT * FROM orders WHERE username = 'testuser'").fetchone()
        assert row is not None
        assert row["total_amount"] == 14.99
        assert row["status"] == "Order Placed"
        conn.close()

    def test_stock_update(self):
        """Test: Stock decreases after a purchase."""
        conn = get_connection()
        c = conn.execute(
            "INSERT INTO products (name, price, category, stock, emoji, description) VALUES (?,?,?,?,?,?)",
            ("UNIQUE_TEST_MILK_XYZ", 2.49, "Dairy", 20, "M", "milk")
        )
        conn.commit()
        pid = c.lastrowid
        conn.execute("UPDATE products SET stock = stock - 3 WHERE id = ?", (pid,))
        conn.commit()
        remaining = conn.execute("SELECT stock FROM products WHERE id = ?", (pid,)).fetchone()["stock"]
        assert remaining == 17
        conn.close()
