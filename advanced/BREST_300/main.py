import openmc

import numpy as np
import shutil

####################################################################################
#                                     MAIN VARIABLES                               #
####################################################################################

fuel_or = 4.1
clad_ir = fuel_or + 0.25
clad_or = clad_ir + 0.5
assembly_pitch = 13
core_pitch = assembly_pitch*13



####################################################################################
#                                       MATERIALS                                  #
####################################################################################

############################################################ Coolant
#Lead
Pb = openmc.Material(name='Lead')
Pb.add_element('Pb', 1)
Pb.set_density('g/cc', 10.48)
Pb.temperature = 480 + 273.15

#Lead gap
Pb_gap = openmc.Material(name='Lead_gap')
Pb_gap.add_element('Pb', 1)
Pb_gap.set_density('g/cc', 10.48)
Pb_gap.temperature = + 273.15

############################################################ Cladding
# Cladding
clad = openmc.Material(name='Cladding')
clad.add_element('Fe', percent=0.8387, percent_type='wo')
clad.add_element('Cr', percent=0.1130, percent_type='wo')
clad.add_element('Si', percent=0.0115, percent_type='wo')
clad.add_element('Ni', percent=0.0085, percent_type='wo')
clad.add_element('Mo', percent=0.0082, percent_type='wo')
clad.add_element('W',  percent=0.0066, percent_type='wo')
clad.add_element('Mn', percent=0.0062, percent_type='wo')
clad.add_element('V',  percent=0.0032, percent_type='wo')
clad.add_element('Nb', percent=0.0026, percent_type='wo')
clad.add_element('C',  percent=0.0015, percent_type='wo')
clad.set_density('g/cc', 7.64)
clad.temperature = 600 + 273.15

############################################################ Fuel
# Nitrogen
N = openmc.Material(name='Nitrogen')
N.add_element('N', 1.0)

# Natural Uranium
U = openmc.Material(name='Natural_Uranium')
U.add_element('U', 1.0)

# Plutonium 239
Pu239 = openmc.Material(name='Pu239')
Pu239.add_nuclide('Pu239', 1.0)

# Plutonium 240
Pu240 = openmc.Material(name='Pu240')
Pu240.add_nuclide('Pu240', 1.0)

# Plutonium 241
Pu241 = openmc.Material(name='Pu241')
Pu241.add_nuclide('Pu241', 1.0)

# Plutonium 242
Pu242 = openmc.Material(name='Pu242')
Pu242.add_nuclide('Pu242', 1.0)

# Plutonium
Pu = openmc.Material.mix_materials([Pu239, Pu240, Pu241, Pu242],
                                    [0.6, 0.25, 0.11, 0.04], 'wo', name='Pu')

# U + Pu for inner core
fissionable_inner = openmc.Material.mix_materials([U, Pu], [0.8883, 0.1117], 'wo', name='fissionable_inner')

# U + Pu for outer core
fissionable_outer = openmc.Material.mix_materials([U, Pu], [0.8554, 0.1446], 'wo', name='fissionable_outer')

# Fuel for inner core
fuel_inner = openmc.Material.mix_materials([fissionable_inner, N], [0.5,0.5], 'ao', name='fuel_inner')
fuel_inner.set_density('g/cc', )
fuel_inner.temperature =

# Fuel for outer core
fuel_outer = openmc.Material.mix_materials([fissionable_outer, N], [0.5,0.5], 'ao', name='fuel_outer')
fuel_outer.set_density('g/cc', )
fuel_outer.temperature =

materials = openmc.Materials([Pb, Pb_gap, clad, N, U, Pu, fuel_inner, fuel_outer])
materials.export_to_xml()



####################################################################################
#                                       GEOMETRY                                   #
####################################################################################

############################################################## PINCELL
fuel_or_surface = openmc.ZCylinder(r=fuel_or)
clad_ir_surface = openmc.ZCylinder(r=clad_ir)
clad_or_surface = openmc.ZCylinder(r=clad_or)


gap_cell = openmc.Cell(fill=Pb_gap, region=+fuel_or_surface & -clad_ir_surface)
clad_cell = openmc.Cell(fill=clad, region=+clad_ir_surface & -clad_or_surface)
coolant_cell = openmc.Cell(fill=Pb, region=+clad_or_surface)

fuel_in_cell = openmc.Cell(fill=fuel_inner, region=-fuel_or_surface)
fuel_out_cell = openmc.Cell(fill=fuel_outer, region=-fuel_or_surface)

fuel_in_universe = openmc.Universe(cells=[fuel_in_cell, gap_cell, clad_cell, coolant_cell])
fuel_out_universe = openmc.Universe(cells=[fuel_out_cell, gap_cell, clad_cell, coolant_cell])

outer_lead = openmc.Cell(fill=Pb)
outer_universe = openmc.Universe(cells=[outer_lead])

## DEBUG
clad_inf_cell = openmc.Cell(fill=clad)
clad_universe = openmc.Universe(cells=[clad_inf_cell])


############################################################## ASSEMBLY IN
assembly_in_lattice = openmc.HexLattice()
assembly_in_lattice.center = (0,0)
assembly_in_lattice.pitch = (assembly_pitch,)
assembly_in_lattice.orientation = 'x'
assembly_in_lattice.outer = outer_universe

