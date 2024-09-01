#CER done
import os
import json
from typing import List, Dict
from dotenv import load_dotenv
from .services.business_plan_generator import generate_business_plan
from .util.parseBusinessPlan import parse_detailed_business_plan_response, parse_business_plan_response

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
API_TOKEN = os.getenv("API_TOKEN")  # API token for authenticating requests
API_URL = os.getenv("API_URL")  # URL of the API endpoint


def generate_business_plan_main(InputData: List[float], cropData: Dict[str, any]):
    # Extract crop data for each crop in the optimal allocation
    crops_data = [
        {
            "name": crop['crop'],  # Name of the crop
            "predicted_revenue": float(crop['expected_return_in_money'].strip('$').replace(',', '')),  # Predicted revenue in monetary value
            "weight": float(crop['expected_return_in_weight'].strip(' units').replace(',', '')),  # Expected return in weight
            "area": crop['area']  # Allocated area for the crop
        }
        for crop in cropData['optimal_allocation']
    ]
    
    # Extract soil parameters from the input data
    soil_params = {
        "pH": InputData[0],  # Soil pH value
        "nitrogen": InputData[4],  # Nitrogen level in the soil
        "phosphorus": InputData[5],  # Phosphorus level in the soil
        "potassium": InputData[6],  # Potassium level in the soil
    }

    # Extract weather data from the input data
    weather_data = {
        "annual_rainfall": InputData[2],  # Annual rainfall amount
        "average_temperature": InputData[1]  # Average temperature
    }

    # Extract budget and total area from the input data
    budget = int(InputData[8])  # Available budget for the business plan
    total_area = int(InputData[9])  # Total area available for crop cultivation

    # Log the extracted data before generating the business plan
    print(f"Generating business plan with the following data:")
    print(f"Crops Data: {crops_data}")
    print(f"Soil Parameters: {soil_params}")
    print(f"Weather Data: {weather_data}")
    print(f"Budget: {budget}, Total Area: {total_area}")
    
    # Generate business plan by calling the external service
    response = generate_business_plan(
        crops_data=crops_data,
        soil_params=soil_params,
        weather_data=weather_data,
        budget=budget,
        total_area=total_area,
        api_token=API_TOKEN,
        api_url=API_URL
    )

    # Parse the detailed business plan response
    businessPlan = parse_detailed_business_plan_response(response)
    
    return businessPlan  # Return the parsed business plan
