import openmc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import shutil

##################################################################
#                           FUNCTIONS                            #
##################################################################

def mesh_plot(mesh_data,title,filename, reduced=False):
    if reduced:
        mesh_dim=red_mesh_dimension
    else:
        mesh_dim=mesh_dimension
    plt.imshow(mesh_data, cmap='coolwarm', origin='lower', extent = [-assembly_side/2,assembly_side/2,-assembly_side/2,assembly_side/2])
    plt.suptitle(title,fontsize=14)
    plt.title('mesh size: [{},{}]   |   neutrons/batch: {}'.format(mesh_dim,mesh_dim,neutrons_per_batch),fontsize=10)
    plt.xlabel('Distance from center [cm]')
    plt.ylabel('Distance from center [cm]')
    plt.colorbar()
    plt.savefig("images/{}/plots/{}.png".format(configuration['name'], filename), dpi=700)
    plt.clf()


def plot_radially(radial_data, ylabel, title,filename, alpha=0.5, diag=False):
    if diag:
        geom_image = mpimg.imread('images/{}/geometry/side_view_diag.ppm'.format(configuration['name']))
        directory = 'diagonal'
        assembly_dim = math.sqrt(2)*assembly_side
    else:
        geom_image = mpimg.imread('images/{}/geometry/side_view_partial.ppm'.format(configuration['name']))
        directory = 'horizontal'
        assembly_dim = assembly_side
    fig, axs = plt.subplots(2,1, sharex=True,sharey=True, figsize=(15,10))
    fig.suptitle('{}'.format(title), fontsize=19)
    axs[0].set_title('mesh size: [{},{}]   |   neutrons/batch: {}'.format(mesh_dimension,mesh_dimension,neutrons_per_batch),fontsize=14, pad=30)
    axs[0].plot(np.linspace(0,assembly_dim/2,len(radial_data)),radial_data, 'r-', linewidth=1.5)
    axs[1].imshow(geom_image, alpha=alpha, origin='lower', extent=[0,assembly_dim/2,0,1.2*max(radial_data)])
    axs[1].plot(np.linspace(0,assembly_dim/2,len(radial_data)), radial_data,'r-', linewidth=1.5)
    axs[1].xaxis.tick_top()
    axs[1].xaxis.set_label_position('top')
    axs[1].set_xlabel('Radial distance from center [cm]')
    axs[1].set_aspect('auto')
    for ax in axs:
        ax.set_ylabel('{}'.format(ylabel))
    plt.savefig("images/{}/radial_plots/{}/{}.png".format(configuration['name'],directory,filename), dpi=700)
    plt.clf()



def reconstruct_complete_mesh(up_right):
    down_right = np.flip(up_right,1)
    up_left = np.flip(up_right,0)
    down_left = np.flip(up_left,1)
    complete = np.block([
                        [down_left,up_left],
                        [down_right,up_right]])
    return complete



##################################################################
#                         MAIN VARIABLES                         #
##################################################################

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
mesh_dimension = 300
red_mesh_dimension = 300
energies_dimension = 500
red_energies_dimension = 10

#settings variables
neutrons_per_batch = 15000


##################################################################
#                      DEFINE MATERIALS                          #
##################################################################

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



##################################################################
#                       DEFINE GEOMETRY                          #
##################################################################

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

#==================================================== CONFIGURATIONS =======================

