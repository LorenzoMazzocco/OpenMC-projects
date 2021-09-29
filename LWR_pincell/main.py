"""
Lo scopo di questo progetto è la simulazione 2D di una semplice pincell di un LWR.
Le informazioni da estrarre sono:
    - spettro di flusso neutronico totale (grafico flux/energy)
    - tasso di reazione fissione (plot 2D, grafico del tasso radiale sotto la geometria)
    - tasso di reazione cattura (plot 2D, grafico del tasso radiale sotto la geometria)
    - tasso di reazione scattering elastico (plot 2D, grafico del tasso radiale sotto la geometria)
    - energia media dei neutroni (plot 2D, grafico radiale)
"""

import openmc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

#================================================================ FUNCTIONS =============================

def plot_radially(radial_data, xlabel, ylabel, title, alpha=0.5):
    geom_image = mpimg.imread('images/geometry/side_view.ppm')
    fig, axs = plt.subplots(2,1, sharex=True,sharey=True, figsize=(15,10))
    fig.suptitle('{}'.format(title))
    axs[0].plot(np.linspace(-pitch/2,pitch/2,len(radial_data)),radial_data, 'r-', linewidth=2)
    axs[1].imshow(geom_image, alpha=alpha, origin='lower', extent=[-pitch/2,pitch/2,0,1.2*max(radial_data)])
    axs[1].plot(np.linspace(-pitch/2,pitch/2,len(radial_data)), radial_data,'r-', linewidth=3)
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
red_mesh_dimension = 300
energies_dimension = 500
red_energies_dimension = 10

neutrons_per_batch = 5000


#================================================================ DEFINE MATERIALS ===========================

#uranium_dioxide
UO2 = openmc.Material(1, "UO2")
UO2.add_element('U', 1.0, enrichment=U_enr)
UO2.add_element('O', 2.0)
UO2.set_density('g/cc', 10.97)

#helium
He = openmc.Material(2, "He")
He.add_element('He',1.0)
He.set_density('g/cc', 0.00222185)

#zirconium
Zr = openmc.Material(3, "Zr")
Zr.add_element('Zr', 1.0)
Zr.set_density('g/cc', 6.56)

#water
H2O = openmc.Material(4, "H2O")
H2O.add_element('H', 2.0)
H2O.add_element('O', 1.0)
H2O.set_density('g/cc', 1.0)
H2O.add_s_alpha_beta('c_H_in_H2O')

materials = openmc.Materials([UO2, He, Zr, H2O])
materials.export_to_xml()


#================================================================ DEFINE GEOMETRY ===========================

#surfaces
fuel_outer_radius = openmc.ZCylinder(r=r_fuel)
clad_inner_radius = openmc.ZCylinder(r=r_clad_in)
clad_outer_radius = openmc.ZCylinder(r=r_clad_out)

#boundaries
left = openmc.XPlane(x0=-pitch/2, boundary_type='reflective')
right = openmc.XPlane(x0=pitch/2, boundary_type='reflective')
bottom = openmc.YPlane(y0=-pitch/2, boundary_type='reflective')
top = openmc.YPlane(y0=pitch/2, boundary_type='reflective')


#regions
fuel_region = -fuel_outer_radius
gap_region = -clad_inner_radius & +fuel_outer_radius
clad_region = -clad_outer_radius & +clad_inner_radius
moderator_region = +clad_outer_radius & +left & -right & -top & +bottom


#cells
fuel = openmc.Cell(name='fuel')
fuel.fill = UO2
fuel.region = fuel_region

gap = openmc.Cell(name='gap')
gap.fill = He
gap.region = gap_region

clad = openmc.Cell(name='clad')
clad.fill = Zr
clad.region = clad_region

mod = openmc.Cell(name='mod')
mod.fill = H2O
mod.region = moderator_region


root_universe = openmc.Universe(cells=[fuel, gap, clad, mod])
geometry = openmc.Geometry()
geometry.root_universe = root_universe
geometry.export_to_xml()

#================================================================ PLOT GEOMETRY ===========================

#top view
geom_plot_top = openmc.Plot()
geom_plot_top.basis = 'xy'
geom_plot_top.origin = (0., 0., 0.)
geom_plot_top.width = (pitch, pitch)
geom_plot_top.pixels = (1500, 1500)
geom_plot_top.color_by = 'material'
geom_plot_top.colors = {mod: 'blue', fuel: 'yellow', gap:'green', clad:'grey'}
geom_plot_top.filename = 'images/geometry/top_view'

#side view
geom_plot_side = openmc.Plot()
geom_plot_side.basis = 'xz'
geom_plot_side.origin = (0., 0., 0.)
geom_plot_side.width = (pitch, pitch)
geom_plot_side.pixels = (400, 400)
geom_plot_side.color_by = 'material'
geom_plot_side.colors = {mod: 'blue', fuel: 'yellow', gap:'green', clad:'grey'}
geom_plot_side.filename = 'images/geometry/side_view'

