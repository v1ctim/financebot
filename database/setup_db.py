import sqlite3

conn = sqlite3.connect('finance_bot.db')
c = conn.cursor()

# Create User table
c.execute('''CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    currency TEXT NOT NULL,
    budget REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

# Create UserTransaction table
c.execute('''CREATE TABLE IF NOT EXISTS UserTransaction (
    transaction_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL NOT NULL,
    description TEXT,
    category TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
)''')

# Create Budget table
c.execute('''CREATE TABLE IF NOT EXISTS Budget (
    budget_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    category TEXT NOT NULL,
    budget_amount REAL NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
)''')

# Create Report table
c.execute('''CREATE TABLE IF NOT EXISTS Report (
    report_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    total_income REAL,
    total_expense REAL,
    balance REAL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
)''')

# Create RecurringTransaction table
c.execute('''CREATE TABLE IF NOT EXISTS RecurringTransaction (
    recurring_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    interval TEXT NOT NULL,
    next_due_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
)''')

conn.commit()
conn.close()
