# LATTICE PLOT TOOL

The goals of this project are:
- introduce a [plotting tool](images/) to rerpresent information on single pincells of an assembly lattice
- order proprietary [templates](lib/Templates/) and [plotting tools](lib/PostProcessing/) in a library to be copied, updated and used in other projects
 <br></br>

The model used is a standard EPR assembly infinite lattice with 20 Gd burnable absorber rods. 

<p align='center'>
<img src="https://user-images.githubusercontent.com/36040421/135927642-7e3fe04d-4d90-4bb4-9979-eb607fd5df92.png" width="400" />
</p>
<br></br>
 
 We tally from the single rods the following information:
 - recoverable fission power (fission-q-recoverable)
 - radiative capture by U-238 reaction rate
<br></br>

Normalizing and elaborating on the tallied quantities it is pretty straightforward to compute, for each rod:
- linear power (W/cm) [image](images/power.png)
- Pu-239 production rate (mg/h) [image](images/plutonium.png)
<br></br>

## RESULTS
The resulting plots can be found in the [images folder](images/).

### Linear Power

<p align='center'>
<img src="https://user-images.githubusercontent.com/36040421/136711856-ae69ef23-2676-4213-8bbc-85645788015e.png" width="600" />
</p>


### Plutonium Production

<p align='center'>
<img src="https://user-images.githubusercontent.com/36040421/136711905-12042ede-df6c-4830-b448-0c1c8d99ef57.png" width="600" />
</p>

<br></br>
<br></br>

>Milan (IT), october 2021
