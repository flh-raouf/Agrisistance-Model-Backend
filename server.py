from flask import Flask, jsonify, request, make_response
from asgiref.wsgi import WsgiToAsgi
import requests
import time
import json
import os
import traceback

from src.predictOptimizeCrops.main import predict_optimize_crops_main
from src.generateBusinessPlan.main import generate_business_plan_main
from src.chatBot.chat_service import ChatRequest

from DB.db_operations import get_model_inputs, process_business_plan_and_save, process_crops_and_save

app = Flask(__name__)

@app.route('/')
async def root():
    print("Root endpoint accessed")
    return jsonify({"message": "Welcome to Agrissistance Models API"})

@app.route('/generate-business-plan', methods=['POST'])
async def generate_business_plan():
    start_time = time.time()
    
    try:
        print("Received request to generate business plan")
        data = request.get_json()
        print(f"Received data: {data}")
        land_id = data.get('land_id')
        print(f"Land ID: {land_id}")
        
        # Fetch necessary data from the database using the land_id
        print("Fetching model inputs")
        try:
            model_inputs =  get_model_inputs(land_id)
            print(f"Model inputs: {model_inputs}")
        except Exception as e:
            print(f"Error fetching model inputs: {str(e)}")
            print(traceback.format_exc())
            raise

        # Pass the model inputs to the crop prediction function
        print("Predicting and optimizing crops")
        try:
            cropData = predict_optimize_crops_main(model_inputs)
            print(f"Crop data type: {type(cropData)}")
            if isinstance(cropData, str):
                cropData = json.loads(cropData)
            #print(f"Crop data: {cropData}")
        except Exception as e:
            print(f"Error in crop prediction: {str(e)}")
            print(traceback.format_exc())
            raise

        print("Generating business plan")
        try:
            businessPlan = generate_business_plan_main(model_inputs, cropData)
            print(f"Business plan type: {type(businessPlan)}")
            if isinstance(businessPlan, str):
                businessPlan = json.loads(businessPlan)
           # print(f"Business plan: {businessPlan}")
        except Exception as e:
            print(f"Error generating business plan: {str(e)}")
            print(traceback.format_exc())
            raise

        # Save the business plan and crop data to the database
        print("Saving business plan and crop data")
        try:
             process_business_plan_and_save(businessPlan, cropData, land_id)
             process_crops_and_save(cropData, land_id)
        except Exception as e:
            print(f"Error saving data to database: {str(e)}")
            print(traceback.format_exc())
            raise

        print("Successfully generated and saved business plan and crop data")
        return jsonify({
            "cropData": cropData,
            "businessPlan": businessPlan
        })
    
    except Exception as e:
        print(f"An error occurred in generate_business_plan: {str(e)}")
        print(traceback.format_exc())
        return make_response(jsonify({"detail": str(e)}), 500)
    
    finally:
        execution_time = time.time() - start_time  
        print(f"Execution time: {execution_time:.2f} seconds")

@app.route("/chat", methods=['POST'])
async def chat():
    try:
        print("Received chat request")
        headers = {
            'Content-Type': 'application/json',
            'api_token': os.getenv('API_TOKEN')
        }
        print(f"Using API token: {headers['api_token']}")
        payload = request.get_json()
        print(f"Chat request payload: {payload}")
        
        print("Sending request to chat API")
        response = requests.post(
            os.getenv('API_URL'),
            json=payload,
            headers=headers
        )
        print(f"Chat API response status code: {response.status_code}")
        print(f"Chat API response content: {response.text}")
        
        return jsonify(response.json())
    
    except Exception as e:
        print(f"An error occurred in chat endpoint: {str(e)}")
        print(traceback.format_exc())
        return make_response(jsonify({"detail": str(e)}), 500)

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    print("Starting the Flask application")
    app.run()