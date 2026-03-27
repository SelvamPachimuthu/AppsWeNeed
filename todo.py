import streamlit as st
from datetime import datetime
from db import get_connection
import os
import pandas as pd

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def show_todo():
    st.title("📝 Notes App")

    # -------- ADD NOTE --------
    st.subheader("➕ Add Note")

    note_title = st.text_input("Note Title")
    note_content = st.text_area("Note Content")

    uploaded_file = st.file_uploader(
        "Upload Excel / Image",
        type=["xlsx", "csv", "png", "jpg", "jpeg"]
    )

    if st.button("Add Note", key="add_note"):
        if note_title and note_content:

            file_name = None

            if uploaded_file:
                file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

                # SAVE FILE
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                file_name = uploaded_file.name

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO tasks (title, content, file_name, created_at) VALUES (%s,%s,%s,%s)",
                (note_title, note_content, file_name, datetime.now())
            )

            conn.commit()
            conn.close()

            st.success("Note added!")
            st.rerun()

    # -------- FETCH DATA --------
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    conn.close()

    # -------- DISPLAY NOTES --------
    st.subheader("📋 Your Notes")

    for task in tasks:
        task_id, title, content, file_name, created_at = task

        st.markdown("---")

        st.markdown(f"## 🏷 {title}")
        st.write(content)
        st.caption(f"🕒 {created_at}")

        # -------- FILE DISPLAY --------
        if file_name:
            file_path = os.path.join(UPLOAD_FOLDER, file_name)

            if os.path.exists(file_path):

                # IMAGE DISPLAY
                if file_name.lower().endswith(("png", "jpg", "jpeg")):
                    st.image(file_path, caption="📷 Uploaded Image", use_container_width=True)

                # EXCEL DISPLAY
                elif file_name.lower().endswith(("xlsx", "csv")):
                    try:
                        if file_name.endswith("xlsx"):
                            df = pd.read_excel(file_path)
                        else:
                            df = pd.read_csv(file_path)

                        st.dataframe(df, use_container_width=True)

                    except Exception as e:
                        st.error("Error reading file")

            else:
                st.warning("File not found")

        col1, col2 = st.columns(2)

        # DELETE
        if col1.button("🗑 Delete", key=f"del_{task_id}"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
            conn.commit()
            conn.close()
            st.rerun()

        # EDIT
        if col2.button("✏️ Edit", key=f"edit_{task_id}"):
            st.session_state["edit_id"] = task_id
            st.session_state["edit_title"] = title
            st.session_state["edit_content"] = content

    # -------- EDIT SECTION --------
    if "edit_id" in st.session_state:
        st.markdown("---")
        st.subheader("✏️ Edit Note")

        new_title = st.text_input("Title", st.session_state["edit_title"])
        new_content = st.text_area("Content", st.session_state["edit_content"])

        if st.button("Update", key="update_note"):
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE tasks SET title=%s, content=%s WHERE id=%s",
                (new_title, new_content, st.session_state["edit_id"])
            )

            conn.commit()
            conn.close()

            del st.session_state["edit_id"]
            st.rerun()