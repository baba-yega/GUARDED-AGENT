
import sqlite3
from langchain_core.tools import tool

@tool
def db_lookup(product_name: str) -> str:
    """
    Look up a product's price and stock by name from the product database.
    Use this when the user asks about pricing, availability, or stock for a specific product.
    Example input: "Wireless Mouse"
    """
    try:
        conn = sqlite3.connect("agent_data.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, price, stock FROM products WHERE name LIKE ?",
            (f"%{product_name}%",)
        )
        results = cursor.fetchall()
        conn.close()

        if not results:
            return f"No product found matching '{product_name}'."

        formatted = [
            f"{name}: ${price:.2f}, {stock} in stock"
            for name, price, stock in results
        ]
        return "\n".join(formatted)

    except sqlite3.Error as e:
        return f"Error: database query failed — {e}"