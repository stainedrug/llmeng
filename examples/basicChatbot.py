import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

## This is a BASIC chatbot using gradio for the interface using openai's API

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

openai = OpenAI()
MODEL = 'gpt-4.1-mini'

system_message = "You are a helpful assistant"

def chat(messages, history):
    #this is for gemini or other apis that rewuire metadata
    history = [{"role":h["role"], "content": h["content"]} for h in history] 
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": messages}]
    response =  openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content

#gr.ChatInterface(fn=chat, type="messages").launch()



#Now lets make this a bit more specialized to demostrate a specific use, a pushy saleseman looking to rid excess inventory

system_message = "You are a helpful assistant in a clothes store. You should try to gently encourage \
the customer to try items that are on sale. Socks are 70% off, and most other items are 40% off. \
For example, if the customer says 'I'm looking to buy socks', \
you could reply something like, 'Wonderful - we have lots of socks - including several that are part of our sales event.'\
Encourage the customer to buy socks if they are unsure what to get."

system_message += "\nIf the customer asks for shoes, you should respond that shoes are not on sale today, \
but remind the customer to look at hats!"

def chat(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history]
    relevant_system_message = system_message
    if 'belt' in message.lower():
        relevant_system_message += " The store does not sell belts; if you are asked for belts, be sure to point out other items on sale."
    
    messages = [{"role": "system", "content": relevant_system_message}] + history + [{"role": "user", "content": message}]

    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)
# Gradio knows this is a generator function
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response


gr.ChatInterface(fn=chat, type="messages").launch()