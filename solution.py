import gymnasium as gym

from genepro.node_impl import *
from genepro.evo import Evolution
from genepro.node_impl import Constant

import torch
import torch.optim as optim

import random
import os
import copy
from collections import namedtuple, deque

import matplotlib.pyplot as plt
from matplotlib import animation

env = gym.make("LunarLander-v2", render_mode="rgb_array")

Transition = namedtuple("Transition", ("state", "action", "next_state", "reward"))


class ReplayMemory(object):
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

    def __iadd__(self, other):
        self.memory += other.memory
        return self

    def __add__(self, other):
        self.memory = self.memory + other.memory
        return self
    
def fitness_function_pt(multitree, num_episodes=5, episode_duration=300, ignore_done=False, render=False):
    memory = ReplayMemory(10000)
    episode_rewards = []
    if render:
        frames = []

    # print(multitree.get_readable_repr())
    for _ in range(num_episodes):
        # get initial state of the environment
        observation = env.reset()
        observation = observation[0]
        rewards = []
        for _ in range(episode_duration):
            if render:
                frames.append(env.render())
            input_sample = torch.from_numpy(observation.reshape((1, -1))).float()
            action = torch.argmax(multitree.get_output_pt(input_sample)).detach()
            observation, reward, terminated, truncated, info = env.step(action.item())
            rewards.append(reward)
            output_sample = torch.from_numpy(observation.reshape((1, -1))).float()
            memory.push(input_sample, torch.tensor([[action.item()]]), output_sample, torch.tensor([reward]))
            if (terminated or truncated) and not ignore_done:
                break
        episode_rewards.append(np.sum(rewards))

    # Get the average reward over all episodes
    fitness = episode_rewards
    if render:
        return fitness, memory, frames
    return fitness, memory

def fitness_function(multitree, num_episodes=5, episode_duration=300, ignore_done=False, render=False):
    env = gym.make("LunarLander-v2", render_mode="rgb_array")


    episode_rewards = []
    if render:
        frames = []

    for _ in range(num_episodes):
        # get initial state of the environment
        observation = env.reset()
        observation = observation[0]
        rewards = []
        for _ in range(episode_duration):
            if render:
                frames.append(env.render())
            input_sample = observation.reshape((1, -1))
            action = np.argmax(multitree.get_output(input_sample))
            observation, reward, terminated, truncated, info = env.step(action.item())
            rewards.append(reward)
            if (terminated or truncated) and not ignore_done:
                break
        episode_rewards.append(np.sum(rewards))

    # Get the average reward over all episodes
    fitness = np.array(episode_rewards)
    if render:
        return fitness, [], frames
    return fitness, []

### USED TO STORE THE EXPERIMENT DICTIONARY
import inspect
import itertools
import pickle


def serialize_functions_in_dict(dictionary):
    for key, value in dictionary.items():
        if inspect.isfunction(value) or inspect.ismethod(value):
            dictionary[key] = value.__name__
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    value[i] = serialize_functions_in_dict(item)
                elif inspect.isfunction(item) or inspect.ismethod(item):
                    value[i] = item.__name__
                elif isinstance(item, Node):
                    value[i] = item.symb
        elif isinstance(value, dict):
            dictionary[key] = serialize_functions_in_dict(value)
    return dictionary

### USED TO CREATE THE EXPERIMENT DICTIONARY
def grid_search_params(params_dict):
    """
    Given a dictionary of hyperparameters, if a value is a list, loop over all values
    and create a grid search.
    """
    param_keys = params_dict.keys()
    param_values = params_dict.values()
    param_combinations = list(itertools.product(*[v if isinstance(v, list) else [v] for v in param_values]))
    for combination in param_combinations:
        yield dict(zip(param_keys, combination))

# Save the gen as a pickle file in the gens folder
def save_and_evaluate_evo_generations(evo, fitness_function, experiment_name, num_episodes=10, dir_name="experiments"):
    generation_evo_fitnesses = []
    generation_test_fitnesses = []
    for i, gen in enumerate(evo.best_of_gens):
        if i == 0:
            continue

        episode_rewards, _ = fitness_function(gen, num_episodes=num_episodes)
        evo_fitness_mean, evo_fitness_std = round(np.mean(gen.fitnesses), 3), round(np.std(gen.fitnesses), 3)
        test_fitness_mean, test_fitness_std  = round(np.mean(episode_rewards), 3), round(np.std(episode_rewards), 3)
        print(f"Best of Generation {i}: evo fitness:{evo_fitness_mean}+/-{evo_fitness_std} \t test_fitness:{test_fitness_mean}+/-{test_fitness_std}")
        
        generation_evo_fitnesses.append(gen.fitnesses)
        generation_test_fitnesses.append(episode_rewards)
        # create the gens folder if it doesn't exist
        os.makedirs(f"./{dir_name}/{experiment_name}/gen/", exist_ok=True) 
        with open(f"./{dir_name}/{experiment_name}/gen/gen_{i}_{evo_fitness_mean}_{test_fitness_mean}.pickle", "wb") as f:
            pickle.dump(gen, f)

    np.save(f"./{dir_name}/{experiment_name}/generation_evo_fitnesses.npy", generation_evo_fitnesses)
    np.save(f"./{dir_name}/{experiment_name}/generation_test_fitnesses.npy", generation_test_fitnesses)   
    return generation_evo_fitnesses, generation_test_fitnesses

