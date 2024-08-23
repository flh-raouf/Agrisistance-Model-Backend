import logging
from .fitness import fitness_function
from .crossover_mutation import crossover, mutate
from .population import initialize_population, tournament_selection

def run_genetic_algorithm(crops, cost_per_m2, revenue_per_m2, total_area, total_budget, 
                          population_size, num_generations, mutation_rate, crossover_rate):
    population = initialize_population(population_size, crops, total_area)
    best_fitness = float('-inf')
    best_individual = None
    
    for generation in range(num_generations):
        new_population = []
        
        for _ in range(population_size):
            parent1 = tournament_selection(population, lambda ind: fitness_function(
                ind, crops, cost_per_m2, revenue_per_m2, total_area, total_budget))
            parent2 = tournament_selection(population, lambda ind: fitness_function(
                ind, crops, cost_per_m2, revenue_per_m2, total_area, total_budget))
            child = crossover(parent1, parent2, crops, crossover_rate)
            child = mutate(child, mutation_rate, total_area)
            new_population.append(child)
        
        population = new_population
        
        current_best = max(population, key=lambda ind: fitness_function(
            ind, crops, cost_per_m2, revenue_per_m2, total_area, total_budget))
        current_best_fitness = fitness_function(current_best, crops, cost_per_m2, revenue_per_m2, total_area, total_budget)
        
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_individual = current_best
        
        if generation % 50 == 0:
            logging.info(f"Generation {generation}: Best fitness = {best_fitness}")
    
    return best_individual
