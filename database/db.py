# db.py
import sqlite3

def add_user(user_id, first_name, plan_budget, currency):
    conn = sqlite3.connect("finance_bot.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            plan_budget REAL,
            currency TEXT
        )
    """)

    try:
        c.execute("""
            INSERT INTO Users (user_id, first_name, plan_budget, currency)
            VALUES (?, ?, ?, ?)
        """, (user_id, first_name, plan_budget, currency))
        
        conn.commit()
        print(f"User {first_name} added successfully.")
    except sqlite3.IntegrityError:
        print("User already exists.")

    conn.close()
