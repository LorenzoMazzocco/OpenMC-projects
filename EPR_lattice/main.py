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
    axs[0].plot(np.linspace(-assembly_side/2,assembly_side/2,len(radial_data)),radial_data, 'r-', linewidth=2)
    axs[1].imshow(geom_image, alpha=alpha, origin='lower', extent=[-assembly_side/2,assembly_side/2,0,1.2*max(radial_data)])
    axs[1].plot(np.linspace(-assembly_side/2,assembly_side/2,len(radial_data)), radial_data,'r-', linewidth=3)
    axs[1].xaxis.tick_top()
    axs[1].xaxis.set_label_position('top')
    axs[1].set_xlabel('{}'.format(xlabel))
    axs[1].set_aspect('auto')
    for ax in axs:
        ax.set_ylabel('{}'.format(ylabel))

#==================================================== VARIABLES =======================

#fuel variables
No_BA_fuel_enrichment = 3.0
BA_fuel_enrichment = 0.25
BA_percentage = 8.0

#geometric variables
pin_fuel_or = 0.3975
pin_clad_ir = 0.4125
pin_clad_or = 0.4750

channel_clad_ir = 0.5725
channel_clad_or = 0.6125

pitch = 1.26
assembly_side = 17*pitch

#tally variables
mesh_dimension = 600
red_mesh_dimension = 300
energies_dimension = 500
red_energies_dimension = 10

#settings variables
neutrons_per_batch = 10000


#======================================================================= DEFINE MATERIALS =======================

# uranium dioxide BA
UO2_BA = openmc.Material(name='UO2_BA')
UO2_BA.add_element('U', 1.0, enrichment=BA_fuel_enrichment)
UO2_BA.add_element('O', 2.0)
UO2_BA.set_density('g/cc', 10.3070)

# uranium dioxide No_BA
fuel_No_BA = openmc.Material(name='fuel_No_BA')
fuel_No_BA.add_element('U', 1.0, enrichment=No_BA_fuel_enrichment)
fuel_No_BA.add_element('O', 2.0)
fuel_No_BA.set_density('g/cc', 10.3070)

# gadolinium oxide
Gd2O3 = openmc.Material(name='Gd2O3')
Gd2O3.add_element('Gd', 2.0)
Gd2O3.add_element('O', 3.0)
Gd2O3.set_density('g/cc', 7.41)

# cladding alloy (MT5)
MT5 = openmc.Material(name='MT5')
MT5.add_element('Zr', 0.775, percent_type='wo')
MT5.add_element('Nb', 0.1, percent_type='wo')
MT5.add_element('O', 0.125, percent_type='wo')
MT5.set_density('g/cc', 6.55)

# helium
He = openmc.Material(name='helium')
He.add_element('He',1.0)
He.set_density('g/cc', 0.00222185)

# water
H2O = openmc.Material(name='water')
H2O.add_element('H',2)
H2O.add_element('O',1)
H2O.set_density('g/cc', 1.0)
H2O.add_s_alpha_beta('c_H_in_H2O')

#MIXTURES
fuel_BA = openmc.Material.mix_materials([UO2_BA, Gd2O3], [0.92, 0.08], 'wo', name='fuel_BA')


#EXPORT
materials = openmc.Materials([UO2_BA, Gd2O3, MT5, He, H2O, fuel_BA, fuel_No_BA])
materials.export_to_xml()



#======================================================================= DEFINE GEOMETRY ====================================

#pin surfaces
pin_fuel_or = openmc.ZCylinder(r=pin_fuel_or)
pin_clad_ir = openmc.ZCylinder(r=pin_clad_ir)
pin_clad_or = openmc.ZCylinder(r=pin_clad_or)

#channel surfaces
channel_clad_or = openmc.ZCylinder(r=channel_clad_or)
channel_clad_ir = openmc.ZCylinder(r=channel_clad_ir)

#FUEL_BA PIN UNIVERSE
fuel_BA_cell = openmc.Cell(fill=fuel_BA, region=-pin_fuel_or)
gap_BA_cell = openmc.Cell(fill=He, region= +pin_fuel_or & -pin_clad_ir)
clad_BA_cell = openmc.Cell(fill=MT5, region= +pin_clad_ir & -pin_clad_or)
water_BA_cell = openmc.Cell(fill=H2O, region= +pin_clad_or)

b = openmc.Universe(cells=[fuel_BA_cell, gap_BA_cell, clad_BA_cell, water_BA_cell])

