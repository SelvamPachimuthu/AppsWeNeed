import streamlit as st
import random
import string

def show_password():
    st.title("🔐 Password Generator")

    length = st.slider("Length", 6, 20, 10)

    if st.button("Generate"):
        chars = string.ascii_letters + string.digits + "!@asd"
        password = ''.join(random.choice(chars) for _ in range(length))

        st.success(password)