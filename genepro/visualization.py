import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_fitness(fitnesses: np.ndarray, save_path):
    """
    fitnesses: m x n np.array, m = num_experiments, n = num_generations
    """
    print(fitnesses)
    df = pd.DataFrame(fitnesses).melt()
    ax = sns.lineplot(data=df, x="variable", y="value")

    fig = ax.get_figure()
    fig.savefig(save_path)

    plt.clf()

if __name__ == "__main__":
    fitnesses_path = "plots/plot_data/plot_test.npy"
    save_path = "plots/viz/test_plot.png"
    fitnesses = np.load(fitnesses_path, allow_pickle=True)

    plot_fitness(fitnesses, save_path)


