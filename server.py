from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


from Controllers.cropPrediction.BestCropPrediction import BestCropPredictionMain
from Controllers.OptimizationPrediction.optimization_algorithm_independent import OptimizationMain

app = FastAPI()

class InputData(BaseModel):
    input: list[float] 

@app.post('/predict')
async def predict(data: InputData):
    try:
    
        # Get predictions from the model
        firstPredictions = BestCropPredictionMain(data.input)
        secondPredictions = OptimizationMain(firstPredictions)

        
        return {
                "firstPredictions": firstPredictions,
                "secondPredictions": secondPredictions
                }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/')
async def root():
    return {"message": "Welcome to the API"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8082)

