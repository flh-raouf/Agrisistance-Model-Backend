from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import os

from src.predictOptimizeCrops.main import predict_optimize_crops_main
from src.generateBusinessPlan.main import generate_business_plan_main
from src.chatBot.chat_service import ChatRequest

from src.generateBusinessPlan.util.parseBusinessPlan import parse_detailed_business_plan_response





app = FastAPI()

class InputData(BaseModel):
    input: list[float] 


@app.get('/')
async def root():
    return {"message": "Welcome to the API"}



@app.post('/generate-business-plan')
async def predict(data: InputData):
    try:  
        InputData = data.input

        cropData = predict_optimize_crops_main(InputData)
        if isinstance(cropData, str):
            cropData = json.loads(cropData)
            
        businessPlan = generate_business_plan_main(InputData, cropData)
        if isinstance(businessPlan, str):
            businessPlan = json.loads(businessPlan)

            
        return {
            "cropData": cropData,
            "businessPlan": businessPlan
        }
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    



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
    
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8082)

