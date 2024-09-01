# /optimization_algorithm/fitness.py commented + error handling doneeee
import numpy as np

def fitness_function(population, crops, cost_per_m2, revenue_per_m2, total_area, total_budget):
    """
    Calculate the fitness of each individual in the population based on cost, revenue, and constraints.
    
    Parameters:
    - population: 2D numpy array where each row represents an individual solution (crop distribution).
    - crops: List or array of crop names (not used in calculations, possibly for reference).
    - cost_per_m2: 1D numpy array representing the cost per square meter for each crop.
    - revenue_per_m2: 1D numpy array representing the revenue per square meter for each crop.
    - total_area: Total available area for planting (int).
    - total_budget: Total budget available for planting (int).
    
    Returns:
    - fitness: 1D numpy array where each element is the fitness value of the corresponding individual.
    
    Raises:
    - ValueError: If dimensions of input arrays don't match or if total_area or total_budget are negative.
    """
    
    # Validate that the population has the correct number of crop types
    if population.shape[1] != len(cost_per_m2) or population.shape[1] != len(revenue_per_m2):
        raise ValueError("Mismatch between number of crops and dimensions of cost/revenue arrays.")
    
    # Validate total_area and total_budget
    if total_area < 0 or total_budget < 0:
        raise ValueError("Total area and total budget must be non-negative.")
    
    # Convert costs and revenues to numpy arrays for vectorized operations
    cost_per_m2 = np.array(cost_per_m2)
    revenue_per_m2 = np.array(revenue_per_m2)
    
    # Calculate total cost and revenue for each individual in the population
    total_cost = np.sum(population * cost_per_m2, axis=1)
    total_revenue = np.sum(population * revenue_per_m2, axis=1)
    total_area_used = np.sum(population, axis=1)
    
    # Calculate profit for each individual
    profit = total_revenue - total_cost
    
    # Apply penalties for exceeding total area, budget, or having negative profit
    area_penalty = np.maximum(0, total_area_used - total_area) * 1800
    budget_penalty = np.maximum(0, total_cost - total_budget) * 1000
    profit_penalty = np.maximum(0, -profit) * 2000
    
    # Calculate final fitness by subtracting penalties from profit
    fitness = profit - area_penalty - budget_penalty - profit_penalty
    
    return fitness
