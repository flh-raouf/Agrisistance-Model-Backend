from flask import Flask, jsonify, request, make_response
from asgiref.wsgi import WsgiToAsgi
import requests
import time
import json
import os

from src.predictOptimizeCrops.main import predict_optimize_crops_main
from src.generateBusinessPlan.main import generate_business_plan_main
from src.chatBot.chat_service import ChatRequest

from src.prisma.db_operations import get_model_inputs, process_business_plan_and_save, process_crops_and_save

app = Flask(__name__)

@app.route('/')
async def root():
    return jsonify({"message": "Welcome to Agrissistance Models API"})

@app.route('/generate-business-plan', methods=['POST'])
async def generate_business_plan():
    start_time = time.time()
    
    try:
        data = request.get_json()
        land_id = data.get('land_id')
        
        # Fetch necessary data from the database using the land_id
        model_inputs = await get_model_inputs(land_id)

        # Pass the model inputs to the crop prediction function
        cropData = predict_optimize_crops_main(model_inputs)
        if isinstance(cropData, str):
            cropData = json.loads(cropData)

        businessPlan = generate_business_plan_main(model_inputs, cropData)
        if isinstance(businessPlan, str):
            businessPlan = json.loads(businessPlan)
              
        # Save the business plan and crop data to the database
        await process_business_plan_and_save(businessPlan, cropData, land_id)
        await process_crops_and_save(cropData, land_id)

        return jsonify({
            "cropData": cropData,
            "businessPlan": businessPlan
        })
    
    except Exception as e:
        print(e)
        return make_response(jsonify({"detail": str(e)}), 500)
    
    finally:
        execution_time = time.time() - start_time  
        print(f"Execution time: {execution_time:.2f} seconds")


@app.route("/chat", methods=['POST'])
async def chat():
    try:
        headers = {
            'Content-Type': 'application/json',
            'api_token': os.getenv('API_TOKEN')
        }
        payload = request.get_json()
        response = requests.post(
            os.getenv('API_URL'),
            json=payload,
            headers=headers
        )
        return jsonify(response.json())
    
    except Exception as e:
        return make_response(jsonify({"detail": str(e)}), 500)
    

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    app.run()
