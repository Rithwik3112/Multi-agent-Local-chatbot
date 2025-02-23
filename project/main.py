import ollama
import yfinance as yf
import json
from typing import Dict, Callable
from stockprice import get_stock_price
from langchain_ollama import OllamaLLM
from genaral import handle_prompt as general_handle_prompt  # ✅ Avoid function name conflict
from weather_agent import  get_weather_info
from whats_app import send_whatsapp_message
from command  import execute_command
from Timetable import get_timetable
# Define tool functions
get_stock_price_tool = {
    'type': 'function',
    'function': {
        'name': 'get_stock_price',
        'description': 'Get the current stock price for any symbol',
        'parameters': {
            'type': 'object',
            'required': ['symbol'],
            'properties': {
                'symbol': {'type': 'string', 'description': 'The stock symbol (e.g., AAPL, GOOGL)'},
            },
        },
    },
}

get_timetable_tool = {
    'type': 'function',
    'function': {
        'name': 'get_timetable',
        'description': 'Retrieve the class schedule based on user input queries.',
        'parameters': {
            'type': 'object',
            'required': ['query'],
            'properties': {
                'query': {'type': 'object', 'description': '''give a mongodb query as dictionary format to execute the query ex: user: which classes do I have after 2.15 on Friday
output: db.timetable.find({day: "Friday", start_time: { $gt: "2:15" }}, { _id: 0, subject: 1, instructor: 1, room: 1, start_time: 1, end_time: 1} '''}

            },
        },
    },
}   
command_tool = {
    'type': 'function',
    'function': {
        'name': 'execute_command',
        'description': 'Performs file and folder operations like creating, deleting, opening, and finding files or directories.',
        'parameters': {
            'type': 'object',
            'required': ['action', 'location', 'name'],
            'properties': {
                'action': {
                    'type': 'string',
                    'description': "The action to perform. Supported actions: 'create', 'delete', 'open', 'find'.",
                    'enum': ['create', 'delete', 'open', 'find']
                },
                'location': {
                    'type': 'string',
                    'description': "The directory where the operation will take place. Supports predefined system folders like 'desktop', 'documents', 'downloads', 'pictures', 'music', 'videos', 'onedrive', 'appdata', 'localappdata', 'programfiles', 'programfilesx86', 'rdisk', 'cdrive', and 'ddrive'.",
                },
                'name': {
                    'type': 'string',
                    'description': "The name of the file or folder to be created, deleted, opened, or found. Include the file extension for files (e.g., 'note.txt')."
                },
            },
        },
    },
}

general_conversation = {
    'type': 'function',
    'function': {
        'name': 'handle_prompt',
        'description': 'Handles general conversation and responds appropriately to user queries.',
        'parameters': {
            'type': 'object',
            'required': ['prompt'],
            'properties': {
                'prompt': {
                    'type': 'string',
                    'description': 'The user’s message or query that needs to be processed.',
                },
            },
        },
    },
}

whatsapp_message = {
    'type': 'function',
    'function': {
        'name': 'send_whatsapp_message',
        'description': 'Sends a WhatsApp message to a specified contact.',
        'parameters': {
            'type': 'object',
            'required': ['contact_name', 'message'],
            'properties': {
                'contact_name': {
                    'type': 'string',
                    'description': 'The name of the contact to whom the message should be sent.',
                },
                'message': {
                    'type': 'string',
                    'description': 'The message content that needs to be sent.',
                },
            },
        },
    },
}

get_weather_tool = {
    'type': 'function',
    'function': {
        'name': 'get_weather_info',
        'description': 'Fetch current weather details based on the user\'s public IP location.',
        'parameters': {
            'type': 'object',
            'required': [],
            'properties': {},
        },
    },
}

# Map function names to actual implementations
available_functions: Dict[str, Callable] = { 
    'handle_prompt': general_handle_prompt, 
    'get_stock_price': get_stock_price,
    'get_timetable': get_timetable,
    'get_weather_info':get_weather_info,
    'send_whatsapp_message': send_whatsapp_message,
    'execute_command': execute_command, 
     
}

def process_prompt(user_input):
    messages = [{"role": "user", "content": user_input}]

    response = ollama.chat(
        model='lappy',
        messages=messages,
        tools=[get_stock_price_tool, get_timetable_tool,general_conversation,get_weather_tool,whatsapp_message,command_tool],
        stream=False  # ✅ Ensure streaming is disabled
    )
    print (response)
    if 'message' in response and 'tool_calls' in response['message']:
        for tool in response['message']['tool_calls']:
            function_name = tool['function']['name']
            arguments = tool['function']['arguments']  # ✅ Fix JSON parsing
            function_output = available_functions[function_name](**arguments)
    print(function_output)
    return function_output

process_prompt("which classes do i have on monday")