config_20 = {'lattice':
            [[f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
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
            [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f]],
            'name': 'config_20_BA'}

config_16 = {'lattice':
            [[f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,b,f,f,c,f,f,c,f,f,c,f,f,b,f,f],
            [f,f,f,c,f,f,f,b,f,b,f,f,f,c,f,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,c,f,f,c,f,f,c,f,f,c,f,f,c,f,f],
            [f,f,f,f,f,f,b,f,f,f,b,f,f,f,f,f,f],
            [f,f,f,b,f,f,f,f,f,f,f,f,f,b,f,f,f],
            [f,f,c,f,f,c,f,f,c,f,f,c,f,f,c,f,f],
            [f,f,f,b,f,f,f,f,f,f,f,f,f,b,f,f,f],
            [f,f,f,f,f,f,b,f,f,f,b,f,f,f,f,f,f],
            [f,f,c,f,f,c,f,f,c,f,f,c,f,f,c,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,f,c,f,f,f,b,f,b,f,f,f,c,f,f,f],
            [f,f,b,f,f,c,f,f,c,f,f,c,f,f,b,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f]],
            'name': 'config_16_BA'}

config_12 = {'lattice':
            [[f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,b,f,f,c,f,f,c,f,f,c,f,f,b,f,f],
            [f,f,f,c,f,f,f,f,f,f,f,f,f,c,f,f,f],
            [f,f,f,f,f,f,b,f,f,f,b,f,f,f,f,f,f],
            [f,f,c,f,f,c,f,f,c,f,f,c,f,f,c,f,f],
            [f,f,f,f,b,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,b,f,f,f],
            [f,f,c,f,f,c,f,f,c,f,f,c,f,f,c,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,b,f,f,f],
            [f,f,f,f,b,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,c,f,f,c,f,f,c,f,f,c,f,f,c,f,f],
            [f,f,f,f,f,f,b,f,f,f,b,f,f,f,f,f,f],
            [f,f,f,c,f,f,f,f,f,f,f,f,f,c,f,f,f],
            [f,f,b,f,f,c,f,f,c,f,f,c,f,f,b,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f]],
            'name': 'config_12_BA'}

config_8 = {'lattice':
            [[f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,f,f,f,c,f,f,c,f,f,c,f,f,f,f,f],
            [f,f,f,c,f,f,f,f,f,f,f,f,f,c,f,f,f],
            [f,f,f,f,f,f,b,f,f,f,b,f,f,f,f,f,f],
            [f,f,c,f,f,c,f,f,c,f,f,c,f,f,c,f,f],
            [f,f,f,f,b,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,b,f,f,f],
            [f,f,c,f,f,c,f,f,c,f,f,c,f,f,c,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,b,f,f,f],
            [f,f,f,f,b,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,c,f,f,c,f,f,c,f,f,c,f,f,c,f,f],
            [f,f,f,f,f,f,b,f,f,f,b,f,f,f,f,f,f],
            [f,f,f,c,f,f,f,f,f,f,f,f,f,c,f,f,f],
            [f,f,f,f,f,c,f,f,c,f,f,c,f,f,f,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f],
            [f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f]],
            'name': 'config_8_BA'}

configuration = config_20

#CREATE THE LATTICE

lattice = openmc.RectLattice()
lattice.lower_left = (-assembly_side/2, -assembly_side/2)
lattice.pitch = (pitch,pitch)
lattice.outer = outer_universe
lattice.universes= configuration['lattice']


#===================================COMPLETE GEOMETRY

#boundaries
left = openmc.XPlane(x0=-assembly_side/2, boundary_type='reflective')
right = openmc.XPlane(x0=assembly_side/2, boundary_type='reflective')
bottom = openmc.YPlane(y0=-assembly_side/2, boundary_type='reflective')
top = openmc.YPlane(y0=assembly_side/2, boundary_type='reflective')

main_cell = openmc.Cell(fill=lattice, region=+left & -right & +bottom & -top)
geometry = openmc.Geometry([main_cell])
geometry.export_to_xml()

#top view
geom_plot_top = openmc.Plot()
geom_plot_top.basis = 'xy'
geom_plot_top.origin = (0., 0., 0.)
geom_plot_top.width = (assembly_side, assembly_side)
geom_plot_top.pixels = (1500, 1500)
geom_plot_top.color_by = 'material'
geom_plot_top.colors = {fuel_No_BA: (255,255,153), fuel_BA:(255,153,255), He:'green', MT5:'grey', H2O:(102,178,255)}
geom_plot_top.filename = 'images/{}/geometry/top_view_complete'.format(configuration['name'])

#side view
geom_plot_side = openmc.Plot()
geom_plot_side.basis = 'xz'
geom_plot_side.origin = (0., 0., 0.)
geom_plot_side.width = (assembly_side, assembly_side)
geom_plot_side.pixels = (1500, 1500)
geom_plot_side.color_by = 'material'
geom_plot_side.colors = {fuel_No_BA: (255,255,153), fuel_BA:(255,153,255), He:'green', MT5:'grey', H2O:(102,178,255)}
geom_plot_side.filename = 'images/{}/geometry/side_view_complete'.format(configuration['name'])

plots = openmc.Plots([geom_plot_top, geom_plot_side])
plots.export_to_xml()
openmc.plot_geometry()

#===================================DIAGONAL PARTIAL GEOMETRY

pitch_diag = math.sqrt(2)*pitch
lattice_diag = openmc.RectLattice()
lattice_diag.lower_left = (-math.sqrt(2)*assembly_side/2, -pitch/2)
lattice_diag.pitch = (pitch_diag,pitch)
lattice_diag.outer = outer_universe
d = np.diag(lattice.universes)
lattice_diag.universes = np.block([[d],[d],[d]])

left = openmc.XPlane(x0=-17*pitch_diag/2, boundary_type='reflective')
right = openmc.XPlane(x0=17*pitch_diag/2, boundary_type='reflective')
bottom = openmc.YPlane(y0=-1.5*pitch, boundary_type='reflective')
top = openmc.YPlane(y0=1.5*pitch, boundary_type='reflective')

main_cell = openmc.Cell(fill=lattice_diag, region=+left & -right & +bottom & -top)
geometry = openmc.Geometry([main_cell])
geometry.export_to_xml()

#side view diag (partial)
geom_plot_side = openmc.Plot()
geom_plot_side.basis = 'xz'
geom_plot_side.origin = (17*pitch_diag/4, 0., 0.)
geom_plot_side.width = (17*pitch_diag/2, 3*pitch)
geom_plot_side.pixels = (1500, 1500)
geom_plot_side.color_by = 'material'
geom_plot_side.colors = {fuel_No_BA: (255,255,153), fuel_BA:(255,153,255), He:'green', MT5:'grey', H2O:(102,178,255)}
geom_plot_side.filename = 'images/{}/geometry/side_view_diag'.format(configuration['name'])

plots = openmc.Plots([geom_plot_side])
plots.export_to_xml()
openmc.plot_geometry()

#===================================PARTIAL GEOMETRY

#boundaries
left = openmc.XPlane(x0=0, boundary_type='reflective')
right = openmc.XPlane(x0=assembly_side/2, boundary_type='reflective')
bottom = openmc.YPlane(y0=0, boundary_type='reflective')
top = openmc.YPlane(y0=assembly_side/2, boundary_type='reflective')

main_cell = openmc.Cell(fill=lattice, region=+left & -right & +bottom & -top)
geometry = openmc.Geometry([main_cell])
geometry.export_to_xml()

#top view
geom_plot_top = openmc.Plot()
geom_plot_top.basis = 'xy'
geom_plot_top.origin = (assembly_side/4, assembly_side/4, 0.)
geom_plot_top.width = (assembly_side/2, assembly_side/2)
geom_plot_top.pixels = (1500, 1500)
geom_plot_top.color_by = 'material'
geom_plot_top.colors = {fuel_No_BA: (255,255,153), fuel_BA:(255,153,255), He:'green', MT5:'grey', H2O:(102,178,255)}
geom_plot_top.filename = 'images/{}/geometry/top_view_partial'.format(configuration['name'])

#side view
geom_plot_side = openmc.Plot()
geom_plot_side.basis = 'xz'
geom_plot_side.origin = (assembly_side/4, 0, 0.)
geom_plot_side.width = (assembly_side/2, assembly_side/2)
geom_plot_side.pixels = (1500, 1500)
geom_plot_side.color_by = 'material'
geom_plot_side.colors = {fuel_No_BA: (255,255,153), fuel_BA:(255,153,255), He:'green', MT5:'grey', H2O:(102,178,255)}
geom_plot_side.filename = 'images/{}/geometry/side_view_partial'.format(configuration['name'])

plots = openmc.Plots([geom_plot_top, geom_plot_side])
plots.export_to_xml()
openmc.plot_geometry()




##################################################################
#                         DEFINE SETTINGS                        #
##################################################################

point = openmc.stats.Point((assembly_side/4, assembly_side/4, 0))
source = openmc.Source(space=point)

settings = openmc.Settings()
settings.source = source
settings.batches = 100
settings.inactive = 20
settings.particles = neutrons_per_batch
settings.verbosity = 7

settings.export_to_xml()


##################################################################
#                         DEFINE TALLIES                         #
##################################################################

#FILTERS
#energy
energies = np.logspace(np.log10(1e-3), np.log10(20.0e6), energies_dimension+1)
energy_filter = openmc.EnergyFilter(energies)


#particle
particle_filter = openmc.ParticleFilter('neutron')

#mesh
mesh = openmc.RegularMesh()
mesh.dimension = [mesh_dimension, mesh_dimension]
mesh.lower_left = [0, 0]
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
t_mesh.scores = ['fission', '(n,gamma)', 'elastic', 'fission-q-recoverable', 'flux']
tallies.append(t_mesh)


tallies.export_to_xml()


##################################################################
#                           RUN OPENMC                            #
##################################################################

openmc.run()



##################################################################
#                        POST-PROCESSING                         #
##################################################################

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
plt.savefig("images/{}/plots/flux_spectrum.png".format(configuration['name']), dpi=700)
plt.clf()


tally_mesh = sp.get_tally(name='mesh_tally')
mesh_cell_volume = ((assembly_side/2)/mesh_dimension)**2

#flux
flux = tally_mesh.get_slice(scores=['flux'])
flux.mean.shape = (mesh_dimension,mesh_dimension)
flux_rec = reconstruct_complete_mesh(flux.mean)
mesh_plot(flux_rec/mesh_cell_volume, 'Fission reaction rate [1/cm3-src]', 'flux')

#fission reaction rate
fission_rr = tally_mesh.get_slice(scores=['fission'])
fission_rr.mean.shape = (mesh_dimension,mesh_dimension)
fission_rr_rec = reconstruct_complete_mesh(fission_rr.mean)
mesh_plot(fission_rr_rec/mesh_cell_volume, 'Fission reaction rate [1/cm3-src]', 'fission_rr')

#scattering reaction rate
elastic_rr = tally_mesh.get_slice(scores=['(n,elastic)'])
elastic_rr.mean.shape = (mesh_dimension,mesh_dimension)
elastic_rr_rec = reconstruct_complete_mesh(elastic_rr.mean)
mesh_plot(elastic_rr_rec/mesh_cell_volume, 'Elastic Scattering Reaction Rate [1/cm3-src]', 'elastic_rr')


#capture reaction rate
capture_rr = tally_mesh.get_slice(scores=['(n,gamma)'])
capture_rr.mean.shape = (mesh_dimension,mesh_dimension)
capture_rr_rec = reconstruct_complete_mesh(capture_rr.mean)
mesh_plot(capture_rr_rec/mesh_cell_volume, 'Radiative Capture Reaction Rate [1/cm3-src]', 'capture_rr')


#recoverable energy
rec_ene = tally_mesh.get_slice(scores=['fission-q-recoverable'])
rec_ene.mean.shape = (mesh_dimension,mesh_dimension)
rec_ene_rec = reconstruct_complete_mesh(rec_ene.mean)
mesh_plot(rec_ene_rec/mesh_cell_volume, 'Recoverable energy [eV/cm3-src]', 'recoverable_energy')

print('\nTop plots completed...')

#RADIAL HORIZONTAL
radial_index=0
radial_flux = flux.mean[radial_index,:]
radial_fission = fission_rr.mean[radial_index,:]
radial_capture = capture_rr.mean[radial_index,:]
radial_elastic = elastic_rr.mean[radial_index,:]
radial_recene = rec_ene.mean[radial_index,:]


plot_radially(radial_flux/mesh_cell_volume, title='Radial horizontal distribution of neutron flux', ylabel='Neutron flux [neutron/cm2-src]', filename='flux')

plot_radially(radial_fission/mesh_cell_volume, title='Radial horizontal distribution of fission reaction rate', ylabel='Fission reaction rate [1/cm3-src]', filename='fission_rr')

plot_radially(radial_capture/mesh_cell_volume, title='Radial horizontal distribution of (n,gamma) reaction rate', ylabel='(n,gamma) reaction rate [1/cm3-src]', filename='capture_rr')

plot_radially(radial_elastic/mesh_cell_volume, title='Radial horizontal distribution of elastic scattering reaction rate', ylabel='Elastic Scattering reaction rate [1/cm3-src]', filename='elastic_rr')

plot_radially(radial_recene/mesh_cell_volume, title='Radial horizontal distribution of recoverable energy', ylabel='Recoverable energy [eV/cm3-src]', filename='recoverable_energy')

print('\nRadial plots completed...')


#RADIAL DIAG

radial_diag_flux = np.diag(flux.mean)
radial_diag_fission = np.diag(fission_rr.mean)
radial_diag_capture = np.diag(capture_rr.mean)
radial_diag_elastic = np.diag(elastic_rr.mean)
radial_diag_recene = np.diag(rec_ene.mean)

plot_radially(radial_diag_flux/mesh_cell_volume, title='Radial diagonal distribution of neutron flux', ylabel='Fission reaction rate [neutron/cm2-src]', diag=True, filename='flux')

plot_radially(radial_diag_fission/mesh_cell_volume, title='Radial diagonal distribution of fission reaction rate', ylabel='Fission reaction rate [1/cm3-src]', diag=True, filename='fission_rr')

plot_radially(radial_diag_capture/mesh_cell_volume, title='Radial diagonal distribution of (n,gamma) reaction rate', ylabel='(n,gamma) reaction rate [1/cm3-src]', diag=True, filename='capture_rr')

plot_radially(radial_diag_elastic/mesh_cell_volume, title='Radial diagonal distribution of elastic scattering reaction rate', ylabel='Elastic Scattering reaction rate [1/cm3-src]', diag=True, filename='elastic_rr')

plot_radially(radial_diag_recene/mesh_cell_volume, title='Radial diagonal distribution of recoverable energy', ylabel='Recoverable energy [eV/src]', diag=True, filename='recoverable_energy')

print('\nRadial diag plots completed...')


#order main folder
shutil.move("materials.xml", "model_xml/materials.xml")
shutil.move("geometry.xml", "model_xml/geometry.xml")
shutil.move("settings.xml", "model_xml/settings.xml")
shutil.move("plots.xml", "model_xml/plots.xml")
shutil.move("tallies.xml", "model_xml/tallies.xml")

shutil.move("statepoint.100.h5", "output/statepoint.100.h5")
shutil.move("summary.h5", "output/summary.h5")
shutil.move("tallies.out", "output/tallies.out")
