import json

#C / loggings done
def parse_detailed_business_plan_response(response):
    try:
        print("Parsing detailed business plan response...")  # Debug: Start of function

        # Parse the JSON content from the response
        #print("Original response:", response)  # Debug: Print the original response
        business_plan_json = json.loads(response)  # Convert the response string into a JSON object
        print("Parsed business plan JSON:", business_plan_json)  # Debug: Print the parsed JSON
        print("A")
        content = json.loads(business_plan_json["response"]["messages"][0]["content"])  # Extract and parse the content part of the response
        print("Content extracted from response:", content)  # Debug: Print the extracted content
        print("B")
        # Extract the business plan sections from the parsed content
        bp = content["BP"]  # Business plan details
        print("Business plan details (BP):", bp)  # Debug: Print business plan details
        variables = content["variables"]  # Key variables impacting the plan
        print("C")
        print("Variables impacting the plan:", variables)  # Debug: Print key variables

        # Build a structured JSON object for the business plan with key sections
        readable_plan_json = {
            "Executive Summary": bp.get("Executive Summary", ""),  # Summary of the business plan
            "Resources": bp.get("Resources", ""),  # Resources required
            "Crops": bp.get("Crops", ""),  # Crops details
            "Weather Considerations": bp.get("Weather", ""),  # Weather-related considerations
            "Soil/Crop Maintenance": bp.get("Soil/Crops Maintenance", ""),  # Maintenance for soil and crops
            "Profit Estimations": bp.get("Profits", ""),  # Estimations of profits
            "Other Recommendations": bp.get("Other Recommendations", ""),  # Additional recommendations
            "Key Variables Impacting the Plan": {  # Variables that have a significant impact on the business plan
                "Human Coverage": variables.get("Human Coverage", ""),
                "Water Availability": variables.get("Water Availability", ""),
                "Land Use": variables.get("Land Use", ""),
                "Pesticides Levels": variables.get("Pesticides Levels", ""),
                "Distribution Optimality": variables.get("Distribution Optimality", "")
            }
        }
        print("Structured business plan JSON:", readable_plan_json)  # Debug: Print the structured JSON

        # Return the structured JSON object as a formatted string
        return json.dumps(readable_plan_json, indent=2)

    except Exception as e:
        # Log and return an error message if parsing fails
        print(f"Error parsing detailed business plan response: {e}")
        return f"Error parsing business plan: {e}"


def parse_business_plan_response(response):
    try:
        print("Parsing business plan response...")  # Debug: Start of function

        # Parse the JSON content from the response
        print("Original response:", response)  # Debug: Print the original response
        business_plan_json = json.loads(response)  # Convert the response string into a JSON object
        #print("Parsed business plan JSON:", business_plan_json)  # Debug: Print the parsed JSON

        content = json.loads(business_plan_json["response"]["messages"][0]["content"])  # Extract and parse the content part of the response
        #print("Content extracted from response:", content)  # Debug: Print the extracted content

        # Extract the business plan sections from the parsed content
        bp = content["BP"]  # Business plan details
       # print("Business plan details (BP):", bp)  # Debug: Print business plan details
        variables = content["variables"]  # Key variables impacting the plan
       # print("Variables impacting the plan:", variables)  # Debug: Print key variables

        # Build a readable business plan text by concatenating sections
        readable_plan = "Business Plan Overview:\n\n"
        for section, details in bp.items():
           # print(f"Adding section: {section}, Details: {details}")  # Debug: Print each section being added
            readable_plan += f"{section}:\n{details}\n\n"  # Append each section and its details to the overview

        # Add key variables impacting the business plan to the overview
        readable_plan += "Key Variables:\n\n"
        for variable, value in variables.items():
            print(f"Adding variable: {variable}, Value: {value}")  # Debug: Print each variable being added
            readable_plan += f"{variable}: {value}\n"  # Append each variable and its value

        # Return the readable plan text, ensuring no trailing whitespace
        print("Final readable plan:", readable_plan.strip())  # Debug: Print the final readable plan
        return readable_plan.strip()

    except Exception as e:
        # Log and return an error message if parsing fails
        print(f"Error parsing business plan response: {e}")
        return f"Error parsing business plan: {e}"
