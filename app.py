import streamlit as st
from db import init_db
from todo import show_todo
from calculator import show_calculator
from expense import show_expense
from analyzer import show_analyzer
from password import show_password


# ---------- INIT ----------
st.set_page_config(
    page_title="Multi App Dashboard",
    page_icon="🚀",
    layout="wide"
)

init_db()

# ---------- SIDEBAR ----------
st.sidebar.markdown("## 📌 My Applications")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "📝 Notes",
        "🧮 Calculator",
        "💰 Expense Tracker",
        "📊 Data Analyzer",
        "🔐 Password Generator",
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Built with ❤️ using Streamlit + MySQL")

# ---------- HOME ----------
if page == "🏠 Home":
    st.title("🚀 Multi App Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📝 Notes App")
        st.write("Notes + files + image preview")

    with col2:
        st.markdown("### 🧮 Calculator")
        st.write("Smart calculator with DB history")

    with col3:
        st.markdown("### 💰 Expense Tracker")
        st.write("Finance analytics & charts")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("### 📊 Data Analyzer")
        st.write("Upload CSV & analyze")

    with col5:
        st.markdown("### 🔐 Password Generator")
        st.write("Generate secure passwords")


    st.success("👉 Select any app from sidebar")

# ---------- ROUTING ----------
elif page == "📝 Notes":
    show_todo()

elif page == "🧮 Calculator":
    show_calculator()

elif page == "💰 Expense Tracker":
    show_expense()

elif page == "📊 Data Analyzer":
    show_analyzer()

elif page == "🔐 Password Generator":
    show_password()
