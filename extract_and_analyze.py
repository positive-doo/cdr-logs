import streamlit as st
from pages import page1, page2

st.set_page_config(layout="wide")

def main():
    st.sidebar.title("Navigation; test staging")
    page = st.sidebar.selectbox("Go to", ["Fetch clients & their workstations", "Page2"], index=None)

    if page == "Fetch clients & their workstations":
        page1()
    elif page == "Page2":
        page2()

if __name__ == "__main__":
    main()
