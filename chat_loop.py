import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chat in a loop
while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "end", "bye"]:
        print("Bot: Goodbye!")
        break

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful chatbot that answers user's question in Korean."},
                  {"role": "user",   "content": user_input}],
    )

    print("Bot:", stream.choices[0].message.content)
