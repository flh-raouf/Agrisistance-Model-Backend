# /optimization_algorithm/fitness.py
def fitness_function(individual, crops, cost_per_m2, revenue_per_m2, total_area, total_budget):
    total_cost = 0
    total_revenue = 0
    total_area_used = 0
    
    for i, crop in enumerate(crops):
        area_for_crop = individual[i]
        total_cost += area_for_crop * cost_per_m2[i]
        total_revenue += area_for_crop * revenue_per_m2[i]
        total_area_used += area_for_crop
    
    profit = total_revenue - total_cost
    
    area_penalty = max(0, total_area_used - total_area) * 1800
    budget_penalty = max(0, total_cost - total_budget) * 1000
    profit_penalty = max(0, -profit) * 2000
    
    fitness = profit - area_penalty - budget_penalty - profit_penalty
    
    return fitness

