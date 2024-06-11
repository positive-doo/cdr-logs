import streamlit as st
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

def positive_login(main):
    """
    Manages user authentication for a Streamlit application using a YAML configuration.
    """

    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )
    
    fields = {
        'Form name': 'Login',
        'Username': 'Username',
        'Password': 'Password',
        'Login': 'Login'
    }
    
    name, authentication_status, username = authenticator.login(fields=fields)
    
    if authentication_status:
        email = config["credentials"]["usernames"][username]["email"]
        access_level = config["credentials"]["usernames"][username]["access_level"]
        st.session_state["name"] = name
        st.session_state["email"] = email
        st.session_state["access_level"] = access_level

        with st.sidebar:
            authenticator.logout("Logout", key="unique_key")
        main()
    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')

    return name, authentication_status, username
