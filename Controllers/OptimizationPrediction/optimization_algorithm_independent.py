import numpy as np
from itertools import accumulate

# Constants
cost_per_m2 = [10] * 20  # Example costs for 20 crops
revenue_per_m2 = [20] * 20  # Example revenues for 20 crops
total_budget = 1000
total_area = 500

population_size = 100
num_generations = 100
mutation_rate = 0.1

def fitness_function(individual, CropData):
    total_cost = 0
    total_revenue = 0
    total_area_used = 0
    
    for i, crop in enumerate(CropData):
        area_for_crop = individual[i]
        total_cost += area_for_crop * cost_per_m2[i]
        total_revenue += area_for_crop * revenue_per_m2[i]
        total_area_used += area_for_crop
    
    if total_cost > total_budget or total_area_used > total_area:
        return 0
    else:
        return total_revenue - total_cost

def initialize_population(CropData):
    population = []
    for _ in range(population_size):
        individual = np.random.randint(0, total_area + 1, size=len(CropData))
        individual.sort()
        population.append(individual)
    return population

def select_parents(population, CropData):
    population_array = np.array(population)
    fitness_scores = [fitness_function(individual, CropData) for individual in population]
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:
        return population_array[np.random.choice(len(population), size=2)]
    probabilities = [score / total_fitness for score in fitness_scores]
    parents = population_array[np.random.choice(len(population), size=2, p=probabilities)]
    return parents

def crossover(parent1, parent2):
    child = []
    for i in range(len(parent1)):
        if i == 0:
            child.append(np.random.randint(0, min(parent1[i], parent2[i]) + 1))
        else:
            min_val = min(parent1[i], parent2[i])
            max_val = max(parent1[i], parent2[i])
            child.append(np.random.randint(min_val, max_val + 1))
    child.sort()
    return child

def mutate(individual):
    mutated_individual = individual.copy()
    for i in range(len(individual)):
        if np.random.rand() < mutation_rate:
            if i == 0:
                mutated_individual[i] = np.random.randint(0, mutated_individual[i] + 1)
            else:
                min_val = 0 if i == 0 else mutated_individual[i-1]
                max_val = total_area if i == len(individual) - 1 else mutated_individual[i+1]
                mutated_individual[i] = np.random.randint(min_val, max_val + 1)
    mutated_individual.sort()
    return mutated_individual

def run_genetic_algorithm(CropData):
    population = initialize_population(CropData)
    for _ in range(num_generations):
        new_population = []
        for _ in range(population_size // 2):
            parents = select_parents(population, CropData)
            child1 = crossover(parents[0], parents[1])
            child2 = crossover(parents[0], parents[1])
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))
        population = new_population
    
    best_individual = max(population, key=lambda ind: fitness_function(ind, CropData))
    return best_individual

def OptimizationMain(CropData):
    best_solution = run_genetic_algorithm(CropData)
    
    # Calculate the results
    allocation = {crop: best_solution[i] - (best_solution[i-1] if i > 0 else 0) for i, crop in enumerate(CropData)}
    total_cost = sum(best_solution[i] * cost_per_m2[i] for i in range(len(CropData)))
    total_revenue = sum(best_solution[i] * revenue_per_m2[i] for i in range(len(CropData)))
    total_profit = total_revenue - total_cost

    result = {
        "Optimal allocation": allocation,
        "Total cost": total_cost,
        "Total revenue": total_revenue,
        "Total profit": total_profit
    }

    return result