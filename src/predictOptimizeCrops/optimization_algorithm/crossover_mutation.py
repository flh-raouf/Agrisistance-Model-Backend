#commented + error handling done (amel)
import random
import numpy as np

def crossover(parent1, parent2, crossover_rate):
    """
    Perform a crossover between two parent arrays to generate a child.
    
    Parameters:
    - parent1: The first parent array (numpy array).
    - parent2: The second parent array (numpy array).
    - crossover_rate: Probability of performing crossover (float between 0 and 1).

    Returns:
    - A new child array generated from the parents.
    
    Raises:
    - ValueError: If parents are not of the same length or if crossover_rate is out of bounds.
    """
    # Validate input lengths
    if len(parent1) != len(parent2):
        raise ValueError("Parent arrays must be of the same length.")
    
    # Validate crossover_rate
    if not (0 <= crossover_rate <= 1):
        raise ValueError("Crossover rate must be between 0 and 1.")
    
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(parent1) - 1)
        child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
    else:
        child = parent1.copy()
    
    return child

def mutate(individual, mutation_rate, total_area):
    """
    Mutate an individual's elements based on a given mutation rate.
    
    Parameters:
    - individual: The array representing the individual to mutate (numpy array).
    - mutation_rate: Probability of each element being mutated (float between 0 and 1).
    - total_area: Maximum value that an element can take (int).

    Returns:
    - The mutated individual array.
    
    Raises:
    - ValueError: If mutation_rate is out of bounds or if total_area is negative.
    """
    # Validate mutation_rate
    if not (0 <= mutation_rate <= 1):
        raise ValueError("Mutation rate must be between 0 and 1.")
    
    # Validate total_area
    if total_area < 0:
        raise ValueError("Total area must be non-negative.")
    
    mask = np.random.random(len(individual)) < mutation_rate
    individual[mask] = np.random.randint(0, total_area + 1, size=mask.sum())
    
    return individual
