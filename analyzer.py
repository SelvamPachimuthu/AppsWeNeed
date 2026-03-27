import streamlit as st
import pandas as pd

def show_analyzer():
    st.title("📊 Data Analyzer")

    file = st.file_uploader("Upload CSV File", type=["csv"])

    if file:
        df = pd.read_csv(file)

        st.subheader("📋 Data Preview")
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Basic Info")
        st.write(df.describe())

        # Select column
        col = st.selectbox("Select Column", df.columns)

        st.subheader("📈 Chart")
        st.bar_chart(df[col].value_counts())