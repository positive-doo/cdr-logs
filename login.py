import streamlit as st
import streamlit_authenticator as stauth
from openai import APIConnectionError, APIError, RateLimitError
import yaml

def positive_login(main):
    """
    Manages user authentication for a Streamlit application using a YAML configuration.
    """

    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.loader.SafeLoader)

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


def check_openai_errors(main_function):
    try:
        main_function()
    except RateLimitError as e:
        if 'insufficient_quota' in str(e):
            st.write("Potrošili ste sve tokene, kontaktirajte Positive za dalja uputstva")
            # Additional handling, like notifying the user or logging the error
        else:
            st.write(f"Greška {str(e)}")
    except APIConnectionError as e:
        # Handle connection error here
        st.write(f"Ne mogu da se povežem sa OpenAI API-jem: {e} pokušajte malo kasnije.")
    except APIError as e:
        # Handle API error here, e.g. retry or log
        st.write(f"Greška u API-ju: {e} pokušajte malo kasnije.")
    except Exception as e:
        # Handle other exceptions
        st.write(f"Neočekivana Greška : {str(e)} pokušajte malo kasnije.")