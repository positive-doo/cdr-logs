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
# Optionally, set these in your environment or use the defaults below.
SHAREPOINT_HOST = os.getenv("SHAREPOINT_HOST", "positivens.sharepoint.com")
SITE_PATH = os.getenv("SITE_PATH", "sites/PUBLIC")

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
    `/Deljeni dokumenti/AI DEV/yourfile.ext`
    """
)

# Text input for the file path (relative to the document library root)
file_path_input = st.text_input(
    "SharePoint File Path",
    value="/Deljeni dokumenti/AI DEV/yourfile.ext"
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
        # The scope '.default' uses all the app permissions granted in the portal.
        scope = ["https://graph.microsoft.com/.default"]

        result = app.acquire_token_for_client(scopes=scope)
        if "access_token" not in result:
            st.error(f"Error obtaining access token: {result.get('error_description')}")
        else:
            access_token = result["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}

            # ---------------------------
            # Step 2: Get the Site ID from SharePoint
            # ---------------------------
            site_endpoint = f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_HOST}:/{SITE_PATH}"
            site_response = requests.get(site_endpoint, headers=headers)
            if site_response.status_code != 200:
                st.error(f"Error fetching site details: {site_response.status_code} {site_response.text}")
            else:
                site_data = site_response.json()
                site_id = site_data.get("id")
                st.write(f"**Retrieved Site ID:** {site_id}")

                # ---------------------------
                # Step 3: Download the File
                # ---------------------------
                # URL-encode the file path (keeping the leading slash intact)
                encoded_file_path = "/" + quote(file_path_input.lstrip("/"))
                file_endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:{encoded_file_path}:/content"
                
                file_response = requests.get(file_endpoint, headers=headers)
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
