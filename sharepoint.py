import os
import streamlit as st
import msal
import requests
from urllib.parse import quote

# -----------------------------------------------------------------------------
# Load sensitive data from environment variables
# -----------------------------------------------------------------------------
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
SHAREPOINT_HOST = os.getenv("SHAREPOINT_HOST", "positivens.sharepoint.com")
SITE_PATH = os.getenv("SITE_PATH", "sites/PUBLIC")

# Debugging: Print environment variables (mask secrets)
print(f"CLIENT_ID: {CLIENT_ID[:5]}...")  # Only show first 5 characters for security
print(f"CLIENT_SECRET: {'*' * len(CLIENT_SECRET) if CLIENT_SECRET else 'NOT SET'}")
print(f"TENANT_ID: {TENANT_ID}")
print(f"SHAREPOINT_HOST: {SHAREPOINT_HOST}")
print(f"SITE_PATH: {SITE_PATH}")

if not CLIENT_ID or not CLIENT_SECRET or not TENANT_ID:
    st.error("Please set CLIENT_ID, CLIENT_SECRET, and TENANT_ID environment variables.")
    st.stop()

# -----------------------------------------------------------------------------
# Streamlit UI
# -----------------------------------------------------------------------------
st.title("SharePoint File Downloader")

st.write(
    """
    Enter the **file path** (including the file name and extension) for the file you want to download from SharePoint.
    
    For example:  
    '/AI DEV/yourfile.ext`
    """
)

# Text input for the file path (relative to the document library root)
file_path_input = st.text_input(
    "SharePoint File Path",
    value="/AI DEV/new_denty/yourfile.ext"
)

# -----------------------------------------------------------------------------
# Button to start the download
# -----------------------------------------------------------------------------
if st.button("Download File"):
    if not file_path_input:
        st.error("Please enter a valid file path.")
    else:
        st.info("Starting file download from SharePoint...")
        
        # ---------------------------
        # Step 1: Acquire an Access Token
        # ---------------------------
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=authority,
            client_credential=CLIENT_SECRET
        )
        scope = ["https://graph.microsoft.com/.default"]

        result = app.acquire_token_for_client(scopes=scope)

        print("Access Token Response:", result)  # Debug access token response

        if "access_token" not in result:
            st.error(f"Error obtaining access token: {result.get('error_description')}")
        else:
            access_token = result["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}

            # ---------------------------
            # Step 2: Get the Site ID from SharePoint
            # ---------------------------
            site_endpoint = f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_HOST}:/{SITE_PATH}"
            print(f"Fetching Site ID from: {site_endpoint}")  # Debug URL

            site_response = requests.get(site_endpoint, headers=headers)
            print("Site Response Status:", site_response.status_code)
            print("Site Response Body:", site_response.text)  # Debug site response

            if site_response.status_code != 200:
                st.error(f"Error fetching site details: {site_response.status_code} {site_response.text}")
            else:
                site_data = site_response.json()
                site_id = site_data.get("id")
                st.write(f"**Retrieved Site ID:** {site_id}")
                print("Site ID:", site_id)  # Debug Site ID

                # ---------------------------
                # Step 3: Get the Drive ID
                # ---------------------------
                drive_endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
                print(f"Fetching available drives from: {drive_endpoint}")

                drive_response = requests.get(drive_endpoint, headers=headers)
                print("Drives Response Status:", drive_response.status_code)
                print("Drives Response Body:", drive_response.text)

                if drive_response.status_code != 200:
                    st.error(f"Error fetching drive details: {drive_response.status_code} {drive_response.text}")
                else:
                    drive_data = drive_response.json()
                    drive_id = drive_data["value"][0]["id"]  # assuming the first drive is the one you need

                    print("Drive ID:", drive_id)  # Debug Drive ID

                    # ---------------------------
                    # Step 4: Verify File Path and List Folder Contents
                    # ---------------------------
                    folder_path = os.path.dirname(file_path_input)  # Extract the folder path
                    encoded_folder_path = "/" + quote(folder_path.lstrip("/"))
                    folder_endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:{encoded_folder_path}:/children"
                    print(f"Fetching folder contents from: {folder_endpoint}")  # Debug folder request

                    folder_response = requests.get(folder_endpoint, headers=headers)
                    print("Folder Response Status:", folder_response.status_code)
                    print("Folder Response Body:", folder_response.text)

                    if folder_response.status_code == 200:
                        files = folder_response.json().get("value", [])
                        print("Files in Folder:", [f["name"] for f in files])  # Debug file names in folder

                    # ---------------------------
                    # Step 5: Download the File
                    # ---------------------------
                    encoded_file_path = "/" + quote(file_path_input.lstrip("/"))
                    file_endpoint = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:{encoded_file_path}:/content"
                    print(f"Attempting to download file from: {file_endpoint}")  # Debug file request

                    file_response = requests.get(file_endpoint, headers=headers)
                    print("File Response Status:", file_response.status_code)
                    print("File Response Body:", file_response.text)

                    if file_response.status_code == 200:
                        file_bytes = file_response.content
                        st.success("File downloaded successfully from SharePoint!")

                        # Provide a download button for the user
                        st.download_button(
                            label="Click here to download the file",
                            data=file_bytes,
                            file_name=os.path.basename(file_path_input),
                            mime="application/octet-stream"
                        )
                    else:
                        st.error(f"Error downloading file: {file_response.status_code} {file_response.text}")
