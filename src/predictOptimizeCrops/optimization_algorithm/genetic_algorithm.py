#comments+ er handling donneeeee
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
    
    # Validate population_size and num_generations
    if population_size <= 0 or num_generations <= 0:
        raise ValueError("Population size and number of generations must be positive integers.")
    
    # Initialize the population
    population = initialize_population(population_size, len(crops), total_area)
    best_fitness = float('-inf')
    best_individual = None
    
    # Start the evolutionary process
    for generation in range(num_generations):
        # Evaluate fitness for the current population
        fitness_values = fitness_function(population, crops, cost_per_m2, revenue_per_m2, total_area, total_budget)
        
        # Update the best fitness and corresponding individual if found
        if np.max(fitness_values) > best_fitness:
            best_fitness = np.max(fitness_values)
            best_individual = population[np.argmax(fitness_values)]
        
        # Early stopping if a positive profit is achieved
        if best_fitness >= 0:
            logging.info(f"Positive profit achieved at generation {generation}. Stopping early.")
            break
        
        # Create a new population using selection, crossover, and mutation
        new_population = []
        for _ in range(population_size // 2):
            parent1 = tournament_selection(population, fitness_values)
            parent2 = tournament_selection(population, fitness_values)
            child1 = crossover(parent1, parent2, crossover_rate)
            child2 = crossover(parent2, parent1, crossover_rate)
            new_population.extend([mutate(child1, mutation_rate, total_area),
                                   mutate(child2, mutation_rate, total_area)])
        
        # Replace the old population with the new one
        population = np.array(new_population)
        
        # Logging progress every 50 generations
        if generation % 50 == 0:
            logging.info(f"Generation {generation}: Best fitness = {best_fitness}")
    
    return best_individual
