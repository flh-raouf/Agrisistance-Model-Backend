from .db_connection import get_db_connection
from psycopg2.extras import RealDictCursor
import re


def get_model_inputs(land_id):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    try:
        # Check if the land_id exists in the database
        cursor.execute("SELECT * FROM land WHERE land_id = %s", (land_id,))
        land_exists = cursor.fetchone()

        if not land_exists:
            raise ValueError("Land ID does not exist in the database")

        # Fetch land data
        cursor.execute("SELECT * FROM land WHERE land_id = %s", (land_id,))
        land_data = cursor.fetchone()

        # Fetch weather data
        cursor.execute("SELECT * FROM weather WHERE land_id = %s", (land_id,))
        weather_data = cursor.fetchone()

        # Fetch financial data
        cursor.execute("SELECT * FROM finance WHERE land_id = %s", (land_id,))
        financial_data = cursor.fetchone()

        if not all([land_data, weather_data, financial_data]):
            raise ValueError("Missing required data for the given land_id")

        # Prepare the model inputs
        model_inputs = [
            land_data['ph_level'], weather_data['temperature'], weather_data['rainfall'], 
            weather_data['humidity'], land_data['nitrogen'], land_data['phosphorus'], 
            land_data['potassium'], land_data['oxygen_level'], 
            financial_data['investment_amount'], land_data['land_size']
        ]

        return model_inputs

    finally:
        cursor.close()
        connection.close()


def process_business_plan_and_save(businessPlan, cropData, land_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Delete existing records for the given land_id
        cursor.execute("DELETE FROM businessplan WHERE land_id = %s", (land_id,))
        cursor.execute("DELETE FROM landstatistic WHERE land_id = %s", (land_id,))
        cursor.execute("DELETE FROM cropmaintenance WHERE land_id = %s", (land_id,))

        # Insert into Business_Plans table
        cursor.execute("""
            INSERT INTO businessplan (executive_summary, resources, crops, weather_considerations, 
                                      soil_maintenance, profit_estimations, other_recommendations, land_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (businessPlan['Executive Summary'], businessPlan['Resources'], businessPlan['Crops'], 
              businessPlan['Weather Considerations'], businessPlan['Soil/Crop Maintenance'], 
              businessPlan['Profit Estimations'], businessPlan['Other Recommendations'], land_id))

        # Insert into Land_Statistics table
        cursor.execute("""
            INSERT INTO landstatistic (land_use, human_coverage, water_availability, 
                                       distribution_optimality, total_profit, land_id) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (businessPlan['Key Variables Impacting the Plan']['Land Use'], 
              businessPlan['Key Variables Impacting the Plan']['Human Coverage'], 
              businessPlan['Key Variables Impacting the Plan']['Water Availability'], 
              businessPlan['Key Variables Impacting the Plan']['Distribution Optimality'], 
              cropData.get('total_profit'), land_id))

        # Insert into Crop_Maintenance table
        cursor.execute("""
            INSERT INTO cropmaintenance (pesticide_level, water_sufficienty, land_id) 
            VALUES (%s, %s, %s)
        """, (businessPlan['Key Variables Impacting the Plan']['Pesticides Levels'], 
              businessPlan['Key Variables Impacting the Plan']['Water Availability'], land_id))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def clean_value(value):
    if isinstance(value, (int, float)):
        return float(value)  # Convert directly if it's already a number

    if not isinstance(value, str):
        return None  # Return None for non-string values that cannot be converted

    # Remove currency symbols and commas
    value = re.sub(r'[^\d.]', '', value)
    
    try:
        return float(value) if value else 0.0
    except ValueError:
        return value
    


def clean_value(value):
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return None
    value = re.sub(r'[^\d.]', '', value)
    try:
        return float(value) if value else 0.0
    except ValueError:
        return value

def process_crops_and_save(cropData, land_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Delete existing crop data for the given land_id
        cursor.execute("DELETE FROM crop WHERE land_id = %s", (land_id,))

        optimal_allocation = cropData.get("optimal_allocation", [])
        total_expected_return_in_money = clean_value(cropData.get("total_expected_return_in_money"))

        for crop in optimal_allocation:
            cursor.execute("""
                INSERT INTO crop (crop_name, crop_area, expected_weight_return, 
                                  expected_money_return, crop_investment, land_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (crop.get("crop"), clean_value(crop.get("area")), 
                  clean_value(crop.get("expected_return_in_weight")), 
                  clean_value(crop.get("expected_return_in_money")), 
                  clean_value(crop.get("cost")), land_id))

        cursor.execute("""
            UPDATE finance 
            SET expected_revenue = %s 
            WHERE land_id = %s
        """, (total_expected_return_in_money, land_id))

        connection.commit()

    finally:
        cursor.close()
        connection.close()