# WGP breeding metric
For the successful deployment of advanced nuclear reactors it is crucial to tackle the proliferation issues.  
This project is looking for an answer to the following question: what is the optimal neutron energy to breed weapon grade plutonium?
Answering this question will give us some insights on how we can engineer more proliferation-resistant reactor cores.

We proceed by creating a metric that tells us the ability of a system to breed WGP and then we analyze to what extent it is minimizable.

We know that WGP is defined by having an isotopic composition consisting of a maximum of 7%ao of Pu240. So ideally we want to increase the amount of Pu239 and reduce as
much as possible the amount of Pu240. Following this logic we construct two metrics (mu and delta) using microscopic cross section for the following reactions:
- U238 - radiative capture (238_c)
- Pu239 - radiative capture (239_c)
- Pu239 - fission (239_f)
- Pu240 - radiative capture (240_c)
- Pu240 - fission (240_f) 

We want a metric that is non dimensional and indipendent from the neutron flux. We propose the following two:

<pre>
&#956 = [Pu239 net production rate] / [Pu240 net production rate]
&#956(E, T) = [&#963<sub>c,238</sub> - (&#963<sub>f,239</sub> + &#963<sub>c,239</sub>)] / [&#963<sub>c,239</sub> - (&#963<sub>f,240</sub> + &#963<sub>c,240</sub>)]


&#948 = [Upgrading events rate] / [Downgrading events rate]
&#948(E, T) = [&#963<sub>c,238</sub> +  &#963<sub>f,240</sub> + &#963<sub>c,240</sub>] / [&#963<sub>f,239</sub> + &#963<sub>c,239</sub>]
</pre>


Both the metrics have a physical meaning but it is clear from a brief analysis that the metric mu has the problem of
depending from the numerator and denominator's sign. Therefore the metric mu assumes different meanings in different regions of the energy spectrum and has to undergo
complex post-processing work to be useful for the analysis that we want to perform. The delta metric is clearly superior since it is defined as a positive
ratio that we want to minimize.

> Note that it can be proven that the two metrics convey the exact same information and therefore there is no downside to using delta instead of mu. This 
> is done later in this readme.

The nuclides' of interest nuclear data is written following endf-6 formatting and can be found in the [endf](endf/) directory.

<br><br/>

## Results

The results are saved in the [images](images/) folder. There are 3 main plot types produced:
- delta as a function of E
- mu as a function of E
- mu numerator and denominator as a function of E

each of these plot types is replicated for every temperature available in the endf datasets for the selected reaction and nuclides. The name of the files is the temperature in kelvin.
<br><br/>

### Delta metric
<p align='center'>
  <img src='https://user-images.githubusercontent.com/36040421/137566240-41fb0002-98ba-4c97-bb2e-16e2a1c200f9.png' width=700/>
<p/>
<br><br/>
 
### Mu metric
<p align='center'>
  <img src='https://user-images.githubusercontent.com/36040421/137566670-44fafb82-9775-4184-aa74-c46fb673bc68.png' width=700/>
<p/>


>Note that the [mu](images/mu) and [mu_nom_den](images/mu_num_den) folders and plots are included for sake of completeness but are not relevant to the original question that we posed ourself at the beginning of this project since the delta metric is clearly superior for this purpouse.Having said that if you want to explore the mu plots keep in mind that different colors are attributed to different spectra regions in order to represent the different physical meaning that arise from the numerator and denominator's sign.

<br><br/>


### Two metrics, one meaning
Despite delta and mu having a very different look they convey the same information. In this section we will demonstrate this in a brief empirical analysis of the two metrics computed at a temperature of 900K.

<p align='center'>
  <img src='https://user-images.githubusercontent.com/36040421/137587203-d7769b7d-bfcb-476e-939b-410e60c59c95.png' width=400 />
  <img src='https://user-images.githubusercontent.com/36040421/137587213-d5fc287e-cecd-4228-9d23-c01d0f05ccd2.png' width=400 />
</p>

It is clear that the mu metric presents the 'orange configuration' (numerator and denominator are both negative) for the thermal and fast region of the spectrum. 
When both the numerator and the denominator are negative it means that we are destroying Pu239 and destroying Pu240. Therefore the reciprocal of mu (1/mu) in that region represents the ratio between the number of Pu240 isotopes destroyed per unit time over the number of Pu239 isotopes destroyed per unit time. It is clear that we want to maximize 1/mu in this region if we want to breed WGP. 
Let's now compare the values for mu and delta in the thermal region:

<p align='center'>
  <img src='https://user-images.githubusercontent.com/36040421/137587621-02d87efa-c790-48b5-897d-aeaaa78e4570.png' width=300 />
  <img src='https://user-images.githubusercontent.com/36040421/137587622-4df7dbba-b00c-4492-8ee8-809a10f48681.png' width=300 />
</p>

