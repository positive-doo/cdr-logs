# main.py
import os
import streamlit as st
from pages import page1, page2

st.set_page_config(layout="wide")

if 'login' not in st.session_state:
    st.session_state.login = False

def check_login(username, password):
    return username == os.getenv("TRMM_USER") and password == os.getenv("TRMM_PASS")

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    if not st.session_state.login:
        login()
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox("Go to", ["Fetch clients & their workstations", "Page 2"], index=None)

        if page == "Fetch clients & their workstations":
            page1()
        elif page == "Page 2":
            page2()
