from DB.db_connection import get_db_connection
from psycopg2.extras import RealDictCursor
import re
import uuid

'''
def get_db_schema():
    connection = get_db_connection()
    cursor = connection.cursor()
    schema = {}
    
    try:
        # Get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}'
            """)
            columns = cursor.fetchall()
            schema[table_name] = {col[0]: col[1] for col in columns}
        
        print("Current Database Schema:")
        for table, columns in schema.items():
            print(f"\nTable: {table}")
            for column, data_type in columns.items():
                print(f"  {column}: {data_type}")
        
    finally:
        cursor.close()
        connection.close()
    
    return schema

'''



def get_model_inputs(land_id):
   # get_db_schema()  # Output schema for debugging
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    try:
        # Check if the land table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE  table_schema = 'public'
                AND    table_name   = 'Land'
            );
        """)
        table_exists = cursor.fetchone()['exists']
        
        if not table_exists:
            raise ValueError("The 'Land' table does not exist in the database")
    
    except Exception as e:
        # Handle any exception that occurs
        print(f"An error occurred while checking table existence: {e}")
    
    try:
        # Check if the land_id exists in the database
        cursor.execute('SELECT * FROM "Land" WHERE land_id = %s', (land_id,))
        land_exists = cursor.fetchone()

        if not land_exists:
            raise ValueError("Land ID does not exist in the database")

    except Exception as e:
        # Handle any exception that occurs
        print(f"An error occurred while checking land_id: {e}")

    try:
        # Fetch land data
        print(f"Fetching land data for land_id: {land_id}")
        cursor.execute('SELECT * FROM "Land" WHERE land_id = %s', (land_id,))
        land_data = cursor.fetchone()
       # print(f"Fetched land data: {land_data}")

    except Exception as e:
        print(f"An error occurred while fetching land data: {e}")
        land_data = None  # In case of error, ensure the value is None

    try:
        # Fetch weather data
        print(f"Fetching weather data for land_id: {land_id}")
        cursor.execute('SELECT * FROM "Weather" WHERE land_id = %s', (land_id,))
        weather_data = cursor.fetchone()
       # print(f"Fetched weather data: {weather_data}")

    except Exception as e:
        print(f"An error occurred while fetching weather data: {e}")
        weather_data = None

    try:
        # Fetch financial data
        print(f"Fetching financial data for land_id: {land_id}")
        cursor.execute('SELECT * FROM "Finance" WHERE land_id = %s', (land_id,))
        financial_data = cursor.fetchone()
       # print(f"Fetched financial data: {financial_data}")

    except Exception as e:
        print(f"An error occurred while fetching financial data: {e}")
        financial_data = None

    # Check if all required data was fetched successfully
    if not all([land_data, weather_data, financial_data]):
        raise ValueError("Missing required data for the given land_id")

    try:
        # Prepare the model inputs
        print("Preparing model inputs...")
        model_inputs = [
            land_data['ph_level'], weather_data['temperature'], weather_data['rainfall'], 
            weather_data['humidity'], land_data['nitrogen'], land_data['phosphorus'], 
            land_data['potassium'], land_data['oxygen_level'], 
            financial_data['investment_amount'], land_data['land_size']
        ]
        print(f"Model inputs prepared: {model_inputs}")

        return model_inputs

    except KeyError as e:
        # Handle any missing data keys
        print(f"An error occurred while preparing model inputs: Missing key {e}")
        raise

    finally:
        cursor.close()
        connection.close()



def process_business_plan_and_save(businessPlan, cropData, land_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Delete existing records for the given land_id
        cursor.execute('DELETE FROM "BusinessPlan" WHERE land_id = %s', (land_id,))
        cursor.execute('DELETE FROM "LandStatistic" WHERE land_id = %s', (land_id,))
        cursor.execute('DELETE FROM "CropMaintenance" WHERE land_id = %s', (land_id,))

       

        # Generate a new UUID for the business_plan_id
        business_plan_id = str(uuid.uuid4())

        # Insert into BusinessPlan table
        cursor.execute("""
        INSERT INTO "BusinessPlan" (business_plan_id, executive_summary, resources, crops, weather_considerations, 
                                soil_maintenance, profit_estimations, other_recommendations, land_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (business_plan_id, businessPlan['Executive Summary'], businessPlan['Resources'], businessPlan['Crops'], 
             businessPlan['Weather Considerations'], businessPlan['Soil/Crop Maintenance'], 
             businessPlan['Profit Estimations'], businessPlan['Other Recommendations'], land_id))

        # Generate a new UUID for the land_statistic_id
        land_stat_id = str(uuid.uuid4())

        # Insert into LandStatistc table
        cursor.execute("""
        INSERT INTO "LandStatistic" (land_stat_id, land_use, human_coverage, water_availability, 
                                distribution_optimality, total_profit, land_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (land_stat_id, businessPlan['Key Variables Impacting the Plan']['Land Use'], 
             businessPlan['Key Variables Impacting the Plan']['Human Coverage'], 
             businessPlan['Key Variables Impacting the Plan']['Water Availability'], 
             businessPlan['Key Variables Impacting the Plan']['Distribution Optimality'], 
             cropData.get('total_profit'), land_id))

     

        # Generate a new UUID for the maintenance_id
        maintenance_id = str(uuid.uuid4())

        # Insert into CropMaintenance table
        cursor.execute("""
            INSERT INTO "CropMaintenance" (maintenance_id, pesticide_level, water_sufficienty, land_id) 
            VALUES (%s, %s, %s, %s)
            """, (maintenance_id, businessPlan['Key Variables Impacting the Plan']['Pesticides Levels'], 
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
        cursor.execute('DELETE FROM "Crop" WHERE land_id = %s', (land_id,))

        optimal_allocation = cropData.get("optimal_allocation", [])
        total_expected_return_in_money = clean_value(cropData.get("total_expected_return_in_money"))

        for crop in optimal_allocation:
            # Generate a new UUID for the crop_id
            crop_id = str(uuid.uuid4())

            # Insert into Crop table
            cursor.execute("""
                INSERT INTO "Crop" (crop_id, crop_name, crop_area, expected_weight_return, 
                                 expected_money_return, crop_investment, land_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (crop_id, crop.get("crop"), clean_value(crop.get("area")), 
                clean_value(crop.get("expected_return_in_weight")), 
                clean_value(crop.get("expected_return_in_money")), 
                clean_value(crop.get("cost")), land_id))

        cursor.execute("""
            UPDATE "Finance"
            SET expected_revenue = %s 
            WHERE land_id = %s
        """, (total_expected_return_in_money, land_id))

        connection.commit()

    finally:
        cursor.close()
        connection.close()