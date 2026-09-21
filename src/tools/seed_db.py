
import sqlite3

def seed_database():
    conn = sqlite3.connect("agent_data.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    sample_data = [
        (1, "Wireless Mouse", 15.99, 120),
        (2, "Mechanical Keyboard", 79.99, 45),
        (3, "USB-C Hub", 24.50, 200),
        (4, "Laptop Stand", 32.00, 75),
        (5, "Webcam 1080p", 45.99, 30),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
        sample_data
    )

    conn.commit()
    conn.close()
    print("Database seeded.")

if __name__ == "__main__":
    seed_database()