import yaml
import bcrypt
import streamlit as st
import time


def main():
    st.subheader('New User')
    placeholder = st.empty()
    st.session_state['question'] = ''

    with placeholder.form(key='my_form', clear_on_submit=True):
        # Prompt user for username and password
        username = st.text_input("Enter username:", key="username_input")
        email = st.text_input("Enter email:", key="email_input")
        access_level = st.text_input(
            "Enter access level:", key="access_level_input")
        password = st.text_input(
            "Enter password:", type="password", key="password_input")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            # Load existing YAML data from file
            if len(username) == 0 or len(email) == 0 or len(access_level) == 0 or len(password) == 0 or "@" not in email:
                st.error("You must enter all fileds, email must contain @")
            else:
                with open("config.yaml", "r") as file:
                    data = yaml.safe_load(file)
                # if username exist ask for a new username
                if username in data["credentials"]["usernames"]:
                    st.error(
                        "Username already exists. Please enter a different username.")
                else:
                    # Generate hashed password
                    salt = bcrypt.gensalt()  # Generate a salt for bcrypt
                    hashed_password = bcrypt.hashpw(
                        password.encode(), salt).decode()

                    # Add new user to the 'credentials' section
                    data["credentials"]["usernames"][username] = {
                        "email": email,
                        "name": username.capitalize(),
                        "password": hashed_password,
                        "access_level": access_level
                    }

                    # Write updated YAML data to file
                    with open("config.yaml", "w") as file:
                        yaml.dump(data, file, default_flow_style=False)
                    alert = st.success("New user added successfully.")
                    time.sleep(2)
                    alert.empty()


if __name__ == "__main__":
    main()