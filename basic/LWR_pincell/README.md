# LWR PINCELL

This simulation is performed on a simple LWR pincell surrounded by unborated pure water (infinite lattice).

## Geometry and Materials

>**FUNDAMENTAL GEOMETRY PARAMETERS**
>- Fuel pellet outer radius: 0.39 cm
>- Cladding inner radius: 0.40 cm
>- Cladding outer radius: 0.46 cm
>- Lattice pitch: 1.26 cm

>**FUNDAMENTAL MATERIAL PARAMETERS**
>- Fuel: UO2 (5.0% wt enrichment) (yellow)
>- Helium (green)
>- Cladding: pure Zr (grey)
>- Water (blue)

The following [plot](./images/geometry/) represents the top view of the model:

<p align='center'>
<img src="https://user-images.githubusercontent.com/36040421/136110866-9e758c69-c50f-4015-b391-b21411fbb2b5.png" width="300" />
<p/>
<br></br>

## Tallies, mesh and data representation

The used mesh is a rectangular regular 300x300 mesh.

>**TALLIED QUANTITIES**
>- flux spectrum (all geometry)
>- capture reaction rate (mesh)
>- fission reaction rate (mesh)
>- neutron flux (mesh)
>- neutron mean energy (mesh)
>- recoverable energy from fission (mesh)

(Please note that all this quantities are not normalized and therefore the unit of measure depends on the number of neutron sources for the eigenvalue simulation, which are not quantified. The results should be read as relative changes throughout the geometry)

The results are represented in 2 different ways:
- mesh plot (top view)
- radial distribution (side view)

Following are examples for each plot type:

**Mesh Plot**\
<img src="https://user-images.githubusercontent.com/36040421/136111482-2d89d37e-1881-452b-b0f3-a78df8063712.png" width="400" />
<br></br>
**Radial**\
<img src="https://user-images.githubusercontent.com/36040421/136111519-44035d9b-4890-49ec-bb07-d49cad459e19.png" width="500" /> 
<br></br>

