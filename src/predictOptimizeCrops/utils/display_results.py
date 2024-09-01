#CER donee
import json

def display_optimal_allocation(crops, best_solution, cost_per_m2, weight_area, revenue_per_m2, total_area, total_budget):
    """
    Display the optimal allocation of crops, including costs, expected returns, and profit.

    Parameters:
    - crops: List of crop names.
    - best_solution: Array representing the optimal area allocation for each crop.
    - cost_per_m2: Array representing the cost per square meter for each crop.
    - weight_area: Array representing the expected weight return per square meter for each crop.
    - revenue_per_m2: Array representing the expected revenue per square meter for each crop.
    - total_area: Total available area for planting (int).
    - total_budget: Total budget available for planting (int).

    Returns:
    - A JSON string containing the optimal allocation details, including total cost, returns, and profit.
    
    Raises:
    - ValueError: If lengths of input arrays do not match, or if total_area or total_budget are non-positive.
    """
    
    # Validate the lengths of the input arrays
    if not (len(crops) == len(best_solution) == len(cost_per_m2) == len(weight_area) == len(revenue_per_m2)):
        raise ValueError("Input arrays must all have the same length.")
    
    # Validate total_area and total_budget
    if total_area <= 0 or total_budget <= 0:
        raise ValueError("Total area and total budget must be positive.")
    
    # Initialize cumulative totals
    total_cost = 0
    total_expected_weight_return = 0
    total_expected_money_return = 0
    total_area_used = 0

    # Initialize results dictionary
    results = {
        "optimal_allocation": [],
        "total_area_used": 0,
        "unused_area": 0,
        "total_expected_return_in_money": 0,
        "total_expected_return_in_weight": 0,
        "total_cost": 0,
        "total_profit": 0,
        "budget_utilization": 0
    }

    # Calculate costs and returns for each crop
    for i, crop in enumerate(crops):
        area_for_crop = int(best_solution[i])  # Convert to int
        cost_for_crop = float(area_for_crop * cost_per_m2[i])  # Convert to float
        expected_weight_return = float(area_for_crop * weight_area[i])
        expected_money_return = float(area_for_crop * revenue_per_m2[i])
        
        # Accumulate totals
        total_cost += cost_for_crop
        total_expected_weight_return += expected_weight_return
        total_expected_money_return += expected_money_return
        total_area_used += area_for_crop
        
        # Add crop allocation details to results if area is allocated
        if area_for_crop > 0:
            crop_result = {
                "crop": crop,
                "area": area_for_crop,
                "expected_return_in_weight": f"{expected_weight_return:.2f} units",
                "expected_return_in_money": f"${expected_money_return:.2f}",
                "cost": f"${cost_for_crop:.2f}"
            }
            results["optimal_allocation"].append(crop_result)

    # Calculate total profit
    total_profit = total_expected_money_return - total_cost

    # Update results dictionary with final totals
    results["total_area_used"] = total_area_used
    results["unused_area"] = total_area - total_area_used
    results["total_expected_return_in_money"] = f"${total_expected_money_return:.2f}"
    results["total_expected_return_in_weight"] = f"{total_expected_weight_return:.2f} units"
    results["total_cost"] = f"${total_cost:.2f}"
    results["total_profit"] = total_profit
    results["budget_utilization"] = f"{(total_cost / total_budget) * 100:.2f}%"

    # Convert the results dictionary to a JSON string with indentation for readability
    json_results = json.dumps(results, indent=4)

    # Return the JSON string
    return json_results
