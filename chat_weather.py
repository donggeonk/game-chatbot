import requests
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from weather import get_weather

# create LLM client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the tool for the LLM to call - tell AI abotut the function
functions = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get the current temperature in celsius, weather description (sunny, cloudy, etc), humidity in percent, and wind speed in kph for the provided city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "Name of the city"},
        },
        "required": ["city"],},
    }
]

user_input = input("User: ")
# instructions tell the AI that it can call a function to get the weather
input_messages = [{"role": "user", "content": user_input},
                  {"role": "system", "content": "You can call a function to get the infromation on current temperature in celsius, weather description (sunny, cloudy, etc), humidity in percent, and wind speed in kph. If no function needed, do not call any function and respond concisely."}]


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=input_messages,
    # give the AI access to the tool and information
    functions=functions, # context of all the functions it can call
    function_call="auto", # let the AI decide if it wants to call the function
)

# first step - decide whether to use function or not
message = response.choices[0].message
print("First LLM response:", message)

# If it decided to call get_weather:
if message.function_call:
    # function_call=FunctionCall(arguments='{"city":"Seoul"}', name='get_weather')
    func_name = message.function_call.name # get_weather
    args = json.loads(message.function_call.arguments) # {"city" : "Seoul"}

    if func_name == "get_weather":
        weather_info = get_weather(**args) # key * value **
        function_response = { "weather": weather_info }
    else:
        function_response = { "unknown function" : func_name }

    # system message to tell the LLM that it can use the function call result to generate a followup response
    followup_messages = [
        {"role": "system", "content": "You are a friendly assistant that answers in human-like sentences without symbols or bullet points. Reply to user with the current weather in the city using the data from function call. You have access to current temperature in celsius, weather description (sunny, cloudy, etc), humidity in percent, and wind speed in kph. Only take the data requested by the user."},
        {"role": "user",   "content": user_input},
        message,  # the function_call event
        {
            "role": "function",
            "name": func_name,
            "content": json.dumps(function_response)
        }
    ]

    # send the function call result back to the LLM so it can generate a followup response
    followup = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=followup_messages,
    )
    print("Second LLM response:", followup.choices[0].message)
    print("Bot:", followup.choices[0].message.content)
else:
    # otherwise it answered directly or didn't call a function
    print("Bot:", message.content)