# /optimization_algorithm/fitness.py
import numpy as np

def fitness_function(population, crops, cost_per_m2, revenue_per_m2, total_area, total_budget):
    cost_per_m2 = np.array(cost_per_m2)
    revenue_per_m2 = np.array(revenue_per_m2)
    
    total_cost = np.sum(population * cost_per_m2, axis=1)
    total_revenue = np.sum(population * revenue_per_m2, axis=1)
    total_area_used = np.sum(population, axis=1)
    
    profit = total_revenue - total_cost
    
    area_penalty = np.maximum(0, total_area_used - total_area) * 1800
    budget_penalty = np.maximum(0, total_cost - total_budget) * 1000
    profit_penalty = np.maximum(0, -profit) * 2000
    
    fitness = profit - area_penalty - budget_penalty - profit_penalty
    
    return fitness

