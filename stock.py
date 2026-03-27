import streamlit as st
import pandas as pd
import yfinance as yf

def show_stock():
    st.title("📈 Stock Dashboard")

    stock = st.text_input("Enter Stock (e.g., TCS.NS, INFY.NS)")

    if stock:
        data = yf.download(stock, period="6mo")

        st.line_chart(data["Close"])

        st.subheader("📋 Data")
        st.dataframe(data.tail())