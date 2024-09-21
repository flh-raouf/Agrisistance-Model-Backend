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
    # Construct the prompt to send to the AI model
    prompt = f"""You are an AI assistant specialized in agricultural business planning. Your task is to generate a detailed agricultural business plan based on the provided data. The plan should be comprehensive, data-driven, and tailored to the specific crops, soil conditions, weather, and budget provided.

    Please generate a detailed agricultural business plan with the following sections. For each section, provide a long, well-explained paragraph of at least 150 words. The output should be in JSON format with two main dictionaries: BP (for the paragraphs) and variables (for calculated metrics):

    1. Executive Summary: Provide a brief overview of the entire plan.

    2. Resources: Discuss the recommended number of workers, affordable workers based on the budget of ${budget}, suggested machines for the crops ({', '.join([crop['name'] for crop in crops_data])}), recommended pesticides, soil vitamins, and products based on the soil parameters ({soil_params}), and potential farm improvements.

    3. Crops: For each crop ({', '.join([crop['name'] for crop in crops_data])}), discuss best practices for soil preparation, crop maintenance, growth maintenance tips, and recommended area and budget allocation.

    4. Weather: Based on the weather data ({weather_data}), suggest best measures to ensure high revenue and protective measures for the crops.

    5. Soil/Crops Maintenance: Provide a detailed maintenance schedule, including watering frequency and amount, fertilization schedule, and pest control measures.

    6. Profits: Discuss expected numbers and total investment returns based on the crop data ({crops_data}), and suggest procedures to improve profitability.

    7. Other Recommendations: Provide additional suggestions to improve growth, land use, or investment returns.

    In the 'variables' dictionary, include the following calculated metrics, use approximations if needed do not return null values, only numeric values:
    - Human Coverage: Ratio of workers the farmer can afford to workers needed
    - Water Availability: Ratio of water available in the area to water needed
    - Land Use: Ratio of area used (sum of crop areas) to total area ({total_area})
    - Pesticides Levels: Percentage of pesticides recommended for the crop types
    - Distribution Optimality: Percentage of how optimal the space between crops is

    Please ensure all output is in valid JSON format and no null values when expecting numerical values."""

    # Prepare the headers for the API request
    headers = {
        'Content-Type': 'application/json',
        'api_token': api_token
    }
    
    # Prepare the payload with the model and prompt data
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 3000,  # Set token limit to ensure the response is detailed but not too long
        'temperature': 0.7,  # Set creativity level of the AI response
        'user_id': 'agricultural_business_planner'
    }

    # Log the prompt being sent to the API for debugging
    # print(f"Sending prompt to API: {prompt}")
    
    # Make the POST request to the AI API
    response = requests.post(api_url, json=payload, headers=headers)
    
    # Check if the response is successful
    if response.status_code == 200:
        try:
            # Attempt to parse the JSON content from the response
            content = response.json()['response']['messages'][0]['content']
            # print("Successfully received and parsed the response from the API.")
            return json.loads(content)  # Convert the response content to a Python dictionary
        except json.JSONDecodeError:
            # Log an error message if JSON parsing fails
            print(f"Error: Unable to parse JSON response. Raw content: {content}")
            return {"error": f"Unable to parse JSON response. Raw content: {content}"}
    else:
        # Log the response code and text if the request was unsuccessful
        # print(f"Received status code {response.status_code}. Response text: {response.text}")
        return response.text  # Return the raw response text for further investigation
