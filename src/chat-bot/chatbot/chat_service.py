from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import requests
from dotenv import load_dotenv
import os
from typing import Dict, List
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# In-memory store for user conversations
conversation_history: Dict[str, List[Dict[str, str]]] = defaultdict(list)

# Define the payload structure for the chatbot request
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: list[Message]
    max_token: int = None
    temperature: float = None
    response_format: str = 'text/plain'
    function: dict = None
    user_id: str = None

    @validator('messages')
    def validate_messages(cls, messages):
        if not isinstance(messages, list) or not all(isinstance(msg, Message) for msg in messages):
            raise ValueError('Messages must be a list of Message objects')
        return messages

# Your API token
API_TOKEN = os.getenv('API_TOKEN')

def generate_content(request: ChatRequest):
    headers = {
        'Content-Type': 'application/json',
        'api_token': API_TOKEN
    }
    
    # Add a professional tone and context
    system_message = {
        "role": "system",
        "content": "You are a professional assistant helping farmers with information on crop selection, land management, and other agricultural inquiries."
    }
    
    payload = {
        "model": request.model,
        "messages": [system_message] + request.messages,  # Add system message at the beginning
        "max_token": request.max_token or 150,  # Default value
        "temperature": request.temperature or 0.7,  # Default value
        "response_format": request.response_format,
        "function": request.function,
        "user_id": request.user_id
    }
    
    response = requests.post(
        'https://api.afro.fit/api_v2/api_wrapper/chat/completions',
        json=payload,
        headers=headers
    )
    return response.json()

@app.post("/chat")
async def chat(request: ChatRequest):
    user_id = request.user_id
    if user_id:
        # Append incoming message to history
        conversation_history[user_id].append({"role": "user", "content": request.messages[-1].content})

    try:
        # Include conversation history in request
        messages_with_history = conversation_history.get(user_id, []) + request.messages
        request_with_history = ChatRequest(
            model=request.model,
            messages=messages_with_history,
            max_token=request.max_token,
            temperature=request.temperature,
            response_format=request.response_format,
            function=request.function,
            user_id=request.user_id
        )
        
        response = generate_content(request_with_history)
        
        # Append chatbot's response to history
        if user_id:
            conversation_history[user_id].append({"role": "assistant", "content": response['response']['messages'][-1]['content']})

        if response.get('error'):
            raise HTTPException(status_code=400, detail=response.get('error'))

        return response
    except requests.RequestException as req_e:
        raise HTTPException(status_code=502, detail=f"Request failed: {str(req_e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
