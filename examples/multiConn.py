# imports

import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set (and this is optional)")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")

# Connect to OpenAI client library
# A thin wrapper around calls to HTTP endpoints

openai = OpenAI()

# For Gemini, DeepSeek and Groq, we can use the OpenAI python client
# Because Google and DeepSeek have endpoints compatible with OpenAI
# And OpenAI allows you to change the base_url

anthropic_url = "https://api.anthropic.com/v1/"
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
ollama_url = "http://localhost:11434/v1"

anthropic = OpenAI(api_key=anthropic_api_key, base_url=anthropic_url)
gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)
ollama = OpenAI(api_key="ollama", base_url=ollama_url)

tell_a_joke = [
    {"role": "user", "content": "Tell a joke for a student on the journey to becoming an expert in LLM Engineering"},
]


#response = openai.chat.completions.create(model="gpt-4.1-mini", messages=tell_a_joke)
#answer1 = response.choices[0].message.content
#print("OpenAI Says: \n" +answer1)

#response = anthropic.chat.completions.create(model="claude-sonnet-4-5-20250929", messages=tell_a_joke)
#answer2 = response.choices[0].message.content
#print("Anthropic Says: \n" + answer2)

#response = ollama.chat.completions.create(model="llama3.2", messages=tell_a_joke)
#answer3 = response.choices[0].message.content
#print("Ollama Says: \n" + answer3)


# Training vs Inference time scaling Display the difference in inference time between models 
easy_puzzle = [
    {"role": "user", "content": 
        "You toss 2 coins. One of them is heads. What's the probability the other is tails? Answer with the probability only."},
]

#response = openai.chat.completions.create(model="gpt-5-nano", messages=easy_puzzle, reasoning_effort="minimal")
#print("Wrong - Minimal Reasoning:  " + response.choices[0].message.content)

#response = openai.chat.completions.create(model="gpt-5-nano", messages=easy_puzzle, reasoning_effort="low")
#print("Correct - Low Effort  " + response.choices[0].message.content)

#response = openai.chat.completions.create(model="gpt-5-mini", messages=easy_puzzle, reasoning_effort="minimal")
#print("Correct - different but larger model  " + response.choices[0].message.content)

#response = ollama.chat.completions.create(model="llama3.2", messages=easy_puzzle)
#print("Ollama 3.2:= Wrong - " + response.choices[0].message.content)



# the answer to this is 4mm
hard = """
On a bookshelf, two volumes of Pushkin stand side by side: the first and the second.
The pages of each volume together have a thickness of 2 cm, and each cover is 2 mm thick.
A worm gnawed (perpendicular to the pages) from the first page of the first volume to the last page of the second volume.
What distance did it gnaw through?
"""
hard_puzzle = [
    {"role": "user", "content": hard}
]

#response = openai.chat.completions.create(model="gpt-5-nano", messages=hard_puzzle, reasoning_effort="minimal")
#print("Wrong GPT 5 NANO : " + response.choices[0].message.content)

#response = anthropic.chat.completions.create(model="claude-sonnet-4-5-20250929", messages=hard_puzzle)
#print("Wrong Claude Sonnet 4.5.2 : " + response.choices[0].message.content)

#response = openai.chat.completions.create(model="gpt-5", messages=hard_puzzle)
#print("Correct:GPT 5 : " + response.choices[0].message.content)

#response = gemini.chat.completions.create(model="gemini-2.5-pro", messages=hard_puzzle)
#print("Correct - Gemini 2.5 Pro : " + response.choices[0].message.content)





#Lets see how these models play nice or dirty with no errot secified
dilemma_prompt = """
You and a partner are contestants on a game show. You're each taken to separate rooms and given a choice:
Cooperate: Choose "Share" — if both of you choose this, you each win $1,000.
Defect: Choose "Steal" — if one steals and the other shares, the stealer gets $2,000 and the sharer gets nothing.
If both steal, you both get nothing.
Do you choose to Steal or Share? Pick one.
"""

dilemma = [
    {"role": "user", "content": dilemma_prompt},
]

#response = anthropic.chat.completions.create(model="claude-sonnet-4-5-20250929", messages=dilemma)
#print("Anthropic Says: " + response.choices[0].message.content)

#response = openai.chat.completions.create(model="gpt-5-nano", messages=dilemma)
#print("OpenAI Says: " + response.choices[0].message.content)

#response = gemini.chat.completions.create(model="gemini-2.5-pro", messages=dilemma)
#print("Gemini Says: " + response.choices[0].message.content)

#response = ollama.chat.completions.create(model="llama3.2", messages=dilemma)
#print("Ollama Says: " + response.choices[0].message.content)

# run 1,2 & 3: Anth Share, OpenAI Steal, Gemini Share, Ollama Share