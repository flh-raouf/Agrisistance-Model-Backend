#comm/er donee

import numpy as np

def initialize_population(population_size, num_crops, total_area):
    """
    Initialize the population with random crop distributions.
    
    Parameters:
    - population_size: Number of individuals in the population (int).
    - num_crops: Number of different crops (int).
    - total_area: Maximum area available for each crop (int).
    
    Returns:
    - A numpy array of shape (population_size, num_crops) where each element represents the area assigned to a crop for an individual.
    
    Raises:
    - ValueError: If population_size, num_crops, or total_area are non-positive.
    """
    # Validate input parameters
    if population_size <= 0 or num_crops <= 0 or total_area <= 0:
        raise ValueError("Population size, number of crops, and total area must be positive integers.")
    
    # Generate a population with random values within the specified range
    return np.random.randint(0, total_area + 1, size=(population_size, num_crops))

def tournament_selection(population, fitness_values, tournament_size=5):
    """
    Select an individual from the population using tournament selection.
    
    Parameters:
    - population: 2D numpy array where each row represents an individual solution.
    - fitness_values: 1D numpy array representing the fitness of each individual.
    - tournament_size: Number of individuals to compete in the tournament (int, default=5).
    
    Returns:
    - The individual (array) with the highest fitness from the tournament.
    
    Raises:
    - ValueError: If tournament_size is greater than the population size or less than 1.
    """
    # Validate tournament_size
    if tournament_size > len(population) or tournament_size < 1:
        raise ValueError("Tournament size must be between 1 and the population size.")
    
    # Randomly select indices for the tournament participants
    tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
    # Get the fitness values of the selected individuals
    tournament_fitness = fitness_values[tournament_indices]
    # Find the index of the individual with the highest fitness
    winner_index = tournament_indices[np.argmax(tournament_fitness)]
    
    # Return the individual with the highest fitness
    return population[winner_index]
