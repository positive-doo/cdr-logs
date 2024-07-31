import os
import requests
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

API_BASE_URL = os.getenv("TRMM_BASE_URL")
HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": os.getenv("TRMM_NP"),
}

@st.cache_data
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
        workstations_ids = [workstation['agent_id'] for workstation in workstations]
        return workstations, workstations_ids
    else:
        print(f'Failed to fetch workstations: {response.status_code}')
        return []


def fetch_software_data(workstation_id):
    """Fetch the software data for the specified workstation ID and return the response."""
    response = requests.get(f'{API_BASE_URL}/software/{workstation_id}/', headers=HEADERS)
    if response.status_code == 200:
        software_data = response.json()
        return software_data
    else:
        print(f'Failed to fetch software data: {response.status_code}')
        return []


def fetch_ram_data(agent_id):
    """Fetch the RAM data for the specified workstation ID using web scraping."""
    API_BASE_URL = os.getenv("TRMM_BASE_URL")
    url = f"{API_BASE_URL}/agents/{agent_id}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        ram_element = soup.select_one("div.q-item__section.column.q-item__section--main.justify-center")
        ram_text = ram_element.text if ram_element else "N/A"
    except Exception as e:
        print(f"Failed to fetch RAM data: {e}")
        ram_text = "N/A"
    
    return ram_text


def page1():
    if "clients" not in st.session_state:
        st.session_state.clients = None
    if "workstations" not in st.session_state:
        st.session_state.workstations = None
    if "software" not in st.session_state:
        st.session_state.software = None

    st.title("App za pristup podacima iz Tactical RMM-a 💻")

    with st.expander("Instrukcije za korišćenje"):
        st.write("""
        ... kada bude bilo potrebe...
        """)

    st.divider()

    col1, _, col2 = st.columns([3, 1, 5])

    with col1:
        st.session_state.clients = pd.DataFrame(fetch_clients())

        if st.session_state.clients is not None:
            df = st.session_state.clients
            display_df = df[['name', 'id', 'agent_count']]
            st.write("### Client Data")
            st.dataframe(display_df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8-sig')

            st.download_button(
                label="Download Clients as CSV",
                data=csv,
                file_name='clients.csv',
                mime='text/csv',
            )

    with col2:
        col21, _ = st.columns([1, 6])
        client_id = col21.text_input("Unesi ID klijenta")

        if client_id:
            if client_id.isdigit():
                client_id_int = int(client_id)
                if client_id_int in st.session_state.clients['id'].values:
                    workstations, workstations_ids = fetch_workstations(client_id_int)

                    if workstations != []:
                        with st.spinner("Obrada radnih stanica..."):
                            if workstations:
                                st.session_state.workstations = pd.DataFrame(workstations)

                            if st.session_state.workstations is not None:
                                df = st.session_state.workstations

                                software_list = []
                                ram_list = []
                                for w_id in workstations_ids:
                                    software_data = fetch_software_data(w_id)
                                    if 'software' in software_data:
                                        sw_names = [software['name'] for software in software_data['software']]
                                        software_list.append({'workstation_id': w_id, 'software': sw_names})
                                    ram_data = fetch_ram_data(w_id)
                                    ram_list.append({'workstation_id': w_id, 'ram': ram_data})

                                software_df = pd.DataFrame(software_list)
                                ram_df = pd.DataFrame(ram_list)

                                # Merge software and RAM data with workstations data
                                df = df.merge(software_df, left_on='agent_id', right_on='workstation_id', how='left')
                                df = df.merge(ram_df, left_on='agent_id', right_on='workstation_id', how='left')
                                df['software'] = df['software'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')

                                # Filter and rename columns
                                df = df[['hostname', 'client_name', 'operating_system', 'cpu_model', 'graphics', 'physical_disks', 'ram', 'software']]
                                df.rename(columns={
                                    'hostname': 'Hostname',
                                    'client_name': 'Client',
                                    'operating_system': 'OS',
                                    'cpu_model': 'CPU',
                                    'graphics': 'GPU',
                                    'software': 'SW',
                                    'ram': 'RAM'
                                }, inplace=True)

                                # Separate physical_disks into individual columns
                                max_disks = df['physical_disks'].apply(lambda x: len(x) if isinstance(x, list) else 0).max()
                                for i in range(max_disks):
                                    df[f'DISK {i+1}'] = df['physical_disks'].apply(lambda x: x[i] if isinstance(x, list) and len(x) > i else '')

                                df.drop(columns=['physical_disks'], inplace=True)

                                display_df = df[['Hostname', 'Client', 'OS', 'CPU', 'GPU', 'RAM'] + [f'DISK {i+1}' for i in range(max_disks)] + ['SW']]
                                st.write("### Workstation Data")
                                st.dataframe(display_df, use_container_width=True)
                                csv = df.to_csv(index=False).encode('utf-8-sig')

                                st.download_button(
                                    label="Download Workstations as CSV",
                                    data=csv,
                                    file_name='workstations.csv',
                                    mime='text/csv',
                                    key='workstations_csv',
                                )
                    else:
                        st.warning("Nema radnih stanica za ovog klijenta.")
                else:
                    st.warning("Ne postoji klijent sa tim ID-jem.")
            else:
                st.warning("Samo intedžeri!")


def page2():
    def check_term_in_file(url, term):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return term.lower() in soup.text.lower()
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return False

    st.title("Pretraga planiranih isključenja struje")

    term0 = "Данила Киша"
    urls = [
        "https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_0_Iskljucenja.htm",
        "https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_1_Iskljucenja.htm",
        "https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_2_Iskljucenja.htm",
        "https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_3_Iskljucenja.htm"
    ]

    day_mapping = {
        0: "Danas",
        1: "Sutra",
        2: "Prekosutra",
        3: "Nakosutra"
    }
    term = st.text_input("Unesite termin (ostaviti prazno za 'Данила Киша')")
    if term.strip() == "":
        term = term0

    if st.button("Pretraži"):
        results = []
        for i, url in enumerate(urls):
            if check_term_in_file(url, term):
                results.append((day_mapping[i], url))
        
        output = ""
        if results:
            for result in results:
                output += f"Termin '{term}' je pronađen za '{result[0]}', pogledajte:\n{result[1]}\n\n"
        else:
            output += f"Termin'{term}' nije pronađen u narednim danima.\n\n"

        st.write(output)
