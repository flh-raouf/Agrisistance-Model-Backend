from DB.connect import connect
import aiomysql
import uuid
import re

async def get_model_inputs(land_id: str):
    conn = await connect()
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            # Fetch land data
            await cursor.execute(
                'SELECT land_size, ph_level, phosphorus, potassium, oxygen_level, nitrogen FROM Land_Data WHERE land_id = %s',
                (land_id)
            )
            land_data = await cursor.fetchone()

            # Fetch weather data
            await cursor.execute(
                'SELECT temperature, humidity, rainfall FROM Weather_Data WHERE land_id = %s',
                (land_id,)
            )
            weather_data = await cursor.fetchone()

            # Fetch financial data
            await cursor.execute(
                'SELECT investment_amount FROM Financial_Data WHERE land_id = %s',
                (land_id,)
            )
            financial_data = await cursor.fetchone()

            # Prepare the model inputs
            model_inputs = [
                land_data['ph_level'], weather_data['temperature'], weather_data['rainfall'], weather_data['humidity'],
                land_data['nitrogen'], land_data['phosphorus'], land_data['potassium'], land_data['oxygen_level'], 
                financial_data['investment_amount'], land_data['land_size']
            ]

        return model_inputs
    finally:
        conn.close()


async def process_business_plan_and_save(businessPlan, land_id):
    # Generate UUIDs
    businessPlanId = str(uuid.uuid4())
    land_statistics_id = str(uuid.uuid4())
    maintenance_id = str(uuid.uuid4())

    # Extracting business plan elements
    (executive_summary, resources, crops, weather_considerations, 
     soil_maintenance, profit_estimations, other_recommendations) = (
        businessPlan[key] for key in [
            'Executive Summary', 'Resources', 'Crops', 
            'Weather Considerations', 'Soil/Crop Maintenance', 
            'Profit Estimations', 'Other Recommendations'
        ]
    )

    # Extracting key variables impacting the plan and handling 'N/A' values
    def handle_na(value):
        return 0 if value == 'N/A' else value

    (human_coverage, water_availability, land_use, 
     distribution_optimality, pesticides_levels) = (
        handle_na(businessPlan['Key Variables Impacting the Plan'].get(key)) for key in [
            'Human Coverage', 'Water Availability', 
            'Land Use', 'Distribution Optimality', 
            'Pesticides Levels'
        ]
    )

    # Reconnect and save data to the database
    conn = await connect()
    try:
        async with conn.cursor() as cursor:
            # Check if there are existing records for the given land_id and delete them
            await cursor.execute("DELETE FROM Business_Plans WHERE land_id = %s", (land_id,))
            await cursor.execute("DELETE FROM Land_Statistics WHERE land_id = %s", (land_id,))
            await cursor.execute("DELETE FROM Crop_Maintenance WHERE land_id = %s", (land_id,))

            # Insert into Business_Plans table
            sql_bp = "INSERT INTO Business_Plans VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            await cursor.execute(sql_bp, (
                businessPlanId, executive_summary, resources, crops, 
                weather_considerations, soil_maintenance, 
                profit_estimations, other_recommendations, land_id
            ))

            # Insert into Land_Statistics table
            sql_ls = "INSERT INTO Land_Statistics VALUES (%s, %s, %s, %s, %s, %s)"
            await cursor.execute(sql_ls, (
                land_statistics_id, land_use, human_coverage, 
                water_availability, distribution_optimality, land_id
            ))

            # Insert into Crop_Maintenance table
            sql_cm = "INSERT INTO Crop_Maintenance VALUES (%s, %s, %s, %s)"
            await cursor.execute(sql_cm, (
                maintenance_id, pesticides_levels, water_availability, land_id
            ))

            # Commit the transaction
            await conn.commit()

    finally:
        conn.close()


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
    


async def process_crops_and_save(cropData, land_id):
    # Connect to the database
    conn = await connect()
    try:
        async with conn.cursor() as cursor:

            await cursor.execute("DELETE FROM Crop_Data WHERE land_id = %s", (land_id,))

            # Extract data from cropData
            optimal_allocation = cropData.get("optimal_allocation", [])
            total_expected_return_in_money = cropData.get("total_expected_return_in_money")

            # Clean the total_expected_return_in_money value
            total_expected_return_in_money = clean_value(total_expected_return_in_money)

            # Save each crop in the optimal_allocation list to the Crops table
            for crop in optimal_allocation:
                crop_id = str(uuid.uuid4())  # Generate UUID for each crop
                crop_name = crop.get("crop")
                area = crop.get("area")
                expected_return_in_weight = crop.get("expected_return_in_weight")
                expected_return_in_money = crop.get("expected_return_in_money")
                cost = crop.get("cost")

                # Clean the values
                area = clean_value(area)
                expected_return_in_weight = clean_value(expected_return_in_weight)
                expected_return_in_money = clean_value(expected_return_in_money)
                cost = clean_value(cost)

                # Insert crop data into Crops table
                sql_crops = "INSERT INTO Crop_Data VALUES (%s, %s, %s, %s, %s, %s, %s)"
                await cursor.execute(sql_crops, (
                    crop_id, crop_name, area, cost, expected_return_in_money, expected_return_in_weight, land_id
                ))

            # Update financial_data table with total_expected_return_in_money
            sql_update_financial = """
                UPDATE Financial_Data
                SET expected_revenue = %s
                WHERE land_id = %s
            """
            await cursor.execute(sql_update_financial, (total_expected_return_in_money, land_id))

            # Commit the transaction
            await conn.commit()

    finally:
        conn.close()