# Plutonium breeding metric
This project is looking for an answer to the following question: what is the optimal neutron energy to breed weapon grade plutonium?


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
complex post-processing work to be useful for the analysis that we want to perform. Therefore the delta metric is clearly superior since it is defined as a positive
ratio that we want to maximize.

> Note that can be proven that the two metrics convey the exact same information and therefore there is no downside to using delta instead of mu.

<br><br/>

The nuclides' of interest nuclear data is written following endf-6 format and can be found in the [endf](endf/) directory.
