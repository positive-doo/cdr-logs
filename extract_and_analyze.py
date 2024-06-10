import os
import requests
import streamlit as st
import pandas as pd

# API base URL and headers
API_BASE_URL = os.getenv("TRMM_BASE_URL")
HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": os.getenv("TRMM_NP"),
}

def list_clients():
    """Fetch the list of clients."""
    response = requests.get(f'{API_BASE_URL}/clients/', headers=HEADERS)
    if response.status_code == 200:
        clients = response.json()
        return clients
    else:
        st.error(f'Failed to fetch clients: {response.status_code}')
        return []

def main():
    # Streamlit web page
    st.title("Client Management")

    with st.expander("Instructions"):
        st.write("""
        Here you can manage your clients. Use the button below to fetch the list of clients.
        After fetching the clients, you will see a table with the client data and an option to download it as a CSV file.
        """)

    if st.button("Fetch Clients"):
        clients = list_clients()
        if clients:
            df = pd.DataFrame(clients)
            st.write("### Client Data")
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name='clients.csv',
                mime='text/csv',
            )

if __name__ == "__main__":
    main()
