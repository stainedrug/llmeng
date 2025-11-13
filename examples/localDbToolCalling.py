import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import sqlite3

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
MODEL = "gpt-4.1-mini"
openai = OpenAI()

system_message = """
You are a helpful assistant for an Airline called Fake Airlines.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
"""

def get_ticket_price(city):
    print(f"DATABASE TOOL CALLED: Getting price for {city}", flush=True)
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        pattern = f"{city}%"
        cursor.execute("""
            SELECT destination, airport_code, price
            FROM flights
            WHERE airport_code LIKE ? 
            OR destination LIKE ?
        """, (pattern, pattern))
        result = cursor.fetchone()
        print(result)
        return f"Ticket price to {city} is ${result[2]}" if result else "No price data available for this city"

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": price_function}]

def chat(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history] #req for Gemini
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    while response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        responses = handle_tool_calls(message)
        messages.append(message)
        messages.extend(responses)
        response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    
    return response.choices[0].message.content

def handle_tool_calls(message):
    responses = []
    for tool_call in message.tool_calls:
        if tool_call.function.name == "get_ticket_price":
            arguments = json.loads(tool_call.function.arguments)
            city = arguments.get('destination_city')
            price_details = get_ticket_price(city)
            responses.append({
                "role": "tool",
                "content": price_details,
                "tool_call_id": tool_call.id
            })
    return responses

DB = "prices.db"

with sqlite3.connect(DB) as conn:
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS flights (id INTEGER PRIMARY KEY AUTOINCREMENT,destination TEXT NOT NULL,airport_code TEXT NOT NULL,price REAL NOT NULL);')
    conn.commit()

#def set_ticket_price(city, price):
#    with sqlite3.connect(DB) as conn:
#        cursor = conn.cursor()
#        cursor.execute('INSERT INTO prices (city, price) VALUES (?, ?) ON CONFLICT(city) DO UPDATE SET price = ?', (city.lower(), price, price))
#        conn.commit()

#ticket_prices = {"london":799, "paris": 899, "tokyo": 1420, "sydney": 2999, "new york": 1299}
#//for city, price in ticket_prices.items():
#    set_ticket_price(city, price)

gr.ChatInterface(fn=chat, type="messages").launch()



