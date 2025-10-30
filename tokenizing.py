import tiktoken

#load environment variables
encoding = tiktoken.encoding_for_model("gpt-4.1-mini")

#encode a text string into tokens
tokens = encoding.encode("Hi my name is John Doe and I like banoffee pie")
#print the encoded tokens
print(tokens)

#loop tokens and print their text representation
for token_id in tokens:
    token_text = encoding.decode([token_id])
    print(f"{token_id} = {token_text}")

#example to print a token in this case 326 = and
print(encoding.decode([326]))

######################################################################

import os
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")

from openai import OpenAI

openai = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi! I'm Mike!"}
    ]
print('Processing Call')
#this will work fine
response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
print(response.choices[0].message.content)

#this will not continue working because every call is stateless, so it won't remember the previous call's state
#Tools like Grok continuously append to the dict, an invisible trick 
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What's my name?"}
    ]

print('Processing Bad Example Call')
response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
print(response.choices[0].message.content)

# In order for this to work propberly we need to add everything to the call as below
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi! I'm Mike!"},
    {"role": "assistant", "content": "Hi Mike! How can I assist you today?"},
    {"role": "user", "content": "What's my name?"}
    ]
print('Processing Good Call')
response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
print(response.choices[0].message.content)

"""
https://platform.openai.com/tokenizer
1. Every call to an LLM is stateless
2. We pass in the entire conversation so far in the input prompt, every time
3. This gives the illusion that the LLM has memory - it apparently keeps the context of the conversation
4. But this is a trick; it's a by-product of providing the entire conversation, every time
5. Context windows are the allowance for input
6. A context window is the maximum number of tokens that the model can process in a single call
7. By providing the entire conversation, we're essentially creating a context window of the entire conversation
A contexxt window is on line 59
8. If you want to keep the conversation stateful, you would need to break up the conversation into smaller chunks and make separate calls for each chunk
"""