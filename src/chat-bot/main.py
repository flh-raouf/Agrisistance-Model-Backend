import os
from fastapi import FastAPI, HTTPException
import requests
import numpy as np
import joblib
import pandas as pd
from chatbot.chat_service import ChatRequest  # Import the ChatRequest model

# Load the model and scaler
model = joblib.load('crop_model_simplified.joblib')
scaler = joblib.load('crop_scaler.joblib')

# Initialize FastAPI app
app = FastAPI()

# Input and parameters
total_budget = 1000  # Placeholder, will come from request
total_area = 500     # Placeholder, will come from request


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        headers = {
            'Content-Type': 'application/json',
            'api_token': os.getenv('API_TOKEN')
        }
        payload = request.dict()
        response = requests.post(
            'https://api.afro.fit/api_v2/api_wrapper/chat/completions',
            json=payload,
            headers=headers
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# To run the server, use the command:
# uvicorn main:app --reload
