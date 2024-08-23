from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

from src.predictOptimizeCrops.main import predict_optimize_crops_main
from src.generateBusinessPlan.main import generate_business_plan_main




app = FastAPI()

class InputData(BaseModel):
    input: list[float] 


@app.post('/generate-business-plan')
async def predict(data: InputData):
    try:  
        InputData = data.input
        cropData = predict_optimize_crops_main(InputData)
        if isinstance(cropData, str):
            cropData = json.loads(cropData)
        print(cropData)
        businessPlan = generate_business_plan_main(InputData, cropData)
        print (businessPlan)
        return {"message": "Prediction Complete!", "data": businessPlan}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/')
async def root():
    return {"message": "Welcome to the API"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8082)

