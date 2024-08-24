import json

def parse_detailed_business_plan_response(response):
    try:
        # Parse the JSON content from the response
        business_plan_json = json.loads(response)
        content = json.loads(business_plan_json["response"]["messages"][0]["content"])

        # Extract the business plan sections
        bp = content["BP"]
        variables = content["variables"]

        # Build a structured JSON object for the business plan
        readable_plan_json = {
            "Executive Summary": bp.get("Executive Summary", ""),
            "Resources": bp.get("Resources", ""),
            "Crops": bp.get("Crops", ""),
            "Weather Considerations": bp.get("Weather", ""),
            "Soil/Crop Maintenance": bp.get("Soil/Crops Maintenance", ""),
            "Profit Estimations": bp.get("Profits", ""),
            "Other Recommendations": bp.get("Other Recommendations", ""),
            "Key Variables Impacting the Plan": {
                "Human Coverage": variables.get("Human Coverage", ""),
                "Water Availability": variables.get("Water Availability", ""),
                "Land Use": variables.get("Land Use", ""),
                "Pesticides Levels": variables.get("Pesticides Levels", ""),
                "Distribution Optimality": variables.get("Distribution Optimality", "")
            }
        }

        return json.dumps(readable_plan_json, indent=2)

    except Exception as e:
        return f"Error parsing business plan: {e}"

# Example usage
response = '''
    {"response":{"model":"gpt-3.5-turbo-0125","token_usage":{"total":1291,"input":758,"output":533},"messages":[{"role":"assistant","content":"{\\n    \\"BP\\": {\\n        \\"Executive Summary\\": \\"This agricultural business plan aims to maximize profits by growing a variety of crops (date, mushroom, prickly pear, apricot, peppermint, lavender, basil, flax) based on soil conditions, weather data, and a budget of $50000. The plan includes recommendations for resource allocation, crop maintenance, weather protection measures, and profit optimization strategies.\\",\\n        \\"Resources\\": \\"For the recommended crops, the plan suggests hiring a specific number of workers based on the budget constraint of $50000. Additionally, it recommends investing in machines suitable for each crop, using specific pesticides, soil vitamins, and products based on the soil parameters provided. Potential farm improvements such as irrigation systems or soil drainage enhancements are also suggested to optimize crop growth and yield.\\",\\n        \\"Crops\\": \\"Each crop (date, mushroom, prickly pear, apricot, peppermint, lavender, basil, flax) requires specific soil preparation techniques, maintenance practices, growth tips, and budget allocations. For example, apricot trees may need well-drained soil and regular pruning, while basil thrives in warm, sunny conditions with adequate water supply. Proper area allocation and budget management are crucial for successful crop cultivation.\\",\\n        \\"Weather\\": \\"Considering the low annual rainfall and moderate average temperature in the area, it is essential to implement efficient irrigation systems and moisture retention techniques to ensure optimal crop growth. Protective measures such as mulching or shade structures can also help crops withstand extreme weather conditions and maximize revenue.\\",\\n        \\"Soil/Crops Maintenance\\": \\"A detailed maintenance schedule including watering frequency, fertilization routines, and pest control measures is crucial for crop health and yield optimization. Monitoring soil moisture levels, nutrient deficiencies, and pest infestations regularly can help prevent crop diseases and ensure sustainable growth throughout the season.\\",\\n        \\"Profits\\": \\"Based on the predicted revenue and area allocation for each crop, the plan estimates the total investment returns and discusses strategies to improve profitability. By analyzing crop performance, adjusting resource allocation, and exploring market opportunities, the business can enhance revenue streams and maximize overall profits.\\",\\n        \\"Other Recommendations\\": \\"To further improve growth, land use efficiency, and investment returns, the plan suggests exploring alternative crop varieties, implementing sustainable farming practices, and diversifying income sources through value-added products or agritourism initiatives.\\"\\n    },\\n    \\"variables\\": {\\n        \\"Human Coverage\\": 0.8,\\n        \\"Water Availability\\": 0.9,\\n        \\"Land Use\\": 0.6,\\n        \\"Pesticides Levels\\": 75,\\n        \\"Distribution Optimality\\": 85\\n    }\\n}"}],"finish_reason":"stop"}}
'''

print(parse_detailed_business_plan_response(response))
