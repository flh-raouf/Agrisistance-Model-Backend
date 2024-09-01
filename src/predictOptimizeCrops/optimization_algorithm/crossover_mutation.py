import random
import numpy as np

def crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(parent1) - 1)
        child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
    else:
        child = parent1.copy()
    return child

def mutate(individual, mutation_rate, total_area):
    mask = np.random.random(len(individual)) < mutation_rate
    individual[mask] = np.random.randint(0, total_area + 1, size=mask.sum())
    return individual