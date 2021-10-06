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
    plt.imshow(mesh_data, cmap='jet', origin='lower', extent = [-pitch/2,pitch/2,-pitch/2,pitch/2])
    plt.suptitle(title,fontsize=14)
    plt.title('mesh size: [{},{}]   |   neutrons/batch: {}'.format(mesh_dim,mesh_dim,neutrons_per_batch),fontsize=10)
    plt.xlabel('Distance from center [cm]')
    plt.ylabel('Distance from center [cm]')
    plt.colorbar()
    plt.savefig("images/plots/{}.png".format(filename), dpi=700)
    plt.clf()


def plot_radially(radial_data, ylabel, title, filename, diag=False, alpha=0.5):
    geom_image = mpimg.imread('images/geometry/side_view.ppm')
    pitch_dim = pitch
    mesh_dim = mesh_dimension
    directory = 'horizontal'
    if diag:
        geom_image = mpimg.imread('images/geometry/side_diagonal_view.ppm')
        pitch_dim = diagonal_pitch
        directory = 'diagonal'
    fig, axs = plt.subplots(2,1, sharex=True, sharey=True, figsize=(15,10))
    fig.suptitle('{}'.format(title), fontsize=19)
    axs[0].set_title('mesh size: [{},{}]   |   neutrons/batch: {}'.format(mesh_dim,mesh_dim,neutrons_per_batch),fontsize=14, pad=30)
    axs[1].imshow(geom_image, alpha=alpha, origin='lower', extent=[-pitch_dim/2,pitch_dim/2,0,1.2*np.amax(radial_data)])
    axs[0].plot(np.linspace(-pitch_dim/2,pitch_dim/2,mesh_dim),radial_data, 'r-', linewidth=2)
    axs[1].plot(np.linspace(-pitch_dim/2,pitch_dim/2,mesh_dim), radial_data, 'r-', linewidth=3)
    axs[1].xaxis.tick_top()
    axs[1].xaxis.set_label_position('top')
    axs[1].set_xlabel('Radial Distance [cm]')
    axs[1].set_aspect('auto')
    for ax in axs:
        ax.set_ylabel('{}'.format(ylabel))

    plt.savefig("images/radial_plots/{}/{}.png".format(directory,filename), dpi=700)
    plt.clf()



##################################################################
#                         MAIN VARIABLES                         #
##################################################################

pitch = 1.0730001
diagonal_pitch = math.sqrt(2)*pitch
mesh_dimension = 300
neutrons_per_batch = 2000



##################################################################
#                      DEFINE MATERIALS                          #
##################################################################

U235 = openmc.Material(name='U235')
U235.add_nuclide('U235', 1.0)
U235.set_density('g/cm3', 10.0)

U238 = openmc.Material(name='U238')
U238.add_nuclide('U238', 1.0)
U238.set_density('g/cm3', 10.0)

Pu238 = openmc.Material(name='Pu238')
Pu238.add_nuclide('Pu238', 1.0)
Pu238.set_density('g/cm3', 10.0)

Pu239 = openmc.Material(name='U235')
Pu239.add_nuclide('Pu239', 1.0)
Pu239.set_density('g/cm3', 10.0)

Pu240 = openmc.Material(name='Pu240')
Pu240.add_nuclide('Pu240', 1.0)
Pu240.set_density('g/cm3', 10.0)

Pu241 = openmc.Material(name='Pu241')
Pu241.add_nuclide('Pu241', 1.0)
Pu241.set_density('g/cm3', 10.0)

Pu242 = openmc.Material(name='Pu242')
Pu242.add_nuclide('Pu242', 1.0)
Pu242.set_density('g/cm3', 10.0)

Am241 = openmc.Material(name='Am241')
Am241.add_nuclide('Am241', 1.0)
Am241.set_density('g/cm3', 10.0)

