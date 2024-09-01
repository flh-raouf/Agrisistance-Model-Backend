import numpy as np

def initialize_population(population_size, num_crops, total_area):
    return np.random.randint(0, total_area + 1, size=(population_size, num_crops))

def tournament_selection(population, fitness_values, tournament_size=5):
    tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
    tournament_fitness = fitness_values[tournament_indices]
    winner_index = tournament_indices[np.argmax(tournament_fitness)]
    return population[winner_index]