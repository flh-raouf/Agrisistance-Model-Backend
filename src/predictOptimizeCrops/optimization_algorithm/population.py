import random
import numpy as np

def initialize_population(population_size, crops, total_area):
    population = []
    for _ in range(population_size):
        individual = np.random.randint(0, total_area + 1, size=len(crops))
        population.append(individual)
    return population

def tournament_selection(population, fitness_function, tournament_size=5):
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=fitness_function)