O16 = openmc.Material(name='O16')
O16.add_nuclide('O16', 1.0)
O16.set_density('g/cm3', 10.0)

sodium = openmc.Material(name='sodium')
sodium.add_nuclide('Na23', 1.0)
sodium.set_density('g/cm3', 0.96)

Cu63 = openmc.Material(name='Cu63')
Cu63.set_density('g/cm3', 10.0)
Cu63.add_nuclide('Cu63', 1.0)

Al2O3 = openmc.Material(name='Al2O3')
Al2O3.set_density('g/cm3', 10.0)
Al2O3.add_element('O', 3.0)
Al2O3.add_element('Al', 2.0)

#mixtures
inner = openmc.Material.mix_materials(
    [U235, U238, Pu238, Pu239, Pu240, Pu241, Pu242, Am241, O16],
    [0.0019, 0.7509, 0.0046, 0.0612, 0.0383, 0.0106, 0.0134, 0.001, 0.1181],
    'wo', name='inner')
clad = openmc.Material.mix_materials(
    [Cu63,Al2O3], [0.997,0.003], 'wo', name='clad')

#export
materials_file = openmc.Materials([inner, sodium, clad])
materials_file.export_to_xml()


##################################################################
#                       DEFINE GEOMETRY                          #
##################################################################

#=====================================begin mock geometry==================================================================
# in order to plot the tallies radially we need to include the sodium region. To do that we need to create a
# mock geometry to plot the side diagonal view THIS PORTION OF THE CODE IS ONLY OF USE TO CREATE THE BACKGROUND
# PLOT IN THE RADIAL CHARTS. We create the mock geometry, plot it and replace it with the real one.

fuel_or = openmc.ZCylinder(surface_id=4, r=0.943/2)
clad_ir = openmc.ZCylinder(surface_id=5, r=0.973/2)
clad_or = openmc.ZCylinder(surface_id=6, r=1.073/2)

left = openmc.XPlane(x0=-diagonal_pitch/2, boundary_type='reflective')
right = openmc.XPlane(x0=diagonal_pitch/2, boundary_type='reflective')
bottom = openmc.YPlane(y0=-diagonal_pitch/2, boundary_type='reflective')
top = openmc.YPlane(y0=diagonal_pitch/2, boundary_type='reflective')

fuel_region = -fuel_or
gap_region  = +fuel_or & -clad_ir
clad_region = +clad_ir & -clad_or
moderator_region = +clad_or & +left & -right & -top & +bottom

gap_cell = openmc.Cell(cell_id=5, fill=inner, region=gap_region)
clad_cell = openmc.Cell(cell_id=6, fill=clad, region=clad_region)
sodium_cell = openmc.Cell(cell_id=7, fill=sodium, region=moderator_region)
fuel_cell = openmc.Cell(cell_id=8, fill=inner, region=fuel_region)
universe = openmc.Universe(universe_id=2, cells=(fuel_cell, gap_cell, clad_cell, sodium_cell))

geometry = openmc.Geometry()
geometry.root_universe = universe
geometry.export_to_xml()

geom_plot_diag_side = openmc.Plot()
geom_plot_diag_side.basis = 'xz'
geom_plot_diag_side.origin = (0., 0., 0.)
geom_plot_diag_side.width = (diagonal_pitch, diagonal_pitch)
geom_plot_diag_side.pixels = (400, 400)
geom_plot_diag_side.color_by = 'material'
geom_plot_diag_side.colors = {inner: 'yellow', sodium: 'orange',clad:'grey'}
geom_plot_diag_side.filename = 'images/geometry/side_diagonal_view'

plots = openmc.Plots([geom_plot_diag_side])
plots.export_to_xml()
openmc.plot_geometry()

#============================================end mock===========================================================

fuel_or = openmc.ZCylinder(surface_id=1, r=0.943/2)
clad_ir = openmc.ZCylinder(surface_id=2, r=0.973/2)
clad_or = openmc.ZCylinder(surface_id=3, r=1.073/2)

