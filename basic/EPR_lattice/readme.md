# EPR ASSEMBLY LATTICE

This simulation concernes a 17x17 assembly infinite lattice from the [original EPR core design](https://github.com/LorenzoMazzocco/OpenMC-projects/files/7281364/EPR.core.design.pdf).
The simulation is performed on the top-left quarter of the geometry but the resulting mesh data is extended and flipped to represent the whole assembly.
<br></br>

## GEOMETRY AND MATERIALS

The model presents 3 different types of pins:
- Fuel rods (yellow)
- Gd burnable absorber integral rods (pink)
- Instrumentation and control rods channels

>**FUNDAMENTAL GEOMETRY PARAMETERS**
>- Fuel pellet outer radius: 0.3975 cm
>- Cladding inner radius: 0.4125 cm
>- Cladding outer radius: 0.4750 cm
>- Lattice pitch: 1.26 cm
>- Assembly side: 21.42 cm

>**FUNDAMENTAL MATERIAL PARAMETERS**
>- Fuel: UO2 (3.0% wt enrichment) (yellow)
>- BA: UO2-Gd2O3 (UO2 0.25% wt enr. - 8% wt Gd2O3) (pink)
>- Cladding: M5 alloy (Zr 98.875 %wt - Nb 1 %wt - O 0.125 %wt) (grey)
<br></br>

The BA (Burnable Absorber) rods can change in number. We can have 4 different configurations, in order 8 BA, 12 BA, 16 BA, 20 BA

<p align="center">
  <img src="https://user-images.githubusercontent.com/36040421/135927626-10d8c1d2-753a-4305-90b6-be0676913de1.png" width="250" />
  <img src="https://user-images.githubusercontent.com/36040421/135927633-a08d1e9f-d4d2-4d5e-88bf-ea7b073b3f6d.png" width="250" /> 
  <img src="https://user-images.githubusercontent.com/36040421/135927637-788702c2-427f-4127-9aa3-85bb50cc4383.png" width="250" />
  <img src="https://user-images.githubusercontent.com/36040421/135927642-7e3fe04d-4d90-4bb4-9979-eb607fd5df92.png" width="250" />
</p>

The modeled configurations are taken from the [original EPR core design](https://github.com/LorenzoMazzocco/OpenMC-projects/files/7281364/EPR.core.design.pdf), as shown in the following 
figure taken from the paper:

<p align="center">
<img src="https://user-images.githubusercontent.com/36040421/135928035-8386af87-276e-4adf-978b-77f9eb09066c.png" width="400" />
</p>
<br></br>

## TALLIES, MESH AND DATA REPRESENTATION
The used mesh is a rectangular regular 300x300 mesh.

>**TALLIED QUANTITIES**
>- flux spectrum (all geometry)
>- capture reaction rate (mesh)
>- fission reaction rate (mesh)
>- neutron flux (mesh)
>- recoverable energy from fission (mesh)

(Please note that all this quantities are not normalized and therefore the unit of measure depends on the number of neutron sources for the eigenvalue simulation, which are not quantified. The results should be read as relative changes throughout the geometry)\

The results are represented in 2 different ways:
- mesh plot (top view)
- radial distribution (side view)

Note that the radial distribution side view can be horizontal (vertical plane cutting the assembly horizontally at y=0) or diagonal (vertical plane cutting the assebly diagonally at 45° y=x). Following are 3 examples, one for each type of plot:

**Mesh Plot**\
<img src="https://user-images.githubusercontent.com/36040421/135933999-f006cb36-a765-4b5a-a9f3-f799dcf8357d.png" width="400" />
<br></br>
**Radial Horizontal**\
<img src="https://user-images.githubusercontent.com/36040421/135934059-b2a8f38b-e70b-4ed6-b007-496948431ef6.png" width="500" /> 
<br></br>
**Radial Diagonal**\
<img src="https://user-images.githubusercontent.com/36040421/135934084-b9731132-4ea2-41a0-9c00-bb8a66eba819.png" width="500" />
<br></br>


>Hint: the radial diagonal distribution plots represent the influence of the BA rods while radial horizontal plots are limited to fuel rods and channels. 

All of the plots can be found in the images folder for every configuration ([8 BA](./images/config_8_BA/) - [12 BA](./images/config_12_BA/) - [16 BA](./images/config_16_BA/) - [20 BA](./images/config_20_BA/)).

<br></br>

## INTERESTING RESULTS


### Influence of BA on neutron flux
It is evident that the gadolinium burnable absorbers have a strong influence on the value of the neutron flux throughout the geometry. In particular around a BA rod the flux significantly reduces (this is because of the absence of fission events and the subsequent release of prompt neutrons). The following plots are revealing:

<p align="center">
  <img src="https://user-images.githubusercontent.com/36040421/135936161-452dd61d-4a19-4fb8-8f3f-091eca29368c.png" width="550" />
  <img src="https://user-images.githubusercontent.com/36040421/135934538-eac388e4-d61a-4fcb-83c2-87a237233c04.png" width="700" />
</p>
<br></br>

### Influence of control rod channels neutron moderation and fission
From the elastic scattering reaction rate mesh plot it seems that inside the water filled control rods and instrumentation channels the number of scattering events is greater than in the other areas of the geometry filled with water. This is because of the great quantity of moderator present inside the channels and the distance from any source of neutron absorber. The radial plot confirms this:

<p align="center">
  <img src="https://user-images.githubusercontent.com/36040421/135935709-a8054aeb-2e4c-45cd-9e0f-5de7d2b00f43.png" width="550" />
  <img src="https://user-images.githubusercontent.com/36040421/135935741-1982adfc-b0d9-4bcc-a869-524ff1797b23.png" width="700" />
</p>

This particular anomaly of the distribution of scattering events has the direct consequence of facilitating fission in the fuel rods around the channels.
We can clearly see from the mesh plot and radial distribution plot of fission reaction rate density that there is also a soft gradient of fission events rates inside the same fuel rod, increasing towards the side near the channel.

<p align="center">
  <img src="https://user-images.githubusercontent.com/36040421/135936086-3fd9a5b0-c06b-4fe6-bd52-444250592267.png" width="550" />
  <img src="https://user-images.githubusercontent.com/36040421/135936116-5ff51223-b685-43ef-8ac6-90102057114e.png" width="700" />
</p>


>Milan (IT), october 2021
