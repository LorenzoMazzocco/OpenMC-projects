import models
import openmc.model
import numpy as np
import matplotlib.pyplot as plt

complete=False
lower_limit = 2*(0.4750-0.2)
upper_limit = 4
n = 40

def build_model(pitch):

    #create the materials and geometry files
    assembly = models.EPR_assembly(config=20, complete=complete)
    assembly.set_pitch(pitch)
    assembly.__init__(config=20,complete=False)

    if complete:
        bounds = [-17*assembly.pitch/2, -17*assembly.pitch/2, -1., 17*assembly.pitch/2, 17*assembly.pitch/2, 1.]
    else:
        bounds = [0, 0, -1., 17*assembly.pitch/2, 17*assembly.pitch/2, 1.]

    #define the settings
    uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)

    settings = openmc.Settings()
    settings.source = openmc.source.Source(space=uniform_dist)
    settings.batches = 100
    settings.inactive = 20
    settings.particles = 1000
    settings.output = {'tallies': False}
    settings.vebosity = 1
    settings.export_to_xml()

    model = openmc.model.Model(assembly.geometry, assembly.materials, settings)
    return model


#perform exploration

pitches = np.linspace(lower_limit, upper_limit, n)
keffs = []


for i, pitch in enumerate(pitches):
    print('{} - Computing for pitch: {} cm'.format(i,pitch))
    model = build_model(pitch)
    openmc.run()
    keffs.append(openmc.StatePoint('statepoint.100.h5').k_generation[-1])
    np.savetxt("results.csv", keffs, delimiter=",")



plt.figure(figsize=(8, 4.5))
plt.title('Eigenvalue versus Pitch')
# Create a scatter plot using the mean value of keff
plt.plot(pitches, keffs)
plt.xlabel('Pitch [cm]')
plt.ylabel('Eigenvalue')
plt.savefig("lol.png", dpi=700)
plt.clf()
