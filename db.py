import sqlite3

def get_connection():
    return sqlite3.connect("todo_app.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # -------- TASKS --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        file_name TEXT,
        created_at DATETIME
    )
    """)

    # -------- CALCULATOR --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calculator_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expression TEXT,
        result TEXT,
        created_at DATETIME
    )
    """)

    # -------- EXPENSE --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        amount REAL,
        category TEXT,
        created_at DATETIME
    )
    """)

    # -------- BALANCE --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS balance (
        id INTEGER PRIMARY KEY,
        amount REAL
    )
    """)

    # Insert default balance
    cursor.execute("SELECT * FROM balance WHERE id=1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO balance (id, amount) VALUES (1, 0)")

    conn.commit()
    conn.close()