plots = openmc.Plots([geom_plot_top, geom_plot_side])
plots.export_to_xml()
openmc.plot_geometry()


#================================================================ DEFINE SETTINGS ===========================

point = openmc.stats.Point((0, 0, 0))
source = openmc.Source(space=point)

settings = openmc.Settings()
settings.source = source
settings.batches = 100
settings.inactive = 20
settings.particles = neutrons_per_batch

settings.export_to_xml()


#================================================================ DEFINE TALLIES ===========================
#FILTERS
#energy
energies = np.logspace(np.log10(1e-3), np.log10(20.0e6), energies_dimension+1)
energy_filter = openmc.EnergyFilter(energies)

#reduced energy
reduced_energies = np.logspace(np.log10(1e-3), np.log10(20.0e6), red_energies_dimension+1)
reduced_energy_filter = openmc.EnergyFilter(reduced_energies)

#particle
particle_filter = openmc.ParticleFilter('neutron')

#mesh
mesh = openmc.RegularMesh()
mesh.dimension = [mesh_dimension, mesh_dimension]
mesh.lower_left = [-pitch/2, -pitch/2]
mesh.upper_right = [pitch/2, pitch/2]
mesh_filter = openmc.MeshFilter(mesh)

#reduced mesh
reduced_mesh = openmc.RegularMesh()
reduced_mesh.dimension = [red_mesh_dimension, red_mesh_dimension]
reduced_mesh.lower_left = [-pitch/2, -pitch/2]
reduced_mesh.upper_right = [pitch/2, pitch/2]
reduced_mesh_filter = openmc.MeshFilter(reduced_mesh)

#TALLIES
tallies = openmc.Tallies()

#total flux spectrum
t_tot_flux_spec = openmc.Tally(name='total_flux')
t_tot_flux_spec.filters = [energy_filter, particle_filter]
t_tot_flux_spec.scores = ['flux']
tallies.append(t_tot_flux_spec)

#mesh tally (fission, capture, scattering RR)
t_mesh = openmc.Tally(name='mesh_tally')
t_mesh.filters = [mesh_filter]
t_mesh.scores = ['fission', '(n,gamma)', 'elastic', 'fission-q-recoverable']
tallies.append(t_mesh)


t_flux_ene = openmc.Tally(name='tally_flux_ene')
t_flux_ene.filters = [reduced_mesh_filter,reduced_energy_filter]
t_flux_ene.scores = ['flux']
tallies.append(t_flux_ene)

tallies.export_to_xml()

#================================================================ RUN SIMULATION ===========================
openmc.run()

#================================================================ POST PROCESSING ===========================

print('\n\nOpening StatePoint file...')
sp = openmc.StatePoint('statepoint.100.h5')

print('\nPostprocessing started!')

#total flux spectrum
tally_tot_flux = sp.get_tally(name='total_flux')
energy_diff = np.diff(energies)

plt.loglog(energies[:-1], tally_tot_flux.mean[:,0,0])
plt.xlabel('Energy [eV]')
plt.ylabel('E*Phi(E) [arbitrary units]')
plt.grid()
plt.savefig("images/plots/flux_spectrum.png", dpi=700)
plt.clf()


tally_mesh = sp.get_tally(name='mesh_tally')
#fission reaction rate
fission_rr = tally_mesh.get_slice(scores=['fission'])
fission_rr.mean.shape = (mesh_dimension,mesh_dimension)

plt.imshow(fission_rr.mean, cmap='jet')
plt.title('Fission Reaction Rate [reaction/s]\nmesh_dim: {} -- neutrons/batch: {}'.format(mesh_dimension,neutrons_per_batch), pad=10)
plt.colorbar()
plt.savefig("images/plots/fission_RR.png", dpi=700)
plt.clf()

#scattering reaction rate
elastic_rr = tally_mesh.get_slice(scores=['(n,elastic)'])
elastic_rr.mean.shape = (mesh_dimension,mesh_dimension)

plt.imshow(elastic_rr.mean, cmap='jet')
plt.title('Elastic Scattering Reaction Rate [reaction/s]\nmesh_dim: {} -- neutrons/batch: {}'.format(mesh_dimension,neutrons_per_batch), pad=10)
plt.colorbar()
plt.savefig("images/plots/elastic_RR.png", dpi=700)
plt.clf()

#capture reaction rate
capture_rr = tally_mesh.get_slice(scores=['(n,gamma)'])
capture_rr.mean.shape = (mesh_dimension,mesh_dimension)

