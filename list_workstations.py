import os
import requests
import csv

API_BASE_URL = os.getenv("TRMM_BASE_URL")
HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": os.getenv("TRMM_NP"),
    }

def fetch_workstations(client_id):
    """Fetch the list of workstations for the specified client ID and return the response."""
    response = requests.get(f'{API_BASE_URL}/agents/?client={client_id}', headers=HEADERS)
    if response.status_code == 200:
        workstations = response.json()
        return workstations
    else:
        print(f'Failed to fetch workstations: {response.status_code}')
        return []

client_id = 11  # Use the client ID obtained previously
workstations = fetch_workstations(client_id)

# CSV file path
csv_file_path = 'sajam_workstations.csv'

def main():
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Computer Name', 'Motherboard', 'CPU', 'RAM', 'HDD/SSD', 'CD/DVD', 'Installed Software'])

        for workstation in workstations:
            if workstation.get('monitoring_type') == 'workstation':
                computer_name = workstation.get('hostname', 'N/A')
                motherboard = workstation.get('make_model', 'N/A')
                cpu = ", ".join(workstation.get('cpu_model', ['N/A']))
                ram = workstation.get('ram', 'N/A')  # Adjust based on actual key if available
                hdd_ssd = ", ".join(workstation.get('physical_disks', ['N/A']))
                cd_dvd = workstation.get('cd_dvd', 'N/A')  # Adjust based on actual key if available
                installed_software = ", ".join(workstation.get('installed_software', ['N/A']))

                writer.writerow([computer_name, motherboard, cpu, ram, hdd_ssd, cd_dvd, installed_software])

if __name__ == '__main__':
    main()
