from .prisma_connection import prisma_connection
import re

async def get_model_inputs(land_id: str):
    await prisma_connection.connect()
    try:
        # Check if the land_id exists in the database
        land_exists = await prisma_connection.prisma.land.find_unique(
            where={"land_id": land_id},
        )

        if not land_exists:
            raise ValueError("Land ID does not exist in the database")

        # Fetch land data
        land_data = await prisma_connection.prisma.land.find_unique(
            where={"land_id": land_id},
        )

        # Fetch weather data
        weather_data = await prisma_connection.prisma.weather.find_first(
            where={"land_id": land_id},
        )

        # Fetch financial data
        financial_data = await prisma_connection.prisma.finance.find_first(
            where={"land_id": land_id},
        )

        # Check if all data is available
        if not all([land_data, weather_data, financial_data]):
            raise ValueError("Missing required data for the given land_id")

        # Prepare the model inputs
        model_inputs = [
            land_data.ph_level, weather_data.temperature, weather_data.rainfall, weather_data.humidity,
            land_data.nitrogen, land_data.phosphorus, land_data.potassium, land_data.oxygen_level, 
            financial_data.investment_amount, land_data.land_size
        ]

        return model_inputs

    finally:
        # Ensure the Prisma client is disconnected
        await prisma_connection.disconnect()


async def process_business_plan_and_save(businessPlan, cropData, land_id):
    # Extracting business plan elements
    (executive_summary, resources, crops, weather_considerations, 
     soil_maintenance, profit_estimations, other_recommendations) = (
        businessPlan[key] for key in [
            'Executive Summary', 'Resources', 'Crops', 
            'Weather Considerations', 'Soil/Crop Maintenance', 
            'Profit Estimations', 'Other Recommendations'
        ]
    )

    total_profit = cropData.get('total_profit')

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

    # Ensure the Prisma client is connected
    await prisma_connection.connect()

    try:
        # Delete existing records for the given land_id
        await prisma_connection.prisma.businessplan.delete_many(
            where={"land_id": land_id}
        )
        await prisma_connection.prisma.landstatistic.delete_many(
            where={"land_id": land_id}
        )
        await prisma_connection.prisma.cropmaintenance.delete_many(
            where={"land_id": land_id}
        )

        # Insert into Business_Plans table
        await prisma_connection.prisma.businessplan.create(
            data={
                "executive_summary": executive_summary,
                "resources": resources,
                "crops": crops,
                "weather_considerations": weather_considerations,
                "soil_maintenance": soil_maintenance,
                "profit_estimations": profit_estimations,
                "other_recommendations": other_recommendations,
                "land_id": land_id
            }
        )

        # Insert into Land_Statistics table
        await prisma_connection.prisma.landstatistic.create(
            data={
                "land_use": land_use,
                "human_coverage": human_coverage,
                "water_availability": water_availability,
                "distribution_optimality": distribution_optimality,
                "total_profit": total_profit,
                "land_id": land_id
            }
        )

        # Insert into Crop_Maintenance table
        await prisma_connection.prisma.cropmaintenance.create(
            data={
                "pesticide_level": pesticides_levels,
                "water_sufficienty": water_availability,
                "land_id": land_id
            }
        )

    finally:
        # Ensure the Prisma client is disconnected
        await prisma_connection.disconnect()


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
    # Ensure the Prisma client is connected
    await prisma_connection.connect()

    try:
        # Delete existing crop data for the given land_id
        await prisma_connection.prisma.crop.delete_many(
            where={"land_id": land_id}
        )

        # Extract data from cropData
        optimal_allocation = cropData.get("optimal_allocation", [])
        total_expected_return_in_money = clean_value(cropData.get("total_expected_return_in_money"))

        # Save each crop in the optimal_allocation list to the Crop table
        for crop in optimal_allocation:
            crop_name = crop.get("crop")
            crop_area = clean_value(crop.get("area"))
            expected_weight_return = clean_value(crop.get("expected_return_in_weight"))
            expected_money_return = clean_value(crop.get("expected_return_in_money"))
            crop_investment = clean_value(crop.get("cost"))

            # Insert crop data into Crop table
            await prisma_connection.prisma.crop.create(
                data={
                    "crop_name": crop_name,
                    "crop_area": crop_area,
                    "expected_weight_return": expected_weight_return,
                    "expected_money_return": expected_money_return,
                    "crop_investment": crop_investment,
                    "land_id": land_id
                }
            )

        # Update finance table with total_expected_return_in_money
        await prisma_connection.prisma.finance.update_many(
            where={"land_id": land_id},
            data={"expected_revenue": total_expected_return_in_money}
        )

    finally:
        # Ensure the Prisma client is disconnected
        await prisma_connection.disconnect()