left = openmc.XPlane(x0=-pitch/2, boundary_type='reflective')
right = openmc.XPlane(x0=pitch/2, boundary_type='reflective')
bottom = openmc.YPlane(y0=-pitch/2, boundary_type='reflective')
top = openmc.YPlane(y0=pitch/2, boundary_type='reflective')

fuel_region = -fuel_or
gap_region  = +fuel_or & -clad_ir
clad_region = +clad_ir & -clad_or
moderator_region = +clad_or & +left & -right & -top & +bottom

gap_cell = openmc.Cell(cell_id=1, fill=inner, region=gap_region)
clad_cell = openmc.Cell(cell_id=2, fill=clad, region=clad_region)
sodium_cell = openmc.Cell(cell_id=3, fill=sodium, region=moderator_region)
fuel_cell = openmc.Cell(cell_id=4, fill=inner, region=fuel_region)
universe = openmc.Universe(universe_id=1, cells=(fuel_cell, gap_cell, clad_cell, sodium_cell))

geometry = openmc.Geometry()
geometry.root_universe = universe
geometry.export_to_xml()



##################################################################
#                        PLOT GEOMETRY                           #
##################################################################

#top view
geom_plot_top = openmc.Plot()
geom_plot_top.basis = 'xy'
geom_plot_top.origin = (0., 0., 0.)
geom_plot_top.width = (pitch, pitch)
geom_plot_top.pixels = (1500, 1500)
geom_plot_top.color_by = 'material'
geom_plot_top.colors = {inner: 'yellow', sodium: 'orange',clad:'grey'}
geom_plot_top.filename = 'images/geometry/top_view'

#side view
geom_plot_side = openmc.Plot()
geom_plot_side.basis = 'xz'
geom_plot_side.origin = (0., 0., 0.)
geom_plot_side.width = (pitch, pitch)
geom_plot_side.pixels = (400, 400)
geom_plot_side.color_by = 'material'
geom_plot_side.colors = {inner: 'yellow', sodium: 'orange',clad:'grey'}
geom_plot_side.filename = 'images/geometry/side_view'

plots = openmc.Plots([geom_plot_top, geom_plot_side])
plots.export_to_xml()
openmc.plot_geometry()


##################################################################
#                         DEFINE SETTINGS                        #
##################################################################

point = openmc.stats.Point((0, 0, 0))
source = openmc.Source(space=point)

settings = openmc.Settings()
settings.source = source
settings.batches = 100
settings.inactive = 20
settings.particles = neutrons_per_batch

settings.export_to_xml()



##################################################################
#                         DEFINE TALLIES                         #
##################################################################

#FILTERS
#energy
energies = np.logspace(np.log10(1e-3), np.log10(20.0e6), 501)
energy_filter = openmc.EnergyFilter(energies)

#particle
particle_filter = openmc.ParticleFilter('neutron')

#mesh
mesh = openmc.RegularMesh()
mesh.dimension = [mesh_dimension, mesh_dimension]
mesh.lower_left = [-pitch/2, -pitch/2]
mesh.upper_right = [pitch/2, pitch/2]
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


##################################################################
#                           RUN OPENMC                            #
##################################################################

#openmc.run()


##################################################################
#                        POST-PROCESSING                         #
##################################################################

sp = openmc.StatePoint('statepoint.100.h5')

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
mesh_cell_volume = (pitch/mesh_dimension)**2
#fission reaction rate
fission_rr = tally_mesh.get_slice(scores=['fission'])
fission_rr.mean.shape = (mesh_dimension,mesh_dimension)
mesh_plot(fission_rr.mean/mesh_cell_volume, 'Fission reaction rate [1/cm3-src]', 'fission_rr')

