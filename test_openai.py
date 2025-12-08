import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    resp = client.chat.completions.create(
        model="gpt-5.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in English and Arabic."},
        ],
    )
    print(resp.choices[0].message.content)

if __name__ == "__main__":
    main()
