# genepromulti



This repository 

## Adjustments to explore
1. Adding more node types:
    - $\sqrt{}$
    - $\log$
    - $\exp$
2. Coefficient optimization:
    - Adam
    - SGD
3. Mutation/Crossover:
    - subtree crossover
    - subtree mutation
    - crossover chance (currently $p=0.25$)
4. Symmetry:
    - left/right thrusters
5. Memory:
    - Record past states
    - potential for smoothing behaviour



## Plan of Attack

### 1: Test the hypotheses

Firstly, we will test out our hypotheses on different **selection, mutation and crossover** methods.  Using a standard experiment and plotting function, we will settle on the combination of the most promising methods.

### 2: Optimize the evolution Hyperparameters.

The evolution funciton hyperparameters can be seen as a discrete optimization problem. Two options to explore the solution space would be:
- 1: Grid search or random search
- 2: Evolutionary optimization (this would be a very cool inception thing to do)

### 3: Coefficient optimization

The final step will be optimizing the coefficients based of the best performing tree we have found using the previous two steps.



## Deliverables



| Task                                             | Team Member |
|--------------------------------------------------|-------------|
| Realizing a baseline solution                    |             |
| Bringing more elaborate ideas                    | David       |
| Experiment with fitness function                 | Caspar      |
| Experiment with subtree crossover                | Marijn      |
| Experiment with different function/terminal sets | Jurjen      |




