# EPR assembly lattice

This simulation concernes a 17x17 assembly infinite lattice from the [original EPR core design](https://github.com/LorenzoMazzocco/OpenMC-projects/files/7281364/EPR.core.design.pdf).
The simulation is performed on the top-left quarter of the geometry but the resulting mesh data is extended and flipped to represent the whole assembly.
<br></br>

## Geometry and materials

The model presents 3 different types of pins:
-Fuel rods (yellow)
-Gd burnable absorber integral rods (pink)
-instrumentation and control rods channels

>**FUNDAMENTAL GEOMETRY PARAMETERS**\
>Fuel pellet outer radius: 0.3975 cm\
>Cladding inner radius: 0.4125 cm\
>Cladding outer radius: 0.4750 cm\
>Lattice pitch: 1.26 cm\
>Assembly side: 21.42 cm

>**FUNDAMENTAL MATERIAL PARAMETERS**\
>Fuel: UO2 (3.0% wt enrichment) (yellow)
>BA: UO2-Gd2O3 (UO2 0.25% wt enr. - 8% wt Gd2O3) (pink)
>Cladding: M5 alloy (Zr 98.875 %wt - Nb 1 %wt - O 0.125 %wt)
<br></br>

The BA (Burnable Absorber) rods can change in number. We can have 4 different configurations, in order 8 BA, 12 BA, 16 BA, 20 BA

<p float="left">
  <img src="https://user-images.githubusercontent.com/36040421/135927626-10d8c1d2-753a-4305-90b6-be0676913de1.png" width="220" />
  <img src="https://user-images.githubusercontent.com/36040421/135927633-a08d1e9f-d4d2-4d5e-88bf-ea7b073b3f6d.png" width="220" /> 
  <img src="https://user-images.githubusercontent.com/36040421/135927637-788702c2-427f-4127-9aa3-85bb50cc4383.png" width="220" />
  <img src="https://user-images.githubusercontent.com/36040421/135927642-7e3fe04d-4d90-4bb4-9979-eb607fd5df92.png" width="220" />
</p>

The modeled configurations are taken from the [original EPR core design](https://github.com/LorenzoMazzocco/OpenMC-projects/files/7281364/EPR.core.design.pdf), as shown in the following 
figure taken from the paper:

<p align="center">
<img src="https://user-images.githubusercontent.com/36040421/135928035-8386af87-276e-4adf-978b-77f9eb09066c.png" width="400" />
</p>
