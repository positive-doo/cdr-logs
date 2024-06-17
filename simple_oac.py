import openai
import os


client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    messages = [
        {"role": "system", "content": "You are a helpful assistant that always writes in Serbian."}
    ]

    while True:
        user_message = input("\n\nUser: ")

        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.0,
            messages=messages,
        )

        assistant_message = response.choices[0].message.content
        
        print(f"Assistant: {assistant_message}")

        messages.append({"role": "assistant", "content": assistant_message})

if __name__ == "__main__":
    main()
