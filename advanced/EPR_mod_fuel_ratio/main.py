from templates import EPR_assembly as templates
import openmc.model
import openmc.lib

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

import shutil
import sys



#####################################
#              VARIABLES            #
#####################################

lower_limit = 0.1
upper_limit = 1.26/2
n = 30

# Check the run mode by parsing
# the command line arguments:
#                       None: postprocessing only
#                       -r: run simulations

if (len(sys.argv) == 2) and (sys.argv[1] == '-r'):
    run_simulation = True
else:
    run_simulation = False



#####################################
#       MODEL BUILDING FUNCTION     #
#####################################

def build_model(fuel_or):

    assembly = templates.EPR_assembly()
    assembly.set_fuel_or(fuel_or)
    assembly.__init__()

    print('======================================================ASSEMBLY DATA ==================================================')
    print('Assembly fuel or: {}'.format(assembly.pin_fuel_or))
    print('Assembly clad ir: {}'.format(assembly.pin_clad_ir))
    print('Assembly clad or: {}'.format(assembly.pin_clad_or))


    bounds = [0, 0, -1., 17*assembly.pitch/2, 17*assembly.pitch/2, 1.]

    #define the settings
    uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)

    settings = openmc.Settings()
    settings.source = openmc.source.Source(space=uniform_dist)
    settings.batches = 100
    settings.inactive = 20
    settings.particles = 1000
    settings.output = {'tallies': False, 'summary':False, 'path':'output/'}
    settings.vebosity = 1
    settings.export_to_xml()




#####################################
#      ITERATION OF SIMULATIONS     #
#####################################

# create the search space for the parameter
radiuses = np.linspace(lower_limit, upper_limit, n)
data = []

#iteration over the search space
if run_simulation:
    for i, radius in enumerate(radiuses):
        print('Computing {}/{}'.format(i,n))
        build_model(radius)
        openmc.lib.init()
        openmc.lib.run()
        data.append(openmc.lib.keff())
        openmc.lib.finalize()
        np.savetxt("output/data.csv", data, delimiter=",")
    #order the main folder moving xml files
    shutil.move("materials.xml", "model_xml/materials.xml")
    shutil.move("geometry.xml", "model_xml/geometry.xml")
    shutil.move("settings.xml", "model_xml/settings.xml")




#####################################
#            POST-PROCESSING        #
#####################################

data = np.genfromtxt('output/data.csv', delimiter=',')
k_effs = data[:,0]
std_devs = data[:,1]

#compute the V_m/V_f ratio (h=1)
V_fs = 3.14*np.square(radiuses)
V_ms = 1.26**2 - V_fs
ratios = V_ms/V_fs

# interpolate the data to get spline
cs = interpolate.CubicSpline(radiuses,k_effs)
radiuses_new = np.linspace(lower_limit, upper_limit, 100)

# create plot
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(radiuses_new, cs(radiuses_new), 'k')
ax1.plot(radiuses, k_effs, 'sr', markersize=4)
ax1.set_xlabel('Fuel pellet radius [cm]', fontsize=9)
ax1.set_ylabel('k-inf')
ax1.grid(True, linestyle='--', linewidth=0.5, axis='y')
ax1.hlines(1, min(radiuses), max(radiuses), colors='r', linestyles='--', linewidth=0.7, label='k-inf = 1')
#sec axis
ax2 = ax1.twiny()
ax2.set_xlabel("Moderator-to-fuel ratio [Vm/Vf]\n", fontsize=9)
ax2.set_xlim(ratios[0], ratios[-1])
ax2.set_xticks([45,40,35,30,25,20,15,10,5])
ax2.grid(True, linestyle='--', linewidth=0.5)
plt.savefig("results.png", dpi=700)
plt.clf()
