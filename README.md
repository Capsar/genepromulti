### <div align='center'> Evolutionary Algorithms - CS4205 <br/> 16-01-2023 </div>

# <div align='center'> genepromulti </div>
#### <div align='center'><i>Forked project about evolving the Lunar Lander with EAs and Gradient-Based Optimisation </i></div>
## Thruster Symmetry

### <div align ='center'> Group 011:</div>
#### <div align='center'>Ben Jacobs: 4713761 </br> Caspar Meijer: 4719298 </br> David Janssen: 4731268 </br> Marijn de Rijk: 4888871 </br> Jurjen Scharringa: 4708652  </div>
The idea for this branch stems from the symmetry in the lunar landers side thrusters.
The multitree genetic program will output a chance for each action based on observations from the environment.
Consider a situation in which the lander is spinning violently counter-clockwise: in this case the chance of fireing the left thruster should be very high while that of fireing the right thruster should be very low.

This project is made for the group assignment of the course EA4205 at the TU Delft. 
The aim of this project is to evolve the Lunar Lander problem using Evolutionary Algorithms and Gradient Based Optimisation. First a baseline is constructed, then multiple hypotheses are drawn up to improve the performance of this baseline. This project is forked from the original [genepromulti](https://github.com/matigekunstintelligentie/genepromulti) project. 
The current implementation of the multitree genetic program does not take symmetry into account.
If there was a way to make the trees corresponding with the respective chance of fireing the left and right thruster symmetric, we would have one less tree per individual (3 vs 4), theoretically resulting in a 25% reduction in computing resources needed to run evolution.

An important thing to note is that not all of the features in the observation space contribute to the symmetry.
The observation space of the lunar lander is a vector of the following features. of which a subset will be inverted to create symmetry between the left and right thrusters.

| feature           | symmery? |
|-------------------|----------|
| x position        | yes      |
| y position        | no       |
| x velocity        | yes      |
| y velocity        | no       |
| angle             | yes      |
| angular velocity  | yes      |
| left leg contact  | yes      |
| right leg contact | yes      |


This repository 

This file will contain the following contents:
- Content description
- Installation guide

## Content description
The repository consists of the following files with corresponding descriptions:
- ```solution.ipynb```: The main solution notebook. Changes were added between #BEGIN OWN CHANGES and #END OWN CHANGES.
- ```genepro/evo.py```: Evolution file responsible for the evolution. No changes were made here.
- ```genepro/multitree.py```: Multitree file responsible for constructing the multitree. No changes were made here.
- ```node_impl.py```: Node implementations file. No changes were made here.
- ```node.py```: Node file. No changes were made here. 
- ```scikit.py```: Scikit file. No changes were made here.
- ```selection.py```: Selection file for selection method. Changes were added between #BEGIN OWN CHANGES and #END OWN CHANGES.
- ```util.py```: Utilisation file. No changes were made here.
- ```variation.py```: Variation file. Changes were added between #BEGIN OWN CHANGES and #END OWN CHANGES.
- ```visualization.py```: Visualization file for plotting the results. This file was created by us.
- `thruster_symmetry.py`: File containing function for swapping out selected feature nodes to achieve symmetry (as explained above)

 
## Installation guide
The following pre-requisites are required:
- Python >3.6, <3.10
- git

Then, the repository needs to be downloaded into a directory of choice:
```
git clone https://github.com/Capsar/genepromulti.git
```
Install the required dependencies by following these steps:

> **_NOTE:_**  Conda does not show a progress bar.  The size of the needed packages is quite large, meaning you may have to wait a while for all the packages to load.


- navigate to the folder in which you installed the repository: ``cd PATH/TO/REPOSITORY``
- Create new conda environment: 
     - Windows: ```conda env create --name EA_group11 -f requirements.txt```
     - Linux: `conda env create -f requirements_linux.txt`
- Activate the new conda environment ```conda activate EA_group11```
