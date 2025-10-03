import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # OOP

# Input from user
prompt = input("User: ")

# Response API - lightweight
response = client.responses.create(
    model="gpt-4o-mini",
    instructions="Respond concisely in 10 words.", # AI model
    input=prompt,
)

print("Bot: ", response.output_text)


# Chat Completion - classic
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system",  "content": "Respond concisely within 10 words."},
        {"role": "user",    "content": prompt},
    ],
)

print("Bot:", completion.choices[0].message.content)


# Streaming
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system",  "content": "Respond concisely in two to three sentences."},
        {"role": "user",    "content": prompt}
    ],
    stream=True
)

# Print as tokens arrive
print("Bot:", end=" ", flush=True)
for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
print()
