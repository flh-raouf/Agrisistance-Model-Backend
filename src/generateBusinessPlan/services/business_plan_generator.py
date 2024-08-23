# services/business_plan_generator.py

import requests
import json
from typing import List, Dict

def generate_business_plan(
    crops_data: List[Dict], 
    soil_params: Dict, 
    weather_data: Dict, 
    budget: float, 
    total_area: float,
    api_token: str,
    api_url: str
) -> dict:
    prompt = f"""You are an AI assistant specialized in agricultural business planning. Your task is to generate a detailed agricultural business plan based on the provided data. The plan should be comprehensive, data-driven, and tailored to the specific crops, soil conditions, weather, and budget provided.

Please generate a detailed agricultural business plan with the following sections. For each section, provide a long, well-explained paragraph of at least 150 words. The output should be in JSON format with two main dictionaries: BP (for the paragraphs) and variables (for calculated metrics):

1. Executive Summary: Provide a brief overview of the entire plan.

2. Resources: Discuss the recommended number of workers, affordable workers based on the budget of ${budget}, suggested machines for the crops ({', '.join([crop['name'] for crop in crops_data])}), recommended pesticides, soil vitamins, and products based on the soil parameters ({soil_params}), and potential farm improvements.

3. Crops: For each crop ({', '.join([crop['name'] for crop in crops_data])}), discuss best practices for soil preparation, crop maintenance, growth maintenance tips, and recommended area and budget allocation.

4. Weather: Based on the weather data ({weather_data}), suggest best measures to ensure high revenue and protective measures for the crops.

5. Soil/Crops Maintenance: Provide a detailed maintenance schedule, including watering frequency and amount, fertilization schedule, and pest control measures.

6. Profits: Discuss expected numbers and total investment returns based on the crop data ({crops_data}), and suggest procedures to improve profitability.

7. Other Recommendations: Provide additional suggestions to improve growth, land use, or investment returns.

In the 'variables' dictionary, include the following calculated metrics:
- Human Coverage: Ratio of workers the farmer can afford to workers needed
- Water Availability: Ratio of water available in the area to water needed
- Land Use: Ratio of area used (sum of crop areas) to total area ({total_area})
- Pesticides Levels: Percentage of pesticides recommended for the crop types
- Distribution Optimality: Percentage of how optimal the space between crops is

Please ensure all output is in valid JSON format."""

    headers = {
        'Content-Type': 'application/json',
        'api_token': api_token
    }
    
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 3000,
        'temperature': 0.7,
        'user_id': 'agricultural_business_planner'
    }

    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        try:
            content = response.json()['response']['messages'][0]['content']
            return json.loads(content)
        except json.JSONDecodeError:
            return {"error": f"Unable to parse JSON response. Raw content: {content}"}
    else:
        return {"error": f"{response.status_code} - {response.text}"}
