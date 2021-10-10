from lib.Templates import EPR
from lib.PostProcessing import plots
import openmc.model
import openmc.lib

import numpy as np
import matplotlib.pyplot as plt
import math

import shutil
import sys



############################################
#                VARIABLES                 #
############################################

#model data
config = 20
complete_model=True

#settings
neutrons_per_batch=100000


############################################
#              BUILD MODEL                 #
############################################

def build_model():

    assembly = EPR.assembly(config=20, complete=complete_model)
    assembly.__init__(config=20, complete=complete_model)

    bounds = [0, 0, -1., 17*assembly.pitch/2, 17*assembly.pitch/2, 1.]

    #define the settings
    uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)

    settings = openmc.Settings()
    settings.source = openmc.source.Source(space=uniform_dist)
    settings.batches = 100
    settings.inactive = 20
    settings.particles = neutrons_per_batch
    settings.export_to_xml()

    return assembly

assembly = build_model()



############################################
#                 TALLIES                  #
############################################

# FILTERS
#particle
particle_filter = openmc.ParticleFilter('neutron')

#cell filters
fuel_cells_filter = openmc.DistribcellFilter(5)
BA_cells_filter = openmc.DistribcellFilter(1)


# TALLIES
tallies = openmc.Tallies()

#normalization tally
t_norm = openmc.Tally(name='normalization_tally')
t_norm.scores = ['fission-q-recoverable']
tallies.append(t_norm)

#power
t_fuel_power = openmc.Tally(name='fuel_power_tally')
t_fuel_power.filters = [fuel_cells_filter]
t_fuel_power.scores = ['fission-q-recoverable']
tallies.append(t_fuel_power)

t_BA_power = openmc.Tally(name='BA_power_tally')
t_BA_power.filters = [BA_cells_filter]
t_BA_power.scores = ['fission-q-recoverable']
tallies.append(t_BA_power)

#plutonium production
t_fuel_plutonium = openmc.Tally(name='fuel_plutonium_tally')
t_fuel_plutonium.filters = [fuel_cells_filter]
t_fuel_plutonium.nuclides = ['U238']
t_fuel_plutonium.scores = ['(n,gamma)']
tallies.append(t_fuel_plutonium)

t_BA_plutonium = openmc.Tally(name='BA_plutonium_tally')
t_BA_plutonium.filters = [BA_cells_filter]
t_BA_plutonium.nuclides = ['U238']
t_BA_plutonium.scores = ['(n,gamma)']
tallies.append(t_BA_plutonium)

tallies.export_to_xml()


############################################
#                RUN OPENMC                #
############################################
#openmc.run()


############################################
#              POST_PROCESSING             #
############################################

config = assembly.configurations["{}".format(config)]['lattice'].flatten()
config = np.reshape([universe.name for universe in config],(17,17))

sp = openmc.StatePoint('output/statepoint.100.h5')

#extract power data
fuel_power_tally = sp.get_tally(name='fuel_power_tally')
fuel_power_mean = fuel_power_tally.get_values(scores=['fission-q-recoverable'], value='mean')

BA_power_tally = sp.get_tally(name='BA_power_tally')
BA_power_mean = BA_power_tally.get_values(scores=['fission-q-recoverable'], value='mean')

#extract plutonium data
fuel_plutonium_tally = sp.get_tally(name='fuel_plutonium_tally')
fuel_plutonium_mean = fuel_plutonium_tally.get_values(scores=['(n,gamma)'], value='mean')

BA_plutonium_tally = sp.get_tally(name='BA_plutonium_tally')
BA_plutonium_mean = BA_plutonium_tally.get_values(scores=['(n,gamma)'], value='mean')

#normalize tallies
normalization_tally = sp.get_tally(name='normalization_tally')
H_eV = normalization_tally.get_values(scores=['fission-q-recoverable'])
H_J = H_eV * 1.602E-19 # 1eV = 1.602E-19J
norm_f = assembly.power/H_J # normalization factor [src/s]


#initialize data arrays
power_data = np.zeros(np.shape(config)[0]*np.shape(config)[1])
plutonium_data = np.zeros(np.shape(config)[0]*np.shape(config)[1])

#define mask to identify lattice structure
fuel_mask = config.flatten() == 'f'
BA_mask = config.flatten() == 'b'
C_mask = config.flatten() == 'c'

#place power data
np.place(power_data, fuel_mask, fuel_power_mean)
np.place(power_data, BA_mask, BA_power_mean)

#place plutonium data
np.place(plutonium_data, fuel_mask, fuel_plutonium_mean)
np.place(plutonium_data, BA_mask, BA_plutonium_mean)

power_data[power_data == 0] = float('nan')
plutonium_data[plutonium_data == 0] = float('nan')

power_data = np.reshape(power_data*norm_f*1.602E-19/420, np.shape(config)) #watt/cm
plutonium_data = np.reshape(plutonium_data*norm_f*239*(60*60)*1000/6.022E23, np.shape(config)) #mg/h


plots.lattice_plot(power_data, title='Rod Linear Power [W/cm]', filename='power', colormap='autumn')
plots.lattice_plot(plutonium_data, title='Pu-239 Production [mg/h]', filename='plutonium', colormap='plasma')



##################################################################
#                        ORDER FOLDER                            #
##################################################################

shutil.move("materials.xml", "model_xml/materials.xml")
shutil.move("geometry.xml", "model_xml/geometry.xml")
shutil.move("settings.xml", "model_xml/settings.xml")
#shutil.move("plots.xml", "model_xml/plots.xml")
shutil.move("tallies.xml", "model_xml/tallies.xml")

#shutil.move("statepoint.100.h5", "output/statepoint.100.h5")
shutil.move("summary.h5", "output/summary.h5")
shutil.move("tallies.out", "output/tallies.out")