Note that both the values are constant in the thermal region. The value of delta is lower than one (I'm downgrading the Pu more that I'm upgrading it) and the value of mu is greater than one (I'm destroying more Pu239 than I'm destroying Pu240). The physical meaning is the same.\
Let's now focus on the fast region of the spectrum:

<p align='center'>
  <img src='https://user-images.githubusercontent.com/36040421/137587784-146979ff-72c9-449f-b98c-4bd1def7e2db.png' width=250 />
  <img src='https://user-images.githubusercontent.com/36040421/137587792-c0b051fb-ad30-44e5-8d3a-ef46ee55718c.png' width=250 />
</p>
Looking at the orange portion for mu, the values for delta and 1/mu show strong correspondence even for little variations./
For the neutron energy of exactly 1 eV this bond between the two functions really stands out:

<p align='center'>
  <img src='https://user-images.githubusercontent.com/36040421/137588149-105ee187-e990-4c0c-a205-02b877f04008.png' width=250 />
  <img src='https://user-images.githubusercontent.com/36040421/137588153-fbd7d8fa-8c54-4879-a2ed-7402580ff04f.png' width=250 />
</p>
As the value of mu approaches zero (meaning that we are not destroying Pu239 but still destroying Pu240) the value of delta spikes up to a local maximum.
<br></br>
<br></br>

## Taking into account the isotopic composition 
We identified the delta metric as the simplest and most effective but both the metrics proposed are indipendent of the isotopic composition of the material to be irradiated. This is a problem since the weights given to the different cross section are all the same (unitary) but in a realistic scenario our sample will have much more U238 than Pu239 or Pu240. To correct the formula we simply assign each cross section a coefficient equal to the atom percentage of the corrisponding isotope (for isotope i is n_i/n_tot, with n=atomic density (atoms/cm3)). Therefore we obtain the following formula:


<pre>
&#916(E, T) = {(n<sub>238</sub>/n<sub>tot</sub>)*&#963<sub>c,238</sub> +  (n<sub>240</sub>/n<sub>tot</sub>)*(&#963<sub>f,240</sub> + &#963<sub>c,240</sub>)} / {(n<sub>239</sub>/n<sub>tot</sub>)*(&#963<sub>f,239</sub> + &#963<sub>c,239</sub>)}

simplifing 1/n<sub>tot</sub> in the numerator and denominator we are left with:

&#916(E, T) = {(n<sub>238</sub>)*&#963<sub>c,238</sub> +  (n<sub>240</sub>)*(&#963<sub>f,240</sub> + &#963<sub>c,240</sub>)} / {(n<sub>239</sub>)*(&#963<sub>f,239</sub> + &#963<sub>c,239</sub>)}

which can be written in a compact way by using macroscopic cross sections:

&#916(E, T) = [&#931<sub>c,238</sub> +  &#931<sub>f,240</sub> + &#931<sub>c,240</sub>] / [&#931<sub>f,239</sub> + &#931<sub>c,239</sub>]
</pre>

Now we have a metric that takes into consideration the isotopic composition but we have added 3 more degrees of freedom: n_238, n_239, n_240. Those variables can be chosen arbitrarily but it is way more useful to simulate a realistic isotopic composition for the problem we are considering. In order to do that we retrieve data from the [burnup simulation of a LWR pincell project](https://github.com/LorenzoMazzocco/OpenMC-projects/tree/main/advanced/LWR_pincell_Pu) on the atom count for U238, Pu239 and Pu240. Now our metric depends only on energy E, temperature T and time t. To simplify the analysis we are goint to stick to a temperature of 600K and substitute time with burnup b in GWd/MTHM.\
For each timestep of the burnup simulation we generate a plot of DELTA(E) at 600K, we then collect all the images in a GIF animation to better understand the evolution of the metric over the spectrum as the burnup increases.
Following is the resulting animation that can be found in the main folder at [movie.gif](movie.gif):
<br><br/>
<p align='center'>
  <img src='movie.gif' width=750 />
</p>

<br><br/>
The first thing we notice is that as the burnup increases the value of the metric decreases. This is because the isotopic prevalence of Pu239 increases and that of U238 decreases.
We also notice a clear morphologic change when the function slowly spikes at exactly 1eV for burnups greater than 2 GWd/MTHM. The cause of the spike is due to the fission and capture cross section of Pu240 and the effects begin to manifest themself when we start to create Pu240.\
Following we can see the isotopic composition of Pu as the burnup increases and the fission cross section for Pu240:

<br><br/>
<p align='center'>
  <img src='https://user-images.githubusercontent.com/36040421/138093658-5bb87e95-a368-4fc7-8dfa-ac656b0821bf.png' width=600 />
</p>
<p align='center'>
  <img src='https://user-images.githubusercontent.com/36040421/138093678-86571b0e-d838-4578-bcc4-4ca03fb12b29.png' width=750 />
</p>
<br></br>
<br></br>

> Milan (IT), october 2021