#scattering reaction rate
elastic_rr = tally_mesh.get_slice(scores=['(n,elastic)'])
elastic_rr.mean.shape = (mesh_dimension,mesh_dimension)
mesh_plot(elastic_rr.mean/mesh_cell_volume, 'Elastic Scattering Reaction Rate [1/cm3-src]', 'elastic_rr')

#capture reaction rate
capture_rr = tally_mesh.get_slice(scores=['(n,gamma)'])
capture_rr.mean.shape = (mesh_dimension,mesh_dimension)
mesh_plot(capture_rr.mean/mesh_cell_volume, 'Radiative Capture Reaction Rate [1/cm3-src]', 'capture_rr')

#recoverable energy
rec_ene = tally_mesh.get_slice(scores=['fission-q-recoverable'])
rec_ene.mean.shape = (mesh_dimension,mesh_dimension)
mesh_plot(rec_ene.mean/mesh_cell_volume, 'Recoverable energy [eV/cm3-src]', 'recoverable_energy')


#RADIAL_ORIZONTAL
radial_index=int((mesh_dimension/2)-1)
radial_horiz_fission = fission_rr.mean[radial_index,:]
radial_horiz_capture = capture_rr.mean[radial_index,:]
radial_horiz_elastic = elastic_rr.mean[radial_index,:]
radial_horiz_recene = rec_ene.mean[radial_index,:]


plot_radially(radial_horiz_fission/mesh_cell_volume, title='Radial horizontal distribution of fission reaction rate', ylabel='Fission reaction rate [1/cm3-src]', filename='fission_rr')

plot_radially(radial_horiz_capture/mesh_cell_volume, title='Radial horizontal distribution of (n,gamma) reaction rate', ylabel='(n,gamma) reaction rate [1/cm3-src]', filename='capture_rr')

plot_radially(radial_horiz_elastic/mesh_cell_volume, title='Radial horizontal distribution of elastic scattering reaction rate', ylabel='Elastic Scattering reaction rate [1/cm3-src]', filename='elastic_rr')

plot_radially(radial_horiz_recene/mesh_cell_volume, title='Radial horizontal distribution of recoverable energy', ylabel='Recoverable energy [eV/cm3-src]', filename='recoverable_energy')


#RADIAL_DIAGONAL
radial_diag_fission = np.diagonal(fission_rr.mean)
radial_diag_capture = np.diagonal(capture_rr.mean)
radial_diag_elastic = np.diagonal(elastic_rr.mean)
radial_diag_recene = np.diagonal(rec_ene.mean)


plot_radially(radial_diag_fission/mesh_cell_volume, title='Radial diagonal distribution of fission reaction rate', ylabel='Fission reaction rate [1/cm3-src]', diag=True, filename='fission_rr')

plot_radially(radial_diag_capture/mesh_cell_volume, title='Radial diagonal distribution of (n,gamma) reaction rate', ylabel='(n,gamma) reaction rate [1/cm3-src]', diag=True, filename='capture_rr')

plot_radially(radial_diag_elastic/mesh_cell_volume, title='Radial diagonal distribution of elastic scattering reaction rate', ylabel='Elastic Scattering reaction rate [1/cm3-src]', diag=True, filename='elastic_rr')

plot_radially(radial_diag_recene/mesh_cell_volume, title='Radial diagonal distribution of recoverable energy', ylabel='Recoverable energy [eV/cm3-src]', diag=True, filename='recoverable_energy')



##################################################################
#                        ORDER FOLDER                            #
##################################################################

shutil.move("materials.xml", "model_xml/materials.xml")
shutil.move("geometry.xml", "model_xml/geometry.xml")
shutil.move("settings.xml", "model_xml/settings.xml")
shutil.move("plots.xml", "model_xml/plots.xml")
shutil.move("tallies.xml", "model_xml/tallies.xml")

shutil.move("statepoint.100.h5", "output/statepoint.100.h5")
shutil.move("summary.h5", "output/summary.h5")
shutil.move("tallies.out", "output/tallies.out")
