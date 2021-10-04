# Moderator to fuel ratio effect on k-inf 

The main goal of this project is to investigate the dependency of k-inf for an [EPR assembly lattice](https://github.com/LorenzoMazzocco/OpenMC-projects/files/7280552/EPR.core.design.pdf) on the ratio of moderator over fuel material in volume.\
\
The model is an EPR assembly infinite lattice with a parametrized fuel pellet outer radius. The cladding geometry is set up to follow the expansion of the fuel pellet.
The lattice pitch is set and fixed at 1.26 cm. n different fuel pellet radiuses are tested and the corresponding k-inf is computed. The errorbars are not present in the [resulting 
plot](results.png) because the standard deviations of the k-inf distributions are negligible for all the configurations considered.
<br/><br/>

<p float="left">
  <img src="https://user-images.githubusercontent.com/36040421/135911129-22e743e3-ade0-4c85-8db9-90d240600ba1.png" width="300" />
  <img src="https://user-images.githubusercontent.com/36040421/135911138-0be1dc88-08e6-4db0-ba38-48b6246cdf33.png" width="300" /> 
  <img src="https://user-images.githubusercontent.com/36040421/135911140-a1142151-57ee-4196-8c21-406bf907df3d.png" width="300" />
</p>

>Progression of fuel radius (and whole geometry) during iterations of the script.

<br/><br/>
The [EPR lattice model](./model_xml) is created via a [template class](./templates/EPR_assembly.py) and modified during the execution of the [main script](main.py).
The k-inf mean values are saved one by one with the corrisponding standard deviations during the execution of the script on an [csv file](./output/data.csv). The main script can be run in  simulation mode (using -r argument in CLI) or bypassing the simulation and executing only the post processing file (no arguments passed in CLI).\
Only 1/4 of the geometry is used but there is the possibility of using the whole assembly geometry. The burnable absorbers configuration can also be changed choosing one of 4 [possible configurations](https://github.com/LorenzoMazzocco/OpenMC-projects/files/7280552/EPR.core.design.pdf). 
<br/><br/>
<br/><br/>

## RESULTS
The resulting dependency is pictured in a simple plot ([results.png](.results.png)):

<img src='https://user-images.githubusercontent.com/36040421/135904923-3c9e58ed-c974-44d2-ba30-1d19b2053019.png' width='800'/>

We can verify that the simulation results match the existing literature:

<a href="https://www.nuclear-power.com/nuclear-power/reactor-physics/reactor-dynamics/moderator-to-fuel-ratio/">
<img src='https://user-images.githubusercontent.com/36040421/135906300-104811c7-34a5-491c-a480-d25e358a9839.png' width='800' />
<a/>
  
>Image linked to source (www.nuclear-power.com)
  
>Milan (IT), october 2021
  
 
