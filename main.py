from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from Notebooks.prediction_controller import get_predictions

app = FastAPI()

class InputData(BaseModel):
    input: list[float] 

@app.post('/predict')
async def predict(data: InputData):
    try:
    
        # Get predictions from the model
        predictions = get_predictions(data.input)    

        return {"predictions": predictions.tolist()}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8082)

