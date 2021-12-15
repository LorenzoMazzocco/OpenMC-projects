# FULL CORE TRIGA

The objective of this project is to model a full 3D core of the Mk II TRIGA Research Reactor in Pavia (IT) and verify the validity of the model confronting the control rod calibration curves with experimental data. Multiple simplifications to the geometry were implemented.
The main reference for this work is this [PhD Thesis](https://github.com/LorenzoMazzocco/OpenMC-projects/files/7717554/Development.and.Experimental.Validation.of.a.Monte.Carlo.Simulation.Model.for.the.TRIGA.Mark.II.Reactor.pdf) by Davide Chiesa.

## THE MODEL

<p float="center">
  <img width="426" src="https://user-images.githubusercontent.com/36040421/146150346-c3f37d41-900a-4b4b-96d2-5b9efad0dfb8.png">
  <img width="435" src="https://user-images.githubusercontent.com/36040421/146150357-348198f7-992d-41f3-918e-ec73e01c33fd.png">
</p>
<br></br>
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
  <img width="426" height="300" src="https://user-images.githubusercontent.com/36040421/146158406-c0dd90ac-d50b-4ce0-91f3-1f33c6a0a08b.png">
  <img width="435" height="300" src="https://user-images.githubusercontent.com/36040421/146158436-2297bef8-940d-4b80-bc2f-29df4fae865d.png">
</p>

The original configuration, shown below, was slightly simplified:

<img width="511" alt="Schermata 2021-12-15 alle 10 21 17" src="https://user-images.githubusercontent.com/36040421/146158893-2065011f-6595-44f4-917f-1421e7238fed.png">

Each control rods height level is parametrized in order to perform the calibration. The experimental data for validations provides control rods' height values in digits from the controller room display. The digit do not have any physical meaning but conversion functions for each rod are coded [here](./utils.py).

<br></br>
<br></br>

### FUEL RODS
The fuel matrix is ZrH (UZrH) with 20% wt enriched uranium.
The fuel elements consist of single rods disposed directly into the core without the need for an assembly-type configuration.
The following fuel types were provided:
<p float="center">
  <img width="589" src="https://user-images.githubusercontent.com/36040421/146161124-82d49119-5091-429c-8cba-00e9f62cf05c.png">
</p>

We've only selected the 101-Type and removed the little extention of graphite inside of the fuel matrix. Following are a full-geometry picture and a close up to highligh the presence of the cladding and of the Samarium burnable absorber disk:

<img width="427" alt="Schermata 2021-12-15 alle 10 37 38" src="https://user-images.githubusercontent.com/36040421/146161770-b438775b-a585-4286-b135-445a6ff7aced.png">

<img width="430" alt="Schermata 2021-12-15 alle 10 37 44" src="https://user-images.githubusercontent.com/36040421/146161781-33357eaa-811a-4ad0-9c23-ab1b74d90978.png">

<br></br>
<br></br>

### CONTROL RODS
There are three control rods. Each one has a different radial geometry but they all have the same axial geometry.

- SHIM: made of B4C, used to perform coarse variation of the k_eff during operation;
- TRANS: made of borated graphite (BG), was used to perform pulse experiments but nowadays has only safety purposes and is rarely used;
- REG: made of B4C, used to fine-tune k_eff at 1 during operation;

Following are a full-geometry picture of the REG control rod and a close up to highligh the presence of the cladding:

<img width="400" alt="Schermata 2021-12-15 alle 10 55 21" src="https://user-images.githubusercontent.com/36040421/146164715-d992339e-0340-4ee7-a391-b9651b2d068d.png">

<img width="434" alt="Schermata 2021-12-15 alle 10 56 27" src="https://user-images.githubusercontent.com/36040421/146164791-92b3ba5e-05ea-48ff-89f9-3b4e20c3b6a0.png">

>Milan (IT), november 2021


