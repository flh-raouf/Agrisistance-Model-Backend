import random
import numpy as np

def crossover(parent1, parent2, crops, crossover_rate):
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(crops) - 1)
        child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
    else:
        child = parent1.copy()
    return child

def mutate(individual, mutation_rate, total_area):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, total_area)
    return individual
