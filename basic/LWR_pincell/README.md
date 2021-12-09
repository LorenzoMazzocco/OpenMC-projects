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
<br></br>

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

(Please note that all this quantities are not normalized and therefore the unit of measure depends on the number of neutron sources for the eigenvalue simulation, which is not computed. The results should be read as relative changes throughout the geometry)

The results are represented in 2 different ways:
- mesh plot (top view)
- radial distribution (side view)

Following are examples for each plot type:

**Mesh Plot**\
<a href='https://github.com/LorenzoMazzocco/OpenMC-projects/tree/main/basic/LWR_pincell/images/plots' >
<img src="https://user-images.githubusercontent.com/36040421/136111482-2d89d37e-1881-452b-b0f3-a78df8063712.png" width="400" />
<a />
<br></br>
**Radial**\
<a href='https://github.com/LorenzoMazzocco/OpenMC-projects/tree/main/basic/LWR_pincell/images/radial_plots' >
<img src="https://user-images.githubusercontent.com/36040421/136111519-44035d9b-4890-49ec-bb07-d49cad459e19.png" width="500" /> 
<a />
<br></br>
<br></br>

## Interesting Results

### Fission reaction rate distribution is not uniform in fuel
When we plot the distribution of specific fission reaction rates across the geometry we can notice that inside the fuel pellet the distribution is not uniform.
In particular we can see that it increases proportionally to radial distance from the symmetry axis of the geometry. The following radial distribution plot is revealing:

<p align='center'>
<img src="https://user-images.githubusercontent.com/36040421/136120084-7bc47240-7d4f-4fd9-b93b-720fc616e97d.png" width="600" /> 
<br></br>
<img src="https://user-images.githubusercontent.com/36040421/136120228-8a46066d-22df-43e7-a8a1-91ef24a64c55.png" width="500" /> 
<p/>
<br></br>

The cause of this phenomena finds his roots in the scattering phenomena affecting neutrons. Fast neutrons are generated in the fuel pellet following fission events, they are then slowed down by moderating materials (in the case of a LWR almost only by water). Thermalized neutrons are more probable to cause a fission event with U-235. It is therefore quite predictable to see more fission events occur in the region of the fuel closer to water:

<p align='center'>
<img src="https://user-images.githubusercontent.com/36040421/136120495-c97a3085-fc9f-46d4-9682-9af2c65a1136.png" width="600" /> 
<p/>
<br></br>

Therefore the hypotesis that comes up naturally is that the higher fission reaction rates at the edge of the fuel pellet are a consequence of the higher thermalization of neutrons in that region. To verify this hypotesis we implemented an algorithm that for each cell mesh 
tallies the neutron spectrum (10 energy levels) and computes the mean energy of the neutrons in that region of the model. We can then plot the results in a mesh plot and on the side view to observe the radial distribution:

<p align='center'>
<img src="https://user-images.githubusercontent.com/36040421/136120973-1edd97df-a29c-41f6-a032-4e6f5a82fd36.png" width="600" /> 
<br></br>
<img src="https://user-images.githubusercontent.com/36040421/136120967-7d5dfa9f-63d4-4a84-85f4-07aadb327276.png" width="600" /> 
<p/>
<br></br>

As we can see the neutron spectrum of neutrons radially thermalizes and therefore our hypothesis was correct. 


>Milan (IT), october 2021

