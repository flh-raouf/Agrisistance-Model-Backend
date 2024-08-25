from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import requests
from dotenv import load_dotenv
import os
from typing import List, Optional, Dict, Any
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
    messages: List[Message]
    max_token: int
    temperature: float
    response_format: str
    # function: Optional[Dict[str, Any]]  
    user_id: Optional[str]

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
        # "function": request.function,
        "user_id": request.user_id
    }
    
    response = requests.post(
        os.getenv('API_URL'),
        json=payload,
        headers=headers
    )
    return response.json()
