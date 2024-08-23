import os
import json
from typing import List, Dict
from dotenv import load_dotenv
from .services.business_plan_generator import generate_business_plan

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
API_TOKEN = os.getenv("API_TOKEN")
API_URL = os.getenv("API_URL")

def generate_business_plan_main(InputData: List[float], cropData: Dict[str, any]):
    # Extract crop data
    crops_data = [
        {
            "name": crop['crop'],
            "predicted_revenue": float(crop['expected_return_in_money'].strip('$').replace(',', '')),
            "weight": float(crop['expected_return_in_weight'].strip(' units').replace(',', '')),
            "area": crop['area']
        }
        for crop in cropData['optimal_allocation']
    ]
    
    # Extract soil parameters
    soil_params = {
        "pH": InputData[0],
        "nitrogen": InputData[4],
        "phosphorus": InputData[5],
        "potassium": InputData[6],
    }

    # Extract weather data
    weather_data = {
        "annual_rainfall": InputData[2],
        "average_temperature": InputData[1]
    }

    # Extract budget and total area
    budget = int(InputData[8])
    total_area = int(InputData[9])

    # Generate business plan
    result = generate_business_plan(
        crops_data=crops_data,
        soil_params=soil_params,
        weather_data=weather_data,
        budget=budget,
        total_area=total_area,
        api_token=API_TOKEN,
        api_url=API_URL
    )
    
    return result  
