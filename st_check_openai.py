
import openai
import os
import streamlit as st
from myfunc.mojafunkcija import positive_login, check_openai_errors

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    if st.button("Generate completion"):
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ]
            )

        st.write(completion.choices[0].message)


def main_warp_for_st():
    check_openai_errors(main)

deployment_environment = os.environ.get("DEPLOYMENT_ENVIRONMENT")
 
if deployment_environment == "Streamlit":
    name, authentication_status, username = positive_login(main, " ")
else: 
    if __name__ == "__main__":
        check_openai_errors(main)
