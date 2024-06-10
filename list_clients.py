import os
import requests
import streamlit as st



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
        for client in clients:
            print(f'Client ID: {client["id"]}, Client Name: {client["name"]}')
    else:
        print(f'Failed to fetch clients: {response.status_code}')

list_clients()