in_1 = [fuel_in_universe]*42
in_2 = [fuel_in_universe]*36
in_3 = [fuel_in_universe]*30
in_4 = [fuel_in_universe]*24
in_5 = [fuel_in_universe]*18
in_6 = [fuel_in_universe]*12
in_7 = [fuel_in_universe]*6
in_8 = [fuel_in_universe]*1
assembly_in_lattice.universes = [in_1, in_2, in_3, in_4, in_5, in_6, in_7, in_8]

assembly_in_container_prism = openmc.model.hexagonal_prism(edge_length=97.43, orientation='x', origin=(0,0))
assembly_in_container = openmc.Cell(fill=assembly_in_lattice, region=assembly_in_container_prism, name='assembly_in_container')
assembly_in_outer = openmc.Cell(fill=Pb, region=~assembly_in_container_prism, name='assembly_in_outer')

assembly_in_universe = openmc.Universe(cells=[assembly_in_container, assembly_in_outer])


############################################################## ASSEMBLY OUT
assembly_out_lattice = openmc.HexLattice()
assembly_out_lattice.center = (0,0)
assembly_out_lattice.pitch = (assembly_pitch,)
assembly_out_lattice.orientation = 'x'
assembly_out_lattice.outer = outer_universe

out_1 = [fuel_out_universe]*42
out_2 = [fuel_out_universe]*36
out_3 = [fuel_out_universe]*30
out_4 = [fuel_out_universe]*24
out_5 = [fuel_out_universe]*18
out_6 = [fuel_out_universe]*12
out_7 = [fuel_out_universe]*6
out_8 = [fuel_out_universe]*1
assembly_out_lattice.universes = [out_1, out_2, out_3, out_4, out_5, out_6, out_7, out_8]

assembly_out_container_prism = openmc.model.hexagonal_prism(edge_length=97.43, orientation='x', origin=(0,0))
assembly_out_container = openmc.Cell(fill=assembly_out_lattice, region=assembly_out_container_prism, name='assebly_out_container')
assembly_out_outer = openmc.Cell(fill=Pb, region=~assembly_out_container_prism, name='assebly_out_outer')

assembly_out_universe = openmc.Universe(cells=[assembly_out_container, assembly_out_outer])


########################################################################## CORE
core_lattice = openmc.HexLattice()
core_lattice.center = (0,0)
core_lattice.pitch = (core_pitch,)
core_lattice.orientation = 'y'
core_lattice.outer = outer_universe

core_1 = [assembly_out_universe]*36
core_2 = [assembly_out_universe]*30
core_3 = [assembly_in_universe]*24
core_4 = [assembly_in_universe]*18
core_5 = [assembly_in_universe]*12
core_6 = [assembly_in_universe]*6
core_7 = [assembly_in_universe]*1
core_lattice.universes = [core_1, core_2, core_3, core_4, core_5, core_6, core_7]

circle_core = openmc.ZCylinder(r=1200)
main_cell = openmc.Cell(fill=core_lattice, region = -circle_core)
main_universe = openmc.Universe(cells=[main_cell])

core_geometry = openmc.Geometry(main_universe)
core_geometry.export_to_xml()



####################################################################################
#                                 GEOMETRY PLOTS                                   #
####################################################################################

# TOP VIEW
top_view = openmc.Plot.from_geometry(core_geometry)
top_view.basis = 'xy'
top_view.pixels = (5000, 5000)
top_view.color_by = 'material'
top_view.colors = {
    fuel_inner: 'yellow',
    fuel_outer: 'orange',
    Pb: 'grey',
    Pb_gap: 'grey',
    clad: 'black'
}
top_view.filename = 'images/geometry/core_top_view'

# SIDE VIEW LONG
side_view_long = openmc.Plot.from_geometry(core_geometry)
side_view_long.basis = 'yz'
side_view_long.pixels = (2000, 2000)
side_view_long.color_by = 'material'
side_view_long.colors = {
    fuel_inner: 'yellow',
    fuel_outer: 'orange',
    Pb: 'grey',
    Pb_gap: 'grey',
    clad: 'black'
}
side_view_long.filename = 'images/geometry/core_side_view_long'

# SIDE VIEW SHORT
side_view_short = openmc.Plot.from_geometry(core_geometry)
side_view_short.basis = 'xz'
side_view_short.pixels = (2000, 2000)
side_view_short.color_by = 'material'
side_view_short.colors = {
    fuel_inner: 'yellow',
    fuel_outer: 'orange',
    Pb: 'grey',
    Pb_gap: 'grey',
    clad: 'black'
}
side_view_short.filename = 'images/geometry/core_side_view_short'


plots = openmc.Plots([top_view, side_view_long, side_view_short])
plots.export_to_xml()
openmc.plot_geometry()



####################################################################################
#                                 ORDER FOLDER                                     #
####################################################################################

shutil.move("materials.xml", "model_xml/materials.xml")
shutil.move("geometry.xml", "model_xml/geometry.xml")
shutil.move("plots.xml", "model_xml/plots.xml")
