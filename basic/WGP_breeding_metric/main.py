import openmc.data

import numpy as np
import matplotlib.pyplot as plt

#MT reaction codes for ENDF-6
# 18: total fission cross section for neutrons
# 102: radiative capture


#extract data for every isotope (U-238, Pu-239, Pu-240)
U238_data = openmc.data.IncidentNeutron.from_hdf5("endf/U238.h5")
Pu239_data = openmc.data.IncidentNeutron.from_hdf5("endf/Pu239.h5")
Pu240_data = openmc.data.IncidentNeutron.from_hdf5("endf/Pu240.h5")

temperatures = U238_data.temperatures


for temperature in temperatures:
    energies = U238_data.energy[temperature]

    thermal_max_index = np.max(np.where(energies<0.1))
    fast_min_index = np.min(np.where(energies>1E5))

    U238_c = U238_data[102].xs[temperature](energies)
    Pu239_c = Pu239_data[102].xs[temperature](energies)
    Pu239_f = Pu239_data[18].xs[temperature](energies)
    Pu240_c = Pu240_data[102].xs[temperature](energies)
    Pu240_f = Pu240_data[18].xs[temperature](energies)


    mu = (U238_c - Pu239_c - Pu239_f)/(Pu239_c - Pu240_c - Pu240_f)
    delta = (U238_c + Pu240_f+ Pu240_c)/(Pu239_c + Pu239_f)

    num = U238_c - Pu239_c - Pu239_f
    den = Pu239_c - Pu240_c - Pu240_f

    c_1 = (num>0) & (den >0) #verde
    c_2 = (num>0) & (den <0) #rosso
    c_3 = (num<0) & (den >0) #rosso
    c_4 = (num<0) & (den <0) #blu

    #PLOT DELTA
    plt.loglog(energies, delta, 'r', linewidth=0.7)
    plt.grid(b=True, which='both', linewidth=0.4, ls='--')
    plt.title('\u03b4(E) for {}'.format(temperature))
    plt.xlabel('Energy [eV]')
    plt.ylabel('\u03b4(E)')
    plt.ylim(min(mu), max(mu))
    plt.savefig("images/delta/{}.png".format(temperature), dpi=700)
    plt.clf()

    #PLOT MU NUM DEN
    plt.loglog(energies, num, 'r', linewidth=0.7, label='Pu239 created (num)')
    plt.loglog(energies, den, 'b', linewidth=0.7, label='Pu240 created (den)')
    plt.legend()
    plt.grid(b=True, which='both', linewidth=0.4, ls='--')
    plt.title('\u03bc(E) num den for {}'.format(temperature))
    plt.yscale('symlog')
    plt.xlabel('Energy [eV]')
    plt.ylabel('\u03bc(E) num den')
    plt.ylim(min(mu), max(mu))
    plt.savefig("images/mu_num_den/{}.png".format(temperature), dpi=700)
    plt.clf()

    #PLOT MU
    plt.scatter(energies[c_1], mu[c_1], s=0.2, c='blue', label='create 239 / create 240 (+/+)')
    plt.scatter(energies[c_2], mu[c_2], s=0.2, c='red', label='create 239 / destroy 240 (+/-)')
    plt.scatter(energies[c_3], mu[c_3], s=0.2, c='green', label='destroy 239 / create 240 (-/+)')
    plt.scatter(energies[c_4], mu[c_4], s=0.2, c='orange', label='destroy 239 / destroy 240 (-/-)')
    lgnd = plt.legend()
    lgnd.legendHandles[0]._sizes = [30]
    lgnd.legendHandles[1]._sizes = [30]
    lgnd.legendHandles[2]._sizes = [30]
    lgnd.legendHandles[3]._sizes = [30]
    plt.xscale('log')
    plt.yscale('symlog')
    plt.grid(b=True, which='both', linewidth=0.4, ls='--')
    plt.title('\u03bc(E) for {}'.format(temperature))
    plt.xlabel('Energy [eV]')
    plt.ylabel('\u03bc(E)')
    plt.ylim(min(mu), max(mu))
    plt.savefig("images/mu/{}.png".format(temperature), dpi=700)
    plt.clf()
