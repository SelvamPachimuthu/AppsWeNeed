import streamlit as st
from db import get_connection
from datetime import datetime

def show_calculator():
    st.title("🧮 Smart Calculator")

    # ---------- SESSION ----------
    if "expression" not in st.session_state:
        st.session_state.expression = ""

    # ---------- DISPLAY ----------
    st.markdown(f"""
    <div style="
        background:#000;
        color:#00FFAA;
        padding:20px;
        border-radius:15px;
        font-size:35px;
        text-align:right;
        margin-bottom:20px;
    ">
        {st.session_state.expression if st.session_state.expression else "0"}
    </div>
    """, unsafe_allow_html=True)

    # ---------- FUNCTIONS ----------
    def press(val):
        st.session_state.expression += str(val)

    def clear():
        st.session_state.expression = ""

    def backspace():
        st.session_state.expression = st.session_state.expression[:-1]

    def calculate():
        try:
            expr = st.session_state.expression
            result = str(eval(expr))

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO calculator_history (expression, result, created_at) VALUES (%s,%s,%s)",
                (expr, result, datetime.now())
            )
            conn.commit()
            conn.close()

            st.session_state.expression = result
        except:
            st.session_state.expression = "Error"

    # ---------- BUTTON STYLE ----------
    st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        border-radius: 12px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- BUTTON GRID ----------
    buttons = [
        ["7","8","9","/"],
        ["4","5","6","*"],
        ["1","2","3","-"],
        ["0",".","=","+"],
    ]

    for r, row in enumerate(buttons):
        cols = st.columns(4)
        for c, val in enumerate(row):
            if val == "=":
                cols[c].button(val, on_click=calculate, key=f"eq_{r}_{c}", use_container_width=True)
            else:
                cols[c].button(val, on_click=press, args=(val,), key=f"{val}_{r}_{c}", use_container_width=True)

    # ---------- CONTROL BUTTONS ----------
    col1, col2 = st.columns(2)
    col1.button("Clear", on_click=clear, use_container_width=True)
    col2.button("⌫ Backspace", on_click=backspace, use_container_width=True)

    # ---------- HISTORY ----------
    st.subheader("📜 History")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT expression, result, created_at FROM calculator_history ORDER BY created_at DESC LIMIT 10")
    history = cursor.fetchall()
    conn.close()

    for expr, res, time in history:
        st.markdown(f"**{expr} = {res}**  \n🕒 {time}")

    if st.button("🧹 Clear History"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM calculator_history")
        conn.commit()
        conn.close()
        st.rerun()