import logging
import numpy as np
from .fitness import fitness_function
from .crossover_mutation import crossover, mutate
from .population import initialize_population, tournament_selection

def run_genetic_algorithm(crops, cost_per_m2, revenue_per_m2, total_area, total_budget, 
                          population_size, num_generations, mutation_rate, crossover_rate):
    population = initialize_population(population_size, len(crops), total_area)
    best_fitness = float('-inf')
    best_individual = None
    
    for generation in range(num_generations):
        fitness_values = fitness_function(population, crops, cost_per_m2, revenue_per_m2, total_area, total_budget)
        
        if np.max(fitness_values) > best_fitness:
            best_fitness = np.max(fitness_values)
            best_individual = population[np.argmax(fitness_values)]
        
        if best_fitness >= 0:
            logging.info(f"Positive profit achieved at generation {generation}. Stopping early.")
            break
        
        new_population = []
        for _ in range(population_size // 2):
            parent1 = tournament_selection(population, fitness_values)
            parent2 = tournament_selection(population, fitness_values)
            child1 = crossover(parent1, parent2, crossover_rate)
            child2 = crossover(parent2, parent1, crossover_rate)
            new_population.extend([mutate(child1, mutation_rate, total_area),
                                   mutate(child2, mutation_rate, total_area)])
        
        population = np.array(new_population)
        
        if generation % 50 == 0:
            logging.info(f"Generation {generation}: Best fitness = {best_fitness}")
    
    return best_individual