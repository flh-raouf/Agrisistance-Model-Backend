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
    




def parse_business_plan_response(response):
    try:
        # Parse the JSON content from the response
        business_plan_json = json.loads(response)
        content = json.loads(business_plan_json["response"]["messages"][0]["content"])

        # Extract the business plan sections
        bp = content["BP"]
        variables = content["variables"]

        # Build a readable business plan text
        readable_plan = "Business Plan Overview:\n\n"
        for section, details in bp.items():
            readable_plan += f"{section}:\n{details}\n\n"

        readable_plan += "Key Variables:\n\n"
        for variable, value in variables.items():
            readable_plan += f"{variable}: {value}\n"

        return readable_plan.strip()

    except Exception as e:
        return f"Error parsing business plan: {e}"