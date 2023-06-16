import json
import numpy as np
import matplotlib.pyplot as plt
import os

# parse args for experiment name
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--experiment_name', type=str, default="fitness_mean-len-std")


def find_experiment_files(root_dir, folder_prefix):
    evo_files = []
    test_files = []
    hyperparam_files = []
    for root, dirs, files in os.walk(root_dir):
        if os.path.basename(root).startswith(folder_prefix):
            for file in files:
                if file.endswith('.npy'):
                    file_path = os.path.join(root, file)
                    if 'evo' in file:
                        evo_files.append(file_path)
                    elif 'test' in file:
                        test_files.append(file_path)
                elif file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    hyperparam_files.append(file_path)
    return evo_files, test_files, hyperparam_files


def plot_generation_files(npy_files, ax, title_sufix, y_min=-150, y_max=300, independent=False, color='tab:blue'):
    total_data = [np.load(npy_file) for npy_file in npy_files]
    if independent:
        for i, npy_data in total_data:
            mean = np.mean(npy_data, axis=1)
            std = np.std(npy_data, axis=1)
            ax.plot(mean, label=f"Experiment {i}", linewidth=0.5)
            # ax.fill_between(np.arange(len(mean)), mean-std, mean+std, alpha=0.2)
    mean_total = np.mean(total_data, axis=(0, 2))
    std_total = np.std(total_data, axis=(0, 2))
    ax.set_ylim(y_min, y_max)
    ax.plot(mean_total, label=f"Mean Reward of Experiments During {title_sufix}", color=color, linewidth=2)
    ax.fill_between(np.arange(len(mean_total)), mean_total-std_total, mean_total+std_total, alpha=0.2, color=color)
    # ax.set_title(f'Reward during {title_sufix} of {len(npy_files)} experiments')
    ax.set_xlabel("Generation")
    ax.set_ylabel("Episodic Reward")
    ax.legend()



if __name__ == "__main__":
    """
        Make sure to set the experiment name to the folder prefix of the experiment you want to plot.
        Also make sure to update the fig.subtitle.
    """
    root_dir = "./experiments"
    output_dir = "./plots"
    # experiment_name = "baseline_exp"
    # experiment_name = "fitness_mean-len-sqrt_std"
    # experiment_name = "elitism_fitness_mean-len-sqrt_std"
    # experiment_name = "fitness_mean-len-std"
    # experiment_name = "fitness_mean-len-quarter_std"
    # experiment_name = "fitness_discounted_return"
    experiment_name = "fitness_discounted_return_len_sqrt_std"


    args = parser.parse_args()
    experiment_name = args.experiment_name

    evo_files, test_files, hperparam_files = find_experiment_files(root_dir, experiment_name)
    assert len(evo_files) == len(test_files), "Number of evolution files and test files must be the same"
    assert len(evo_files) > 0, "No evolution files found"

    hyper_settings = json.load(open(hperparam_files[0], 'r'))
    print(f"experiment settings: {hyper_settings}")
    print(f"Found {len(evo_files)} evolution files and {len(test_files)} test files")
    # for i, (evo_file, test_file) in enumerate(zip(evo_files, test_files)):
    #     print(f"Experiment {i}: {evo_file} - {test_file}")
 
    fig, ax = plt.subplots(figsize=(10, 5))
    plot_generation_files(evo_files, ax, 'Evolution', color='tab:red')
    plot_generation_files(test_files, ax, 'Test', color='tab:blue')
    # fig.suptitle(f"Best Gen Reward with {len(evo_files)} Experiments for Baseline")
    # fig.suptitle(f"Best Gen Reward with {len(evo_files)} Experiments for Fitness Function: mean(rewards) - len(pop) - sqrt(std(rewards))")
    # fig.suptitle(f"Best Gen Reward with {len(evo_files)} Experiments for Elitism with Fitness Function: mean(rewards) - len(pop) - sqrt(std(rewards))")
    # fig.suptitle(f"Best Gen Reward with {len(evo_files)} Experiments for Fitness Function: mean(rewards) - len(pop) - std(rewards)")
    # fig.suptitle(f"Best Gen Reward with {len(evo_files)} Experiments for Fitness Function: discounted return with decay rate 0.99")
    fig.suptitle(f"Best Gen Reward with {len(evo_files)} Experiments for Fitness Function: d_return - len(pop) - sqrt(std(d_return))")
    
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{experiment_name}.png"))
    plt.close()




