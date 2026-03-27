import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="todo_app"
    )

def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()

    # -------- DATABASE --------
    cursor.execute("CREATE DATABASE IF NOT EXISTS todo_app")
    cursor.execute("USE todo_app")

    # -------- TASKS --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        created_at DATETIME
    )
    """)

    # -------- CALCULATOR --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calculator_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        expression VARCHAR(255),
        result VARCHAR(255),
        created_at DATETIME
    )
    """)

    # -------- EXPENSE --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        amount FLOAT,
        category VARCHAR(100),
        created_at DATETIME
    )
    """)

    # -------- BALANCE --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS balance (
        id INT PRIMARY KEY,
        amount FLOAT
    )
    """)

    # Insert default balance
    cursor.execute("SELECT * FROM balance WHERE id=1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO balance (id, amount) VALUES (1, 0)")

    # -------- FIX TASK TABLE --------
    cursor.execute("SHOW COLUMNS FROM tasks")
    cols = [c[0] for c in cursor.fetchall()]

    if "title" not in cols:
        cursor.execute("ALTER TABLE tasks ADD COLUMN title VARCHAR(255)")

    if "content" not in cols:
        cursor.execute("ALTER TABLE tasks ADD COLUMN content TEXT")

    if "file_name" not in cols:
        cursor.execute("ALTER TABLE tasks ADD COLUMN file_name VARCHAR(255)")

    conn.commit()
    conn.close()