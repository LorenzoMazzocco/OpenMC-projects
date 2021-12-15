# FULL CORE TRIGA

The objective of this project is to model a full 3D core of the Mk II TRIGA Research Reactor in Pavia (IT) and verify the validity of the model confronting the control rod calibration curves with experimental data. Multiple simplifications to the geometry were implemented.
The main reference for this work is this [PhD Thesis](https://github.com/LorenzoMazzocco/OpenMC-projects/files/7717554/Development.and.Experimental.Validation.of.a.Monte.Carlo.Simulation.Model.for.the.TRIGA.Mark.II.Reactor.pdf) by Davide Chiesa.

## THE MODEL

<p float="center">
  <img width="426" src="https://user-images.githubusercontent.com/36040421/146150346-c3f37d41-900a-4b4b-96d2-5b9efad0dfb8.png">
  <img width="435" src="https://user-images.githubusercontent.com/36040421/146150357-348198f7-992d-41f3-918e-ec73e01c33fd.png">
</p>
<br></br>

### CORE
The core has a cylindrical geometry and consists of 5 concentric rings that develop around a central irradiation tube filled with air. The outer ring mainly consists of graphite rods. The core is then surrounded by graphite to reflect leaking neutrons.
There are three control rods (SHIM, REG, TRANS) disposed with a relative angle of 120° to balance the neutron flux.

> COLORS 
>- Fuel: gray 
>- Graphite: yellow
>- Boron (CR): red 
>- Water: blue 
>- Air: pink 

<p float="center">

</p>
