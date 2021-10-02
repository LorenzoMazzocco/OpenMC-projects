import openmc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

#=========================FUNCTIONS=============================

def plot_radially(radial_data, xlabel, ylabel, title, alpha=0.5):
    geom_image = mpimg.imread('images/geometry/side_view.ppm')
    fig, axs = plt.subplots(2,1, sharex=True, figsize=(15,10))
    fig.suptitle('{}'.format(title))
    axs[0].plot(np.linspace(-pitch/2,pitch/2,red_mesh_dimension),radial_data, 'r-', linewidth=2)
    axs[1].imshow(geom_image, alpha=alpha, origin='lower', extent=[-pitch/2,pitch/2,0,1.2*np.amax(radial_data)])
    axs[1].plot(np.linspace(-pitch/2,pitch/2,red_mesh_dimension), radial_data,'r-', linewidth=3)
    axs[1].xaxis.tick_top()
    axs[1].xaxis.set_label_position('top')
    axs[1].set_xlabel('{}'.format(xlabel))
    axs[1].set_aspect('auto')
    for ax in axs:
        ax.set_ylabel('{}'.format(ylabel))

U_enr = 5.0
r_fuel = 0.39
r_clad_in = 0.40
r_clad_out = 0.46
pitch = 1.26
mesh_dimension = 300
red_mesh_dimension = 100
energies_dimension = 200

reduced_energies = np.logspace(np.log10(1e-3), np.log10(20.0e6), 201)
energies_diff = np.diff(reduced_energies)

sp = openmc.StatePoint('statepoint.90.h5')

tally_flux_ene = sp.get_tally(name='tally_flux_ene')
df = tally_flux_ene.get_pandas_dataframe()
pd.options.display.float_format = '{:.2e}'.format



mean_energy_mesh = np.zeros((red_mesh_dimension,red_mesh_dimension))

for i in range(red_mesh_dimension):
    for j in range(red_mesh_dimension):
        crit_pos = (df['mesh 2']['x'] == i) & (df['mesh 2']['y'] == j)
        energy_low = df.loc[crit_pos, 'energy low [eV]']
        energy_high = df.loc[crit_pos, 'energy high [eV]']
        energy_mid = (energy_low + energy_high)/2
        flux = df.loc[crit_pos, 'mean']
        if np.shape(flux)[0] == energies_dimension:
            flux = flux/energies_diff
            mean_energy_mesh[i,j] = flux.dot(energy_mid)/flux.sum()
        else:
            mean_energy_mesh[i,j] = math.nan

        print('Processing mean neutron energy mesh --- Done ({}/{},{}). SHAPE: {}'.format(i,red_mesh_dimension,j,np.shape(flux)))

np.savetxt("mean_energy_mesh.csv", mean_energy_mesh, delimiter=",")

mean_energy_mesh = np.nan_to_num(np.genfromtxt('mean_energy_mesh.csv', delimiter=','))

plt.imshow(mean_energy_mesh, cmap='jet')
plt.title('Mean neutron energy [eV]', pad=20)
plt.colorbar()
plt.savefig("images/plots/mean_neutron_energy.png", dpi=700)
plt.clf()

radial_index=int((red_mesh_dimension/2)-1)
plot_radially(mean_energy_mesh[radial_index,:], title='Mean neutron energy [eV]', xlabel='Radial Distance [cm]', ylabel='Mean neutron energy [eV]')
plt.savefig("images/radial_plots/mean_neutron_energy.png", dpi=700)
plt.clf()
