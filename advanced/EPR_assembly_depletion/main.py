import openmc
import openmc.deplete

from lib.Templates import EPR
from lib.PostProcessing import plots

import numpy as np
import matplotlib.pyplot as plt

import shutil


############################################
#                VARIABLES                 #
############################################

neutrons_per_batch = 1000



############################################
#               BUILD MODEL                #
############################################

def build_model():
    assembly = EPR.assembly()

    bounds = [-assembly.side_dimension/2, -assembly.side_dimension/2, -1., assembly.side_dimension/2, assembly.side_dimension/2, 1.]

    #define the settings
    uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)

    settings = openmc.Settings()
    settings.source = openmc.source.Source(space=uniform_dist)
    settings.batches = 100
    settings.inactive = 20
    settings.particles = neutrons_per_batch
    settings.export_to_xml()

    return assembly, settings

assembly, settings = build_model()
geometry = assembly.geometry


############################################
#                 TALLIES                  #
############################################

# I want to tally:
#               - neutron flux
#               - total flux spectrum
#               - fission rr
#               - capture rr
#               -





############################################
#           DEPLETION SIMULATION           #
############################################

# Define depletion chain
chain = openmc.deplete.Chain.from_xml("simplified_pwr_depletion_chain.xml")

# Create operator for simulation
operator = openmc.deplete.Operator(geometry, settings, "simplified_pwr_depletion_chain.xml", diff_burnable_mats=True)

# Create integrator
power = assembly.power
time_steps = np.append([24*60*60]*30, [7*24*60*60] * 100) #step_size is 1w for 104 week total. First month every day.
integrator = openmc.deplete.PredictorIntegrator(operator, time_steps, power)

# Perform SIMULATION
#integrator.integrate()



############################################
#              POST PROCESSING             #
############################################

results = openmc.deplete.ResultsList.from_hdf5("depletion_results.h5")

# retrieve plutonium data
_time, Pu238 = results.get_atoms("1", "Pu238")
_time, Pu239 = results.get_atoms("1", "Pu239")
_time, Pu240 = results.get_atoms("1", "Pu240")


#remove first value
_time = _time[1:]
Pu238 = Pu238[1:]
Pu239 = Pu239[1:]
Pu240 = Pu240[1:]

Pu_grade = Pu239/(Pu238+Pu239+Pu240) #plutonium grade (ao)

# convert time in burnup
MTHM = operator.heavy_metal
power_GW = power/1E9 #power of the assembly in GW
burnup = (_time/(60*60*24))*(power_GW)/(MTHM) #burnup series in GWd/MTHM

# find burnup value for weapon grade threshold
burnup_threshold = burnup[np.amax(np.where(Pu_grade > 0.93))]

##################################################################
#                           PLOTTING                             #
##################################################################





##################################################################
#                        ORDER FOLDER                            #
##################################################################

shutil.move("materials.xml", "model_xml/materials.xml")
shutil.move("geometry.xml", "model_xml/geometry.xml")
shutil.move("settings.xml", "model_xml/settings.xml")
#shutil.move("plots.xml", "model_xml/plots.xml")
shutil.move("tallies.xml", "model_xml/tallies.xml")

shutil.move("summary.h5", "output/summary.h5")
shutil.move("tallies.out", "output/tallies.out")
