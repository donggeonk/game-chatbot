import requests
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_APIKEY"))

def get_temperature(city):
    if city == "Seoul":
        return 20
    else:
        return None
    
def get_samsungUser(city):
    if(city == "Seoul"):
        return 30
    else:
        return 1
    
functions = [{
    "type": "function",
    "name": "get_temperature",
    "description": "Get the current temperature for the provided city in celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type":"string","description": "Name of the city"},
        },
        "required":["city"],},
},
{
    "type": "function",
    "name": "get_samsungUser",
    "description": "Get the current Samsung phone user for the provided city in million.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type":"string","description": "Name of the city"},
        },
        "required":["city"],},
}
]

user_input = input("User: ")
input_messages =[{"role":"user", "content": user_input},
                {"role":"system","content": "You can call a function. If no function call is required, do not call."}] #it is good to be more specific

response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = input_messages,
    functions = functions,
    function_call = "auto",
)

message = response.choices[0].message
print("First reponse: ",message)

if message.function_call:
    func_name = message.function_call.name
    args = json.loads(message.function_call.arguments)

    if func_name == "get_temperature":
        temp = get_temperature(**args) #arguments={"city":"seoul"} ** means take value 
        function_response = {"temperature": temp}
    elif func_name == "get_samsungUser":
        temp = get_samsungUser(**args)
        function_response = {"Samsung phone user count": temp}
    else:
        function_response = {"unknown function":func_name}

    followup_messages = [
        {"role":"system","content":"Reply to user using the data from function call."},
        {"role":"user","content": user_input},
        message, # first agent
        {
            "role":"function",
            "name":func_name,
            "content":json.dumps(function_response)
        }
    ]

    followup = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=followup_messages,
    )
    print("Second LLM response:", followup.choices[0].message)
    print("Bot", followup.choices[0].message.content)
else:
    print("Bot:",message.content)
