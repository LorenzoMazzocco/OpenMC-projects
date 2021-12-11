# Moderator-to-fuel ratio effect on k-inf 

The main goal of this project is to investigate the dependency of k-inf for an [EPR assembly lattice](https://github.com/LorenzoMazzocco/OpenMC-projects/files/7280552/EPR.core.design.pdf) on the ratio of moderator over fuel material in volume.\
\
The model is an EPR assembly infinite lattice with a parametrized assembly pitch.
The fuel and cladding geometries are fixed. n different pitches radiuses are tested and the corresponding k-inf is computed. The errorbars are not present in the [resulting 
plot](results.png) because the standard deviations of the k-inf distributions are negligible for all the configurations considered.
<br/><br/>


<p float="left">
  <img src="https://user-images.githubusercontent.com/36040421/145688972-2826dc52-7cdd-41d3-bf6f-05349433bece.png" width="300" />
  <img src="https://user-images.githubusercontent.com/36040421/145688987-ca9dd2a1-a54b-4e4f-84af-56821e92c835.png" width="300" /> 
  <img src="https://user-images.githubusercontent.com/36040421/145688993-2b3ede87-21e8-4d09-ac26-d5ef11616d16.png" width="300" />
</p>

>Progression of assembly pitch (and whole geometry) during iterations of the script.

<br/><br/>
The [EPR lattice model](./model_xml) is created via a [template class](./templates/EPR_assembly.py) and modified during the execution of the [main script](main.py).
The k-inf mean values are saved one by one with the corrisponding standard deviations during the execution of the script on an [csv file](./output/data.csv). The main script can be run in  simulation mode (using -r argument in CLI) or bypassing the simulation and executing only the post processing file (no arguments passed in CLI).\
The complete geometry is used to run the simulation but there is the possibility of using just 1/4 of it (partial geometry). The burnable absorbers configuration can also be changed choosing one of 4 [possible configurations](https://github.com/LorenzoMazzocco/OpenMC-projects/files/7280552/EPR.core.design.pdf). 
<br/><br/>
<br/><br/>

## RESULTS
The resulting dependency is pictured in a simple plot ([results.png](.results.png)):

<img src='https://user-images.githubusercontent.com/36040421/145689022-18d3ac68-6e18-4db9-9df9-22320d3bbff2.png' width='800'/>

We can verify that the simulation results match the existing literature:

<a href="https://www.nuclear-power.com/nuclear-power/reactor-physics/reactor-dynamics/moderator-to-fuel-ratio/">
<img src='https://user-images.githubusercontent.com/36040421/135906300-104811c7-34a5-491c-a480-d25e358a9839.png' width='800' />
<a/>
  
>Image linked to source (www.nuclear-power.com)
  
>Milan (IT), october 2021
  
 