def plot_evo_test_fitnesses(evo_fitnesses, test_fitnesses, experiment_name, dir_name="experiments"):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_title(f"Fitnesses: {experiment_name}")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.plot(np.arange(len(evo_fitnesses)), [np.mean(gen) for gen in evo_fitnesses], label="evo_fitness", color='tab:blue')
    ax.fill_between(np.arange(len(evo_fitnesses)), [np.mean(gen) - np.std(gen) for gen in evo_fitnesses], [np.mean(gen) + np.std(gen) for gen in evo_fitnesses], alpha=0.2, color='tab:blue')
    ax.plot(np.arange(len(test_fitnesses)), [np.mean(gen) for gen in test_fitnesses], label="test_fitness", color='tab:orange')
    ax.fill_between(np.arange(len(test_fitnesses)), [np.mean(gen) - np.std(gen) for gen in test_fitnesses], [np.mean(gen) + np.std(gen) for gen in test_fitnesses], alpha=0.2, color='tab:orange')
    ax.legend()
    plt.savefig(f"./{dir_name}/{experiment_name}/{experiment_name}.png")
    plt.close()

if __name__ == "__main__":

    from copy import deepcopy
    import json
    from genepro.selection import elitism_selection, tournament_selection, roulette_selection, rank_selection, boltzmann_selection, roulette_selection_elitism
    from genepro.variation import coeff_mutation, subtree_crossover, subtree_mutation

    experiment_name = "roulette_selection_elitism"

    dir_name = "selection_experiments"

    num_features = env.observation_space.shape[0]
    evo_settings = {
        "fitness_function": fitness_function,
        "internal_nodes": [[Plus(), Minus(), Times(), Div(), Sin(), Sqrt()]], #Cos(), Log(), Sqrt(), Square(), Max(), Min()
        "leaf_nodes": [[Feature(i) for i in range(num_features)] + [Constant()]],
        "n_trees": 4,
        "pop_size": 32,
        "max_gens": 50,
        "init_max_depth": 4,
        "max_tree_size": 45,
        "crossovers": [[{"fun": subtree_crossover, "rate": 0.5}]],
        "mutations": [[{"fun": subtree_mutation, "rate": 0.5}]],
        "coeff_opts": [[{"fun": coeff_mutation, "rate": 0.5}]],
        # "selection": {"fun": tournament_selection, "kwargs": {"tournament_size": 4}},
        # "selection": {"fun": roulette_selection},
        # "selection": {"fun": elitism_selection},
        # "selection": {"fun": rank_selection},
        "selection": {"fun": roulette_selection_elitism},
        "n_jobs": 8,
        "verbose": True
    }

    def hpo_evolve(evo_settings, experiment_name):
        hpo_settings = list(grid_search_params(evo_settings))
        for settings in hpo_settings:
            serialized_dict = serialize_functions_in_dict(deepcopy(settings))
            print(serialized_dict)
            
        for i, settings in enumerate(hpo_settings):
            specific_experiment_name = experiment_name + f"_pops{settings['pop_size']}_gens{settings['max_gens']}_mts{settings['max_tree_size']}_cor{settings['crossovers'][0]['rate']}_mutr{settings['mutations'][0]['rate']}_coeffr{settings['coeff_opts'][0]['rate']}"
            os.makedirs(f"./{dir_name}/{specific_experiment_name}", exist_ok=True)
            with open(f"./{dir_name}/{specific_experiment_name}/evo_settings.json", "w") as f:
                serialized_dict = serialize_functions_in_dict(deepcopy(settings))
                json.dump(serialized_dict, f)

            evo_baseline = Evolution(**settings)
            evo_baseline.evolve()

            with open(f"./{dir_name}/{specific_experiment_name}/evolution_class.pickle", "wb") as f:
                pickle.dump(evo_baseline, f)
            
            generation_evo_fitnesses, generation_test_fitnesses = save_and_evaluate_evo_generations(evo_baseline, fitness_function, specific_experiment_name, num_episodes=5, dir_name=dir_name)
            plot_evo_test_fitnesses(generation_evo_fitnesses, generation_test_fitnesses, specific_experiment_name, dir_name=dir_name)

    hpo_evolve(evo_settings, experiment_name)