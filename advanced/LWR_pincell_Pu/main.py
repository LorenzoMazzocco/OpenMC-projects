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
    pincell = EPR.pincell()

    bounds = [-pincell.pitch/2, -pincell.pitch/2, -1., pincell.pitch/2, pincell.pitch/2, 1.]

    #define the settings
    uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)

    settings = openmc.Settings()
    settings.source = openmc.source.Source(space=uniform_dist)
    settings.batches = 100
    settings.inactive = 20
    settings.particles = neutrons_per_batch
    settings.export_to_xml()

    return pincell, settings

pincell, settings = build_model()
geometry = pincell.geometry


############################################
#           DEPLETION SIMULATION           #
############################################

# Define depletion chain
chain = openmc.deplete.Chain.from_xml("simplified_pwr_depletion_chain.xml")

# Create operator for simulation
operator = openmc.deplete.Operator(geometry, settings, "simplified_pwr_depletion_chain.xml")

# Create integrator
power = pincell.linear_power
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
_time, U238 = results.get_atoms("1", "U238")


#remove first value
_time = _time[1:]
Pu238 = Pu238[1:]
Pu239 = Pu239[1:]
Pu240 = Pu240[1:]
U238 = U238[1:]

Pu_grade = Pu239/(Pu238+Pu239+Pu240) #plutonium grade (ao)

# convert time in burnup
MTHM = 3.14*(pincell.pin_fuel_or**2)*9.085/(1000*1000) #density of U 3%wt enr. is 9.085 in MTHM/cm
power_GW = power/1E9 #power of the pincell in MW/cm
burnup = (_time/(60*60*24))*(power_GW)/(MTHM) #burnup series in MWd/MTHM

export_a = np.asarray([burnup, Pu239, Pu240, U238])
np.savetxt("export_data.csv", export_a, delimiter=",")

# find burnup value for weapon grade threshold
burnup_threshold = burnup[np.amax(np.where(Pu_grade > 0.93))]

##################################################################
#                           PLOTTING                             #
##################################################################

# PLOT PLUTONIUM GRADE
fig = plt.figure(figsize=(8, 6))
ax1 = fig.add_subplot(111)
ax1.plot(burnup, Pu_grade*100, 'k', label='Isotopic composition')
ax1.set_xlabel('Burnup [GWd/MTHM]', fontsize=9)
ax1.set_ylabel('Isotopic Composition of Pu [% of Pu-239]')
ax1.set_xlim(min(burnup),max(burnup))
ax1.set_ylim(50,100)
ax1.grid(True, linestyle='--', linewidth=0.5, axis='both')
ax1.hlines(93, min(burnup), max(burnup), colors='r', linestyles='--', linewidth=0.7)
#sec x axis
ax2 = ax1.twiny()
ax2.set_xlabel("Time [weeks]\n", fontsize=9)
ax2.set_xlim(_time[0]/(60*60*24*7), _time[-1]/(60*60*24*7))
#sec yaxis
ax3 = ax1.twinx()
ax3.plot(burnup, 1000*(238*Pu238+239*Pu239+240*Pu240)/(6.022E23), 'k--', label='Total mass of plutonium')
ax3.set_ylabel("Mass of Pu [mg/cm]")
ax3.set_ylim(0,100)
#final details
ax1.axvspan(0,burnup_threshold, facecolor='red', alpha=0.2)
ax1.text(burnup_threshold/2, 75, 'WEAPON GRADE', color='red', alpha=0.6, fontsize=18, weight='bold', rotation='vertical', ha='center', va='center')
ax1.text(2*burnup[-1]/3, 93+2, 'Weapon grade threshold', fontsize=8, color='red', ha='center', va='top')
fig.legend(loc='lower right', bbox_to_anchor=(0.9, 0.2))
plt.savefig("images/plutonium_grade.png", dpi=700)
plt.clf()

#PLOT ISOTOPIC COMPOSITION

fig = plt.figure(figsize=(8, 6))
ax1 = fig.add_subplot(111)
ax1.plot(burnup, 1000*238*Pu238/(6.022E23))
ax1.plot(burnup, 1000*239*Pu239/(6.022E23))
ax1.plot(burnup, 1000*240*Pu240/(6.022E23))
ax1.set_xlabel('Burnup [GWd/MTHM]', fontsize=9)
ax1.set_ylabel('Mass of plutonium [mg/cm]')
ax1.set_xlim(min(burnup),max(burnup))
ax1.set_ylim(0,50)
ax1.grid(True, linestyle='--', linewidth=0.5, axis='both')
#sec x axis
ax2 = ax1.twiny()
ax2.set_xlabel("Time [weeks]\n", fontsize=9)
ax2.set_xlim(_time[0]/(60*60*24*7), _time[-1]/(60*60*24*7))
ax1.legend(['Pu-238','Pu-239','Pu-240'], bbox_to_anchor=(0.2, 0.9))
plt.savefig("images/isotopic_composition.png", dpi=700)
plt.clf()





##################################################################
#                        ORDER FOLDER                            #
##################################################################

shutil.move("materials.xml", "model_xml/materials.xml")
shutil.move("geometry.xml", "model_xml/geometry.xml")
shutil.move("settings.xml", "model_xml/settings.xml")
#shutil.move("plots.xml", "model_xml/plots.xml")
#shutil.move("tallies.xml", "model_xml/tallies.xml")

shutil.move("statepoint.100.h5", "output/statepoint.100.h5")
shutil.move("summary.h5", "output/summary.h5")
shutil.move("tallies.out", "output/tallies.out")
