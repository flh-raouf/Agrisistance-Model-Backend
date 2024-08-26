from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import time
import json
import os

from src.predictOptimizeCrops.main import predict_optimize_crops_main
from src.generateBusinessPlan.main import generate_business_plan_main
from src.chatBot.chat_service import ChatRequest

from DB.DBqueries import get_model_inputs, process_business_plan_and_save, process_crops_and_save


app = FastAPI()

class InputData(BaseModel):
    land_id: str


@app.get('/')
async def root():
    return {"message": "Welcome to the API"}


@app.post('/generate-business-plan')
async def generateBusinessPlan(data: InputData):
    start_time = time.time() 
    
    try:
        land_id = data.land_id

        # Fetch necessary data from the database using the land_id and user_id
        print('Fetching model inputs...')
        model_inputs = await get_model_inputs(land_id)

        # Pass the model inputs to the crop prediction function
        print('Predicting and optimizing crops...')
        cropData = predict_optimize_crops_main(model_inputs)
        if isinstance(cropData, str):
            cropData = json.loads(cropData)
            
        print('Generating business plan...')
        businessPlan = generate_business_plan_main(model_inputs, cropData)
        if isinstance(businessPlan, str):
            businessPlan = json.loads(businessPlan)

        # Save the business plan and crop data to the database
        print('Saving data to the database...')
        await process_business_plan_and_save(businessPlan, land_id)   
        await process_crops_and_save(cropData, land_id)    

        return {
            "cropData": cropData,
            "businessPlan": businessPlan
        }
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        execution_time = time.time() - start_time  
        print(f"Execution time: {execution_time:.2f} seconds")
        


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        headers = {
            'Content-Type': 'application/json',
            'api_token': os.getenv('API_TOKEN')
        }
        payload = request.dict()
        response = requests.post(
            os.getenv('API_URL'),
            json=payload,
            headers=headers
        )
        return response.json()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)