#FUEL_No_BA PIN UNIVERSE
fuel_No_BA_cell = openmc.Cell(fill=fuel_No_BA, region=-pin_fuel_or)
gap_No_BA_cell = openmc.Cell(fill=He, region= +pin_fuel_or & -pin_clad_ir)
clad_No_BA_cell = openmc.Cell(fill=MT5, region= +pin_clad_ir & -pin_clad_or)
water_No_BA_cell = openmc.Cell(fill=H2O, region= +pin_clad_or)

f = openmc.Universe(cells=[fuel_No_BA_cell, gap_No_BA_cell, clad_No_BA_cell, water_No_BA_cell])

#CHANNEL UNIVERSE
in_channel_cell = openmc.Cell(fill=H2O, region=-channel_clad_ir)
channel_clad_cell = openmc.Cell(fill=MT5, region= +channel_clad_ir & -channel_clad_or)
out_channel_cell = openmc.Cell(fill=H2O, region=+channel_clad_or)

c = openmc.Universe(cells=[in_channel_cell, channel_clad_cell, out_channel_cell])

#OUTER UNIVERSE
all_water_cell = openmc.Cell(fill=H2O)
outer_universe = openmc.Universe(cells=[all_water_cell])


#CREATE THE LATTICE

lattice = openmc.RectLattice()
lattice.lower_left = (-assembly_side/2, -assembly_side/2)
lattice.pitch = (pitch,pitch)
lattice.outer = outer_universe
lattice.universes= [[f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
                    [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
                    [f,f,b,f,f,c,f,f,c,f,f,c,f,f,b,f,f],
                    [f,f,f,c,f,f,f,b,f,b,f,f,f,c,f,f,f],
                    [f,f,f,f,b,f,f,f,f,f,f,f,b,f,f,f,f],
                    [f,f,c,f,f,c,f,f,c,f,f,c,f,f,c,f,f],
                    [f,f,f,f,f,f,b,f,f,f,b,f,f,f,f,f,f],
                    [f,f,f,b,f,f,f,f,f,f,f,f,f,b,f,f,f],
                    [f,f,c,f,f,c,f,f,c,f,f,c,f,f,c,f,f],
                    [f,f,f,b,f,f,f,f,f,f,f,f,f,b,f,f,f],
                    [f,f,f,f,f,f,b,f,f,f,b,f,f,f,f,f,f],
                    [f,f,c,f,f,c,f,f,c,f,f,c,f,f,c,f,f],
                    [f,f,f,f,b,f,f,f,f,f,f,f,b,f,f,f,f],
                    [f,f,f,c,f,f,f,b,f,b,f,f,f,c,f,f,f],
                    [f,f,b,f,f,c,f,f,c,f,f,c,f,f,b,f,f],
                    [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
                    [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f]]


#create geometry

#boundaries
left = openmc.XPlane(x0=-assembly_side/2, boundary_type='reflective')
right = openmc.XPlane(x0=assembly_side/2, boundary_type='reflective')
bottom = openmc.YPlane(y0=-assembly_side/2, boundary_type='reflective')
top = openmc.YPlane(y0=assembly_side/2, boundary_type='reflective')

main_cell = openmc.Cell(fill=lattice, region=+left & -right & +bottom & -top)
geometry = openmc.Geometry([main_cell])
geometry.export_to_xml()


#===================================================================================== PLOT GEOMETRY ===========================

#top view
geom_plot_top = openmc.Plot()
geom_plot_top.basis = 'xy'
geom_plot_top.origin = (0., 0., 0.)
geom_plot_top.width = (assembly_side, assembly_side)
geom_plot_top.pixels = (1500, 1500)
geom_plot_top.color_by = 'material'
geom_plot_top.colors = {fuel_No_BA: (255,255,153), fuel_BA:(255,153,255), He:'green', MT5:'grey', H2O:(102,178,255)}
geom_plot_top.filename = 'images/geometry/top_view'

#side view
geom_plot_side = openmc.Plot()
geom_plot_side.basis = 'xz'
geom_plot_side.origin = (0., 0., 0.)
geom_plot_side.width = (assembly_side, assembly_side)
geom_plot_side.pixels = (1500, 1500)
geom_plot_side.color_by = 'material'
geom_plot_side.colors = {fuel_No_BA: (255,255,153), fuel_BA:(255,153,255), He:'green', MT5:'grey', H2O:(102,178,255)}
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


#particle
particle_filter = openmc.ParticleFilter('neutron')

#mesh
mesh = openmc.RegularMesh()
mesh.dimension = [mesh_dimension, mesh_dimension]
mesh.lower_left = [-assembly_side/2, -assembly_side/2]
mesh.upper_right = [assembly_side/2, assembly_side/2]
mesh_filter = openmc.MeshFilter(mesh)


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
