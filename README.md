# genepromulti

## Thruster Symmetry

The idea for this branch stems from the symmetry in the lunar landers side thrusters.
The multitree genetic program will output a chance for each action based on observations from the environment.
Consider a situation in which the lander is spinning violently counter-clockwise: in this case the chance of fireing the left thruster should be very high while that of fireing the right thruster should be very low.

The current implementation of the multitree genetic program does not take symmetry into account.
If there was a way to make the trees corresponding with the respective chance of fireing the left and right thruster symmetric, we would have one less tree per individual (3 vs 4), theoretically resulting in a 25% reduction in computing resources needed to run evolution.

An important thing to note is that not all of the features in the observation space contribute to the symmetry.
The observation space of the lunar lander is a vector of the following features:

| feature           | symmery? |
|-------------------|----------|
| x position        | yes      |
| y position        | no       |
| x velocity        | yes      |
| y velocity        | no       |
| angle             | yes      |
| angular velocity  | yes      |
| left leg contact  | ?        |
| right leg contact | ?        |

I am not sure if the contribution of the leg contact features to the symmetry should be considered.


### Plan of implementation

I plan to create a function that will create a symmetric tree from a given tree.
In this context, symmetry is not defined in terms of the tree structure, but as the multiplication of the symmetrical features with -1.
Concretely, the function will take a tree and a list of features that should be symmetrical.
It will then create a copy of this tree, but swap each of the features (F) in the list with a subtree of the form:

     x
     
    / \
    
   -1  F
   
### Modifying the multitree

To get this to work, we will have to create a multitree of three trees instead of four.
The creating of the symmetrical tree will be done at the moment an action is chosen.





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




