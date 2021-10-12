# PLUTONIUM PRODUCTION IN LWR PINCELL

This is the first depletion simulation I performed. The goal of the project is to investigate the isotopic composition of 
plutonium produced in a PWR pincell at low burnup. In particular we want to know at which burnup (and the corresponding time of irradiation)
the plutonium crosses the weapon-grade composition threshold (7% Pu-240).

## Model
We use the previously [developed model](lib/Templates/EPR.py) for the EPR pincell with a concentration of boron in the borated water of 2000 ppm. \

The depletion chained used was the [semplified LWR spectrum depletion chain](https://openmc.org/depletion-chains/) supplied by the OpenMC website. 

The stepsizes were set to one week for 104 weeks with the first month having a 1 day step size. The total number of eigenvalue simulations performed was 130.


## Results
The results are represented in plots that can be found in the [images](images/) folder.
<br><br/>
### Isotopic composition
<p align='center'>
  <img src='https://user-images.githubusercontent.com/36040421/137033708-7f558fd0-4862-4b86-926d-8911c306239e.png' width=700 />
<p/>
<br><br/>

### Plutonium grade 
<p align='center'>
  <img src='https://user-images.githubusercontent.com/36040421/137033822-c6e74a9d-7504-4d45-8276-d93a0094055a.png' width=700 />
<p/>


We can see that the weapon grade Pu is produced for burnups between 1 and 5 GWd/MTHM. After 20 weeks of irradiation in the reactor core (burnup of 5 GWd/MTHM) the plutonium can be classified as 'fuel grade plutonium'.

<br><br/>

> Milan (IT), october 2021
