import numpy as np
from copy import deepcopy

def tournament_selection(contestants : list, num_to_select : int, tournament_size : int=4) -> list:
  """
  Performs tournament selection on the contestants until the given number of selected contestants is reached;
  note that `len(contestants)` needs to be a multiple of `tournament_size` and similarly for `num_to_select`

  Parameters
  ----------
  contestants : list
    list of Node containing trees that undergo the selection
  num_survivors : int
    how many should be selected
  tournament_size : int, optional
    the size (window) of tournament selection (default is 4)

  Returns
  -------
  list
    list containing (copies of) the trees that were selected
  """
  selected = list()

  n = len(contestants)
  num_selected_per_parse = n // tournament_size
  num_parses = num_to_select // num_selected_per_parse

  # assert quantities are compatible
  assert n / tournament_size == num_selected_per_parse, "Number of contestants {} is not a multiple of tournament size {}".format(n,tournament_size)
  assert num_to_select / num_selected_per_parse == num_parses
 
  for _ in range(num_parses):
    # shuffle
    np.random.shuffle(contestants)
    fitnesses = np.array([t.fitness for t in contestants])

    winning_indices = np.argmax(fitnesses.reshape((-1, tournament_size)), axis=1)
    winning_indices += np.arange(0, n, tournament_size)

    selected += [deepcopy(contestants[i]) for i in winning_indices]

  return selected
 
 # ADDED SELECTION FUNCTIONS
def elitism_selection(contestants : list, num_to_select : int) -> list:
  """
  Performs elitism selection on the contestants until the given number of selected contestants is reached;
  """
  selected = list()

  sorted_contestants = sorted(contestants, key=lambda x: x.fitness, reverse=True)
  
  selected += [deepcopy(contestant) for contestant in sorted_contestants[:num_to_select//2]]
  selected += [deepcopy(contestant) for contestant in sorted_contestants[:num_to_select//2]]

  return selected
  

def rank_selection(contestants : list, num_to_select : int) -> list:
    """"
    Performs rank selection on the contestants until the given number of selected contestants is reached;

    """
    selected = list()
    ranked_contestants = sorted(contestants, key=lambda x: x.fitness)

    proportional_fitness = [i / len(ranked_contestants) for i in range(1, len(ranked_contestants) + 1)]

    proportional_fitness = []
    for i in range(1, len(ranked_contestants) + 1):
        if i == 1:
            proportional_fitness.append(i / len(ranked_contestants))
        else:
            if ranked_contestants[i-1].fitness == ranked_contestants[i-2].fitness:
                proportional_fitness.append((i-1) / len(ranked_contestants))
            else:
                proportional_fitness.append(i / len(ranked_contestants))


    total_fitness = np.sum([fitness for fitness in proportional_fitness])

    probabilities = [fitness / total_fitness for fitness in proportional_fitness]

    selection = np.random.choice(ranked_contestants, p=probabilities, size=num_to_select)
    
    selected += [deepcopy(contestant) for contestant in selection]

    return selected
  

def roulette_selection(contestants : list, num_to_select : int) -> list:
  """
  Performs roulette selection on the contestants until the given number of selected contestants is reached;
  """

  total_fitness = np.sum([contestant.fitness for contestant in contestants])

  probabilities = [contestant.fitness / total_fitness for contestant in contestants]

  return np.random.choice(contestants, p=probabilities, size=num_to_select)


def boltzmann_selection(contestants : list, num_to_select : int, temperature : float) -> list:
    """
    Performs Boltzmann selection on the contestants until the given number of selected contestants is reached,
    using the specified temperature.

    Args:
        contestants: A list of contestants.
        num_to_select: The number of contestants to select.
        temperature: The temperature parameter for Boltzmann selection.

    Returns:
        A list of selected contestants.
    """
    # temperature = .5

    fitness_values = [contestant.fitness for contestant in contestants]

    # Calculate the scaled fitness values using Boltzmann distribution
    scaled_fitness_values = [np.exp(fitness_value / temperature) for fitness_value in fitness_values]


    # Calculate the total scaled fitness
    total_scaled_fitness = np.sum(scaled_fitness_values)

    # Calculate the selection probabilities
    probabilities = scaled_fitness_values / total_scaled_fitness

    # Select contestants based on the probabilities
    selected_contestants = np.random.choice(contestants, size=num_to_select, p=probabilities)

    return selected_contestants


def stochastic_universal_sampling():
  pass