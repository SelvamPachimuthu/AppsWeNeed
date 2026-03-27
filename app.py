import streamlit as st
import mysql.connector
from datetime import datetime

# ------------------ DB CONNECTION ------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="todo_app"
    )

# ------------------ CREATE DATABASE & TABLE ------------------
def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()

    # Create DB
    cursor.execute("CREATE DATABASE IF NOT EXISTS todo_app")

    # Use DB
    cursor.execute("USE todo_app")

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            created_at DATETIME
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# ------------------ CRUD FUNCTIONS ------------------
def add_task(title):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO tasks (title, created_at) VALUES (%s, %s)"
    values = (title, datetime.now())

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit()

    cursor.close()
    conn.close()


def update_task(task_id, new_title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET title=%s WHERE id=%s",
        (new_title, task_id)
    )
    conn.commit()

    cursor.close()
    conn.close()

# ------------------ INIT ------------------
init_db()

st.title("📝 To-Do App (MySQL + Streamlit)")

# ------------------ ADD TASK ------------------
st.subheader("➕ Add Task")
new_task = st.text_input("Enter task")

if st.button("Add"):
    if new_task:
        add_task(new_task)
        st.success("Task added!")
    else:
        st.warning("Enter something!")

# ------------------ VIEW TASKS ------------------
st.subheader("📋 Your Tasks")

tasks = get_tasks()

for task in tasks:
    task_id, title, created_at = task

    col1, col2, col3 = st.columns([4, 2, 2])

    with col1:
        st.write(f"**{title}**")
        st.caption(f"🕒 {created_at}")

    with col2:
        if st.button("Delete", key=f"del_{task_id}"):
            delete_task(task_id)
            st.rerun()

    with col3:
        new_title = st.text_input("Edit", key=f"edit_{task_id}")
        if st.button("Update", key=f"upd_{task_id}"):
            if new_title:
                update_task(task_id, new_title)
                st.rerun()