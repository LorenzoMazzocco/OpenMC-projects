# Moderator to fuel ratio effect on k-inf 

The main goal of this project is to investigate the dependency of k-inf for an EPR assembly lattice on the ratio of moderator on fuel material in volume.\
\
The model is an EPR assebly infinite lattice with a parametrized fuel pellet outer radius. The cladding geometry is set up to follow the expansion of the fuel pellet.
The pitch is set and fixed at 1.26 cm. n different fuel pellet radiuses are tested and the corresponding k-inf is computed. The errorbars are not present in the [resulting 
plot](results.png) because the standard deviations of the k-inf distributions are negligible for all the configurations considered.\
\
The [EPR lattice model](./model_xml) is created via a [template class](./templates/EPR_assembly.py) and modified during the execution of the [main script](main.py).
The k-inf are saved one by one with the corrisponding std devs during the execution of the script on an [csv file](./output/data.csv). The main script can be run in 
simulation mode (using -r argument in CLI) or bypassing the simulation and executing only the post processing file (no arguments passed in CLI).


## RESULTS
The resulting dependency is pictured in a simple plot ([results.png](.results.png)):

<img src='https://user-images.githubusercontent.com/36040421/135904923-3c9e58ed-c974-44d2-ba30-1d19b2053019.png' width='800'/>

We can verify that the simulation results match the literature:

<a href="https://www.nuclear-power.com/nuclear-power/reactor-physics/reactor-dynamics/moderator-to-fuel-ratio/">
<img src='https://user-images.githubusercontent.com/36040421/135906300-104811c7-34a5-491c-a480-d25e358a9839.png' width='800' />
<a/>
  
>Image linked to source (www.nuclear-power.com)
  
>Milan (IT), october 2021
  
 
