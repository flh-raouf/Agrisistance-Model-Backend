import logging
import numpy as np
from .fitness import fitness_function
from .crossover_mutation import crossover, mutate
from .population import initialize_population, tournament_selection

def run_genetic_algorithm(crops, cost_per_m2, revenue_per_m2, total_area, total_budget, 
                          population_size, num_generations, mutation_rate, crossover_rate):
    """
    Run a genetic algorithm to optimize crop distribution for maximum profit.
    
    Parameters:
    - crops: List of crops (not used directly in the algorithm, but relevant for context).
    - cost_per_m2: 1D numpy array representing the cost per square meter for each crop.
    - revenue_per_m2: 1D numpy array representing the revenue per square meter for each crop.
    - total_area: Total available area for planting (int).
    - total_budget: Total budget available for planting (int).
    - population_size: Number of individuals in the population (int).
    - num_generations: Number of generations to run the algorithm (int).
    - mutation_rate: Probability of mutation for each gene (float between 0 and 1).
    - crossover_rate: Probability of crossover between parents (float between 0 and 1).
    
    Returns:
    - best_individual: The individual (array) with the highest fitness found.
    
    Raises:
    - ValueError: If population_size or num_generations are non-positive.
    """
    
    # Validate input parameters
    if population_size <= 0 or num_generations <= 0:
        raise ValueError("Population size and number of generations must be positive integers.")
    
    # Initialize the population
    population = initialize_population(population_size, len(crops), total_area)
    best_fitness = float('-inf')
    best_profit = float('-inf')
    best_individual = None
    
    # Start the evolutionary process
    for generation in range(num_generations):
        # Evaluate fitness for the current population
        fitness_values, profit_values = fitness_function(population, crops, cost_per_m2, revenue_per_m2, total_area, total_budget)
        
        # Update the best solution if a better one is found
        max_fitness_index = np.argmax(fitness_values)
        if fitness_values[max_fitness_index] > best_fitness:
            best_fitness = fitness_values[max_fitness_index]
            best_profit = profit_values[max_fitness_index]
            best_individual = population[max_fitness_index].copy()
        
        # Create a new population
        new_population = []
        elite_size = max(1, int(0.05 * population_size))  # Preserve top 5% of solutions
        elite_indices = np.argsort(fitness_values)[-elite_size:]
        new_population.extend(population[elite_indices])
        
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitness_values)
            parent2 = tournament_selection(population, fitness_values)
            
            # Perform crossover
            child = crossover(parent1, parent2, crossover_rate)
            
            # Perform mutation
            child = mutate(child, mutation_rate, total_area)
            
            new_population.append(child)
        
        # Convert the new population to a numpy array
        population = np.array(new_population)
        
        # Apply repair function to ensure all solutions meet constraints
        population = repair_solutions(population, total_area, total_budget, cost_per_m2)
        
        # Log progress every 50 generations
        if generation % 50 == 0:
            logging.info(f"Generation {generation}: Best fitness = {best_fitness:.2f}, Best profit = {best_profit:.2f}")
    
    # Ensure the best solution meets all constraints
    best_individual = repair_solutions(best_individual.reshape(1, -1), total_area, total_budget, cost_per_m2)[0]
    best_fitness, best_profit = fitness_function(best_individual.reshape(1, -1), crops, cost_per_m2, revenue_per_m2, total_area, total_budget)
    
    logging.info(f"Final solution: Profit = {best_profit[0]:.2f}, Fitness = {best_fitness[0]:.2f}")
    return best_individual

def repair_solutions(population, total_area, total_budget, cost_per_m2):
    """
    Repair solutions to ensure they meet constraints.
    """
    # Ensure total area is not exceeded
    area_sum = np.sum(population, axis=1, keepdims=True)
    population = np.where(area_sum > total_area, population * (total_area / area_sum), population)
    
    # Ensure budget is not exceeded
    total_cost = np.sum(population * cost_per_m2, axis=1, keepdims=True)
    population = np.where(total_cost > total_budget, population * (total_budget / total_cost), population)
    
    # Ensure at least 1 m² is used
    population = np.where(np.sum(population, axis=1, keepdims=True) < 1, population + 1, population)
    
    return population