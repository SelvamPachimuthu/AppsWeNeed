import streamlit as st
from db import get_connection
from datetime import datetime
import pandas as pd

def show_expense():
    st.title("💰 Expense Tracker Pro")

    conn = get_connection()
    cursor = conn.cursor()

    # -------- CURRENT BALANCE --------
    cursor.execute("SELECT amount FROM balance WHERE id=1")
    balance = cursor.fetchone()[0]

    st.metric("💵 Current Balance", f"₹ {balance:.2f}")

    st.markdown("---")

    # -------- ADD TRANSACTION --------
    st.subheader("➕ Add Transaction")

    col1, col2, col3 = st.columns(3)

    with col1:
        title = st.text_input("Title")

    with col2:
        amount = st.number_input("Amount", min_value=0.0)

    with col3:
        t_type = st.selectbox("Type", ["Expense", "Income"])

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Salary", "Other"]
    )

    if st.button("Add Transaction"):
        if title and amount > 0:

            # INSERT
            cursor.execute(
                "INSERT INTO expenses (title, amount, category, created_at) VALUES (%s,%s,%s,%s)",
                (title, amount, category, datetime.now())
            )

            # UPDATE BALANCE
            if t_type == "Expense":
                balance -= amount
            else:
                balance += amount

            cursor.execute(
                "UPDATE balance SET amount=%s WHERE id=1",
                (balance,)
            )

            conn.commit()
            st.success("Added!")
            st.rerun()

    st.markdown("---")

    # -------- FETCH DATA --------
    cursor.execute("SELECT * FROM expenses ORDER BY created_at DESC")
    data = cursor.fetchall()

    conn.close()

    if data:
        df = pd.DataFrame(data, columns=["ID","Title","Amount","Category","Time"])

        df["Time"] = pd.to_datetime(df["Time"])
        df["Date"] = df["Time"].dt.date
        df["Month"] = df["Time"].dt.to_period("M")
        df["Week"] = df["Time"].dt.to_period("W")

        # -------- TABLE --------
        st.subheader("📋 Transactions")
        st.dataframe(df, use_container_width=True)

        # -------- WEEKLY --------
        st.subheader("📅 Weekly Summary")
        weekly = df.groupby("Week")["Amount"].sum()
        st.bar_chart(weekly)

        # -------- MONTHLY --------
        st.subheader("📊 Monthly Summary")
        monthly = df.groupby("Month")["Amount"].sum()
        st.bar_chart(monthly)

        # -------- CATEGORY --------
        st.subheader("📊 Category Spending")
        cat = df.groupby("Category")["Amount"].sum()
        st.bar_chart(cat)

        # -------- TOTAL --------
        st.subheader("📈 Overview")
        total = df["Amount"].sum()

        st.write(f"💸 Total Transactions: ₹ {total:.2f}")