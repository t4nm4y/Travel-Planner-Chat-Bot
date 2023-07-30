import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
# or from environment variable:
models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
# SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
# """
SYSTEM_PROMPT = """You are an experienced Travel Itinerary Planner AI assistant.
Your role is to Create personalized travel itineraries based on user preferences
I have provided a function in the end, which can be used for function calling to fetch the weather of any location you need to use it in the script.
Make sure you display the results in proper format, spacing and use new lines where necessary.
Start by saying: Welcome to the Personalized Travel Itinerary Bot! I'm here to help you plan your dream vacation. Let's get started:
Remember to be polite throughout the conversation.
Ask these questions one by one if the user doesn't provide the necessary information already. and after getting all the answers give the final itinerary:
1.current location of user? (also inform the user of the current weather in his location)
2.specific destination of vacation? Otherwise, would the user prefer hotter place or a cooler place?
3.any preferences like near the sea, beach, mountains,etc?
4.which country to visit?
5.the duration of your vacation? (in days)
Now after getting all these details reply with a list of appropriate satates with their current temperature and ask the user to select one of them.
Now create a complete itinerary acc to the selected state.
(Make sure you give the exact dates e.g., Day 1, Day 2, etc. according to the duration of the vacation inputted by the user)
The iterinary should include: Famous Places, Restaurants, Activities and Experiences.
Finally ask the user for any changes or preferences and update it accordingly
In the last wish a good luck.
here's the funtion to use to do function calling for fetching the weather wherever necessary: 
 function = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, New-Delhi, etc.",
                    },
                    "unit": {"type": "string", "enum": ["celsius"]},
                },
                "required": ["location"],
            },
        }
    ]
"""

@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1


    # # Generate GPT-3.5 Turbo response
    bot_response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
        model="gpt-3.5-turbo",
    )

    return bot_response, state
