import os
import requests
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

API_BASE_URL = os.getenv("TRMM_BASE_URL")
HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": os.getenv("TRMM_NP"),
}

USERNAME = os.getenv("TRMM_USER")
PASSWORD = os.getenv("TRMM_PASS")

if 'login' not in st.session_state:
    st.session_state.login = False

def check_login(username, password):
    return username == USERNAME and password == PASSWORD

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


def fetch_clients():
    """Fetch the list of clients."""
    response = requests.get(f'{API_BASE_URL}/clients/', headers=HEADERS)
    if response.status_code == 200:
        clients = response.json()
        return clients
    else:
        st.error(f'Failed to fetch clients: {response.status_code}')
        return []


def fetch_workstations(client_id):
    """Fetch the list of workstations for the specified client ID and return the response."""
    response = requests.get(f'{API_BASE_URL}/agents/?client={client_id}', headers=HEADERS)
    if response.status_code == 200:
        workstations = response.json()
        return workstations
    else:
        print(f'Failed to fetch workstations: {response.status_code}')
        return []
    

def main():
    if "clients" not in st.session_state:
        st.session_state.clients = None
    if "workstations" not in st.session_state:
        st.session_state.workstations = None

    st.title("App za pristup podacima iz Tactical RMM-a 💻")

    with st.expander("Instrukcije za korišćenje"):
        st.write("""
        ... kada bude bilo potrebe...
        """)

    st.divider()

    col1, _, col2 = st.columns([3, 1, 5])

    with col1:

        if st.button("Fetch Clients"):
            clients = fetch_clients()
            if clients:
                st.session_state.clients = pd.DataFrame(clients)

        if st.session_state.clients is not None:
            df = st.session_state.clients
            display_df = df[['name', 'id', 'agent_count']]
            st.write("### Client Data")
            st.dataframe(display_df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8-sig')

            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name='clients.csv',
                mime='text/csv',
                )
            
    with col2:

        col21, _ = st.columns([1, 6])
        client_id = col21.text_input("Unesi ID klijenta")

        if client_id:
            if client_id.isdigit():
                workstations = fetch_workstations(int(client_id))
                if workstations:
                    st.session_state.workstations = pd.DataFrame(workstations)
                
                if st.session_state.workstations is not None:
                    df = st.session_state.workstations

                    display_df = df[['hostname', 'logged_username']]
                    st.write("### Workstation Data")
                    st.dataframe(display_df, use_container_width=True)
                    csv = df.to_csv(index=False).encode('utf-8-sig')

                    st.download_button(
                        label="Download Workstations as CSV",
                        data=csv,
                        file_name='workstations.csv',
                        mime='text/csv',
                    )
            else:
                st.warning("Samo intedžeri!")

if __name__ == "__main__":
    if not st.session_state.login:
        login()
    else:
        main()