"""
Dict Data
pythonimport sqlite3

# -------------------------------------------------
# 1. The mock data as a Python dict
# -------------------------------------------------
flights_data = {
    "Tokyo, Japan":          {"code": "NRT", "price": 987.50},
    "Paris, France":         {"code": "CDG", "price": 678.00},
    "New York, USA":         {"code": "JFK", "price": 423.75},
    "Sydney, Australia":     {"code": "SYD", "price": 1199.99},
    "Dubai, UAE":            {"code": "DXB", "price": 845.30},
    "London, UK":            {"code": "LHR", "price": 598.20},
    "Bangkok, Thailand":     {"code": "BKK", "price": 567.80},
    "Singapore, Singapore":  {"code": "SIN", "price": 712.40},
    "Los Angeles, USA":      {"code": "LAX", "price": 389.10},
    "Barcelona, Spain":      {"code": "BCN", "price": 512.60},
    "Cairo, Egypt":          {"code": "CAI", "price": 634.90},
    "Mumbai, India":         {"code": "BOM", "price": 489.20},
    "Cape Town, South Africa": {"code": "CPT", "price": 998.50},
    "Rio de Janeiro, Brazil": {"code": "GIG", "price": 876.30},
    "Toronto, Canada":       {"code": "YYZ", "price": 456.70},
    "Seoul, South Korea":    {"code": "ICN", "price": 823.40},
    "Amsterdam, Netherlands": {"code": "AMS", "price": 589.00},
    "Mexico City, Mexico":   {"code": "MEX", "price": 512.80},
    "Istanbul, Turkey":      {"code": "IST", "price": 498.20},
    "Beijing, China":        {"code": "PEK", "price": 945.60},
    "Rome, Italy":           {"code": "FCO", "price": 567.90},
    "Berlin, Germany":       {"code": "BER", "price": 489.10},
    "Hong Kong, China":      {"code": "HKG", "price": 789.50},
    "Dublin, Ireland":       {"code": "DUB", "price": 534.20},
    "Lisbon, Portugal":      {"code": "LIS", "price": 478.90},
    "Buenos Aires, Argentina": {"code": "EZE", "price": 987.30},
    "Stockholm, Sweden":     {"code": "ARN", "price": 567.80},
    "Oslo, Norway":          {"code": "OSL", "price": 589.40},
    "Vienna, Austria":       {"code": "VIE", "price": 512.70},
    "Prague, Czech Republic": {"code": "PRG", "price": 456.10},
    "Warsaw, Poland":        {"code": "WAW", "price": 434.90},
    "Athens, Greece":        {"code": "ATH", "price": 489.60},
    "Zurich, Switzerland":   {"code": "ZRH", "price": 678.20},
    "Copenhagen, Denmark":   {"code": "CPH", "price": 556.80},
    "Helsinki, Finland":     {"code": "HEL", "price": 598.10},
    "Reykjavik, Iceland":    {"code": "KEF", "price": 723.40},
    "Santiago, Chile":       {"code": "SCL", "price": 1045.90},
    "Lima, Peru":            {"code": "LIM", "price": 876.50},
    "Bogotá, Colombia":      {"code": "BOG", "price": 723.20},
    "Nairobi, Kenya":        {"code": "NBO", "price": 998.70},
    "Johannesburg, South Africa": {"code": "JNB", "price": 987.40},
    "Tel Aviv, Israel":      {"code": "TLV", "price": 756.80},
    "Kuala Lumpur, Malaysia": {"code": "KUL", "price": 678.90},
    "Jakarta, Indonesia":    {"code": "CGK", "price": 723.50},
    "Hanoi, Vietnam":        {"code": "HAN", "price": 645.20},
    "Ho Chi Minh City, Vietnam": {"code": "SGN", "price": 667.80},
    "Phuket, Thailand":      {"code": "HKT", "price": 723.10},
    "Bali, Indonesia":       {"code": "DPS", "price": 845.90},
    "Auckland, New Zealand": {"code": "AKL", "price": 1345.60},
    "Vancouver, Canada":     {"code": "YVR", "price": 567.30},
}

## INSERT STATEMENT
-- Insert 50 mock flight records
INSERT INTO flights (destination, airport_code, price) VALUES
('Tokyo, Japan', 'NRT', 987.50),
('Paris, France', 'CDG', 678.00),
('New York, USA', 'JFK', 423.75),
('Sydney, Australia', 'SYD', 1199.99),
('Dubai, UAE', 'DXB', 845.30),
('London, UK', 'LHR', 598.20),
('Bangkok, Thailand', 'BKK', 567.80),
('Singapore, Singapore', 'SIN', 712.40),
('Los Angeles, USA', 'LAX', 389.10),
('Barcelona, Spain', 'BCN', 512.60),
('Cairo, Egypt', 'CAI', 634.90),
('Mumbai, India', 'BOM', 489.20),
('Cape Town, South Africa', 'CPT', 998.50),
('Rio de Janeiro, Brazil', 'GIG', 876.30),
('Toronto, Canada', 'YYZ', 456.70),
('Seoul, South Korea', 'ICN', 823.40),
('Amsterdam, Netherlands', 'AMS', 589.00),
('Mexico City, Mexico', 'MEX', 512.80),
('Istanbul, Turkey', 'IST', 498.20),
('Beijing, China', 'PEK', 945.60),
('Rome, Italy', 'FCO', 567.90),
('Berlin, Germany', 'BER', 489.10),
('Hong Kong, China', 'HKG', 789.50),
('Dublin, Ireland', 'DUB', 534.20),
('Lisbon, Portugal', 'LIS', 478.90),
('Buenos Aires, Argentina', 'EZE', 987.30),
('Stockholm, Sweden', 'ARN', 567.80),
('Oslo, Norway', 'OSL', 589.40),
('Vienna, Austria', 'VIE', 512.70),
('Prague, Czech Republic', 'PRG', 456.10),
('Warsaw, Poland', 'WAW', 434.90),
('Athens, Greece', 'ATH', 489.60),
('Zurich, Switzerland', 'ZRH', 678.20),
('Copenhagen, Denmark', 'CPH', 556.80),
('Helsinki, Finland', 'HEL', 598.10),
('Reykjavik, Iceland', 'KEF', 723.40),
('Santiago, Chile', 'SCL', 1045.90),
('Lima, Peru', 'LIM', 876.50),
('Bogotá, Colombia', 'BOG', 723.20),
('Nairobi, Kenya', 'NBO', 998.70),
('Johannesburg, South Africa', 'JNB', 987.40),
('Tel Aviv, Israel', 'TLV', 756.80),
('Kuala Lumpur, Malaysia', 'KUL', 678.90),
('Jakarta, Indonesia', 'CGK', 723.50),
('Hanoi, Vietnam', 'HAN', 645.20),
('Ho Chi Minh City, Vietnam', 'SGN', 667.80),
('Phuket, Thailand', 'HKT', 723.10),
('Bali, Indonesia', 'DPS', 845.90),
('Auckland, New Zealand', 'AKL', 1345.60),
('Vancouver, Canada', 'YVR', 567.30);
"""