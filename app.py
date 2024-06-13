import streamlit as st
import streamlit.components.v1 as components
import json
import base64
from PIL import Image
from io import BytesIO
from docx import Document
import os

st.title('File Picker')
st.write('Please select files:')

# Define the path to the HTML file
html_file_path = os.path.join(os.path.dirname(__file__), 'public', 'file_picker.html')

# Load the custom file picker component
with open(html_file_path, 'r') as f:
    file_picker_component = components.html(f.read(), height=300)

# Placeholder for displaying file content
file_content_placeholder = st.empty()

# JavaScript code to receive messages from the file picker
components.html("""
    <script>
    window.addEventListener('message', (event) => {
        const fileInfo = event.data;
        const streamlitDiv = window.parent.document.querySelector('div[data-testid="stAppViewContainer"]');
        const input = document.createElement('textarea');
        input.style.display = 'none';
        input.id = 'file_info';
        input.value = JSON.stringify(fileInfo);
        streamlitDiv.appendChild(input);
        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.style.display = 'none';
        streamlitDiv.appendChild(submitButton);
        submitButton.click();
    });
    </script>
""")

# Hidden input to receive file info from JavaScript
file_info_json = st.text_area('', '', key='file_info', height=0)

# Display file content if available
if file_info_json:
    file_info = json.loads(file_info_json)
    file_name = file_info['file_name']
    file_type = file_info['file_type']
    file_content = file_info['file_content']
    
    st.write(f"### {file_name}")
    
    if file_type == 'text/plain':
        st.text(file_content)
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        file_content_bytes = base64.b64decode(file_content.split(',')[1])
        with open('temp.docx', 'wb') as f:
            f.write(file_content_bytes)
        doc = Document('temp.docx')
        doc_text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        st.text(doc_text)
    elif file_type.startswith('image/'):
        file_content_bytes = base64.b64decode(file_content.split(',')[1])
        image = Image.open(BytesIO(file_content_bytes))
        st.image(image, caption=file_name)
    else:
        st.write("Unsupported file type")
