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
    
    # Input validation
    if population.shape[1] != len(cost_per_m2) or population.shape[1] != len(revenue_per_m2):
        raise ValueError("Mismatch between number of crops and dimensions of cost/revenue arrays.")
    
    if total_area <= 0 or total_budget <= 0:
        raise ValueError("Total area and total budget must be positive.")
    
    # Convert costs and revenues to numpy arrays
    cost_per_m2 = np.array(cost_per_m2)
    revenue_per_m2 = np.array(revenue_per_m2)
    
    # Calculate total cost, revenue, and area used for each individual
    total_cost = np.sum(population * cost_per_m2, axis=1)
    total_revenue = np.sum(population * revenue_per_m2, axis=1)
    total_area_used = np.sum(population, axis=1)
    
    # Calculate profit
    profit = total_revenue - total_cost
    
    # Apply penalties for constraint violations
    area_penalty = np.maximum(0, total_area_used - total_area) * 1000
    budget_penalty = np.maximum(0, total_cost - total_budget) * 1000
    min_area_penalty = np.maximum(0, 1 - total_area_used) * 1000  # Penalty for using less than 1 m²
    
    # Calculate fitness
    fitness = profit - area_penalty - budget_penalty - min_area_penalty
    
    # Set fitness to a large negative number for solutions violating constraints
    fitness[total_area_used > total_area] = -1e6
    fitness[total_cost > total_budget] = -1e6
    fitness[profit <= 0] = -1e6
    fitness[total_area_used < 1] = -1e6  # Ensure at least 1 m² is used
    
    return fitness, profit