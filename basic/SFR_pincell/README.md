# LWR PINCELL

This simulation is performed on a sodium fast reactor (SFR) fuel pincell with oxide U/Pu fuel. The geometry and materials used are based on the 
[European Fast Reactor core model](https://github.com/LorenzoMazzocco/OpenMC-projects/files/7296290/1-s2.0-S0029549316304472-main.pdf).

## Geometry and Materials

>**FUNDAMENTAL GEOMETRY PARAMETERS**
>- Fuel pellet outer radius: 0.0.4715 cm
>- Cladding inner radius: 0.4865 cm
>- Cladding outer radius: 0.5365 cm
>- Lattice pitch: 1.073 cm

>**FUNDAMENTAL MATERIAL PARAMETERS**
>- Fuel: U/PuO2 ([detailed isotopic composition](./model_xml/materials.xml)) (yellow)
>- Cladding: copper/aluminium oxide alloy (Cu 0.3 %wt) (grey)
>- Sodium (only Na23) (orange)

The following plot represents the top view of the model:
<br></br>

<p align='center'>
<img src="https://user-images.githubusercontent.com/36040421/136262053-af6c8970-50d0-4fa8-9416-ef0c6587150d.png" width="300" />
<p/>
<br></br>

## Tallies, mesh and data representation

The used mesh is a rectangular regular 300x300 mesh.

>**TALLIED QUANTITIES**
>- flux spectrum (all geometry)
>- capture reaction rate (mesh)
>- fission reaction rate (mesh)
>- neutron flux (mesh)
>- recoverable energy from fission (mesh)

(Please note that all this quantities are not normalized and therefore the unit of measure depends on the number of neutron sources for the eigenvalue simulation, which are not quantified. The results should be read as relative changes throughout the geometry)

The results are represented in 2 different ways:
- mesh plot (top view)
- radial distribution (side view)

Note that the radial distribution side view can be horizontal (vertical plane cutting the assembly horizontally at y=0) or diagonal (vertical plane cutting the assebly diagonally at 45° y=x). Following are 3 examples, one for each type of plot:

Following are examples for each plot type:

**Mesh Plot**\
<a href="https://github.com/LorenzoMazzocco/OpenMC-projects/tree/main/basic/SFR_pincell/images/plots">
<img src="https://user-images.githubusercontent.com/36040421/136263161-c35aefdf-12fd-4db6-921a-3728c90cbc1e.png" width="400" />
<a/>
<br></br>
**Radial Horizontal**\
<a href="https://github.com/LorenzoMazzocco/OpenMC-projects/tree/main/basic/SFR_pincell/images/radial_plots/horizontal">
<img src="https://user-images.githubusercontent.com/36040421/136263299-ce8167d8-bb9a-4ddf-82e9-f1d1e45be19f.png" width="500" /> 
<a/>
<br></br>
**Radial Diagonal**\
<a href="https://github.com/LorenzoMazzocco/OpenMC-projects/tree/main/basic/SFR_pincell/images/radial_plots/diagonal">
<img src="https://user-images.githubusercontent.com/36040421/136263200-873a06b5-6c3f-450c-8650-926ecb2c2573.png" width="500" /> 
<a/>
<br></br>
<br></br>

## Interesting Results

### Harder neutron flux spectrum

Since this model is part of a fast reactor no moderator is present. We can therefore verify that the distribution of neutrons energies in the geometry considered is 
significantly leaning towards high energies.

<p align='center'>
<img src="https://user-images.githubusercontent.com/36040421/136270474-d5ec76ab-183e-4396-95e9-4687ce8a86e1.png" width="600" /> 
<p/>
<br></br>

The results obtained can be compared with the flux spectrum of a light water moderated reactor such as the EPR:

<p align='center'>
<img src="https://user-images.githubusercontent.com/36040421/136270757-a200380e-965f-4fce-875d-00a188e6973b.png" width="600" /> 
<p/>
<br></br>



>Milan (IT), october 2021
