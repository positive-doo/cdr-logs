
import openai
import os
import streamlit as st
from login import positive_login, check_openai_errors

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    if st.button("Generate completion"):
        completion = client.chat.completions.create(
            model="gpt-4",
              messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played? Explain in detail (long answer). Be sure to use as much tokens as you can."}
            ]
            )

        st.write(completion.choices[0].message.content)


def main_wrap_for_st():
    check_openai_errors(main)

deployment_environment = os.environ.get("DEPLOYMENT_ENVIRONMENT")
 
if deployment_environment == "Streamlit":
    name, authentication_status, username = positive_login(main_wrap_for_st)
else: 
    if __name__ == "__main__":
        check_openai_errors(main)