plt.imshow(capture_rr.mean, cmap='jet')
plt.title('Radiative Capture Reaction Rate [reaction/s]\nmesh_dim: {} -- neutrons/batch: {}'.format(mesh_dimension,neutrons_per_batch), pad=10)
plt.colorbar()
plt.savefig("images/plots/capture_RR.png", dpi=700)
plt.clf()

#recoverable energy
rec_ene = tally_mesh.get_slice(scores=['fission-q-recoverable'])
rec_ene.mean.shape = (mesh_dimension,mesh_dimension)

plt.imshow(rec_ene.mean, cmap='jet')
plt.title('Recoverable energy [ev/src]\nmesh_dim: {} -- neutrons/batch: {}'.format(mesh_dimension,neutrons_per_batch), pad=10)
plt.colorbar()
plt.savefig("images/plots/recoverable_energy.png", dpi=700)
plt.clf()

print('\nTop plots completed...')

#RADIAL
radial_index=int((mesh_dimension/2)-1)
radial_fission = fission_rr.mean[radial_index,:]
radial_capture = capture_rr.mean[radial_index,:]
radial_elastic = elastic_rr.mean[radial_index,:]
radial_recene = rec_ene.mean[radial_index,:]


plot_radially(radial_fission, title='Radial distribution of fission reaction rate\nmesh_dim: {} -- neutrons/batch: {}'.format(mesh_dimension,neutrons_per_batch), xlabel='Radial Distance [cm]', ylabel='Fission reaction rate [1/s-src]')
plt.savefig("images/radial_plots/fission_rr.png", dpi=700)
plt.clf()


plot_radially(radial_capture, title='Radial distribution of (n,gamma) reaction rate\nmesh_dim: {} -- neutrons/batch: {}'.format(mesh_dimension,neutrons_per_batch), xlabel='Radial Distance [cm]', ylabel='(n,gamma) reaction rate [1/s-src]')
plt.savefig("images/radial_plots/capture_rr.png", dpi=700)
plt.clf()


plot_radially(radial_elastic, title='Radial distribution of elastic scattering reaction rate\nmesh_dim: {} -- neutrons/batch: {}'.format(mesh_dimension,neutrons_per_batch), xlabel='Radial Distance [cm]', ylabel='Elastic Scattering reaction rate [1/s-src]')
plt.savefig("images/radial_plots/elastic_rr.png", dpi=700)
plt.clf()

plot_radially(radial_recene, title='Radial distribution of recoverable energy\nmesh_dim: {} -- neutrons/batch: {}'.format(mesh_dimension,neutrons_per_batch), xlabel='Radial Distance [cm]', ylabel='Recoverable energy [eV/src]')
plt.savefig("images/radial_plots/recoverable_energy.png", dpi=700)
plt.clf()

print('\nRadial plots completed...')

#mean neutron energy mesh
tally_flux_ene = sp.get_tally(name='tally_flux_ene')
df = tally_flux_ene.get_pandas_dataframe()

mean_energy_mesh = np.zeros((red_mesh_dimension,red_mesh_dimension))

for i in range(red_mesh_dimension):
    for j in range(red_mesh_dimension):
        crit_pos = (df['mesh 2']['x'] == i+1) & (df['mesh 2']['y'] == j+1)
        energy_low = df.loc[crit_pos, 'energy low [eV]']
        energy_high = df.loc[crit_pos, 'energy high [eV]']
        energy_mid = (energy_low + energy_high)/2
        flux = df.loc[crit_pos, 'mean']
        flux = flux/np.diff(reduced_energies)
        mean_energy_mesh[i,j] = flux.dot(energy_mid)/flux.sum()
        print('Processing mean neutron energy mesh \t\t Done ({}/{},{})'.format(i,red_mesh_dimension,j))

np.savetxt("mean_energy_mesh.csv", mean_energy_mesh, delimiter=",")

mean_energy_mesh = np.genfromtxt('mean_energy_mesh.csv', delimiter=',')

plt.imshow(mean_energy_mesh, cmap='jet')
plt.title('Mean neutron energy [eV]\nmesh_dim: {} -- neutrons/batch: {}'.format(red_mesh_dimension,neutrons_per_batch), pad=10)
plt.colorbar()
plt.savefig("images/plots/mean_neutron_energy.png", dpi=700)
plt.clf()

radial_index=int((red_mesh_dimension/2)-1)
plot_radially(mean_energy_mesh[radial_index,:], title='Mean neutron energy [eV]\nmesh_dim: {} -- neutrons/batch: {}'.format(red_mesh_dimension,neutrons_per_batch), xlabel='Radial Distance [cm]', ylabel='Mean neutron energy [eV]')
plt.savefig("images/radial_plots/mean_neutron_energy.png", dpi=700)
plt.clf()
