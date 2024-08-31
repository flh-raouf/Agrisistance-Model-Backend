import json

def display_optimal_allocation(crops, best_solution, cost_per_m2, weight_area, revenue_per_m2, total_area, total_budget):
    total_cost = 0
    total_expected_weight_return = 0
    total_expected_money_return = 0
    total_area_used = 0

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

    for i, crop in enumerate(crops):
        area_for_crop = int(best_solution[i])  # Convert to int
        cost_for_crop = float(area_for_crop * cost_per_m2[i])  # Convert to float
        expected_weight_return = float(area_for_crop * weight_area[i])
        expected_money_return = float(area_for_crop * revenue_per_m2[i])
        
        total_cost += cost_for_crop
        total_expected_weight_return += expected_weight_return
        total_expected_money_return += expected_money_return
        total_area_used += area_for_crop
        
        if area_for_crop > 0:
            crop_result = {
                "crop": crop,
                "area": area_for_crop,
                "expected_return_in_weight": f"{expected_weight_return:.2f} units",
                "expected_return_in_money": f"${expected_money_return:.2f}",
                "cost": f"${cost_for_crop:.2f}"
            }
            results["optimal_allocation"].append(crop_result)

    total_profit = total_expected_money_return - total_cost

    results["total_area_used"] = total_area_used
    results["unused_area"] = total_area - total_area_used
    results["total_expected_return_in_money"] = f"${total_expected_money_return:.2f}"
    results["total_expected_return_in_weight"] = f"{total_expected_weight_return:.2f} units"
    results["total_cost"] = f"${total_cost:.2f}"
    results["total_profit"] = total_profit
    results["budget_utilization"] = f"{(total_cost / total_budget) * 100:.2f}%"

    # Convert the results dictionary to a JSON string and store it in a variable
    json_results = json.dumps(results, indent=4)

    # Return the JSON results
    return json_results