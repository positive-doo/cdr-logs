import os
import streamlit as st
from pages import page1, page2
from login import positive_login

st.set_page_config(layout="wide")


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Fetch clients & their workstations", "Page 2"], index=None)

    if page == "Fetch clients & their workstations":
        page1()
    elif page == "Check power outages":
        page2()

deployment_environment = os.environ.get("DEPLOYMENT_ENVIRONMENT")

if deployment_environment == "Streamlit":
    name, authentication_status, username = positive_login(main)
else:
    if __name__ == "__main__":
        main()