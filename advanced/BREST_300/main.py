import openmc

import numpy as np


####################################################################################
#                                     MAIN VARIABLES                               #
####################################################################################

fuel_or = 4.1
clad_ir = fuel_or + 0.25
clad_or = clad_ir + 0.5
pitch = 13




####################################################################################
#                                       MATERIALS                                  #
####################################################################################

############################################################ Coolant
#Lead
Pb = openmc.Material(name='Lead')
Pb.add_element('Pb', 1)

#Lead gap
Pb_gap = openmc.Material(name='Lead gap')
Pb_gap.add_element('Pb', 1)

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

############################################################ Fuel
# Nitrogen
N = openmc.Material(name='Nitrogen')
N.add_element('N', 1.0)

# Natural Uranium
U = openmc.Material(name='Natural Uranium')
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

# Fuel for outer core
fuel_outer = openmc.Material.mix_materials([fissionable_outer, N], [0.5,0.5], 'ao', name='fuel_outer')


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


############################################################## ASSEMBLY IN
assembly_in_lattice = openmc.HexLattice()
assembly_in_lattice.center = (0,0)
assembly_in_lattice.pitch = (pitch,)
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
assembly_in_container = openmc.Cell(fill=assembly_in_lattice, region=assembly_in_container_prism)
assembly_outer = openmc.Cell(fill=Pb, region=~assembly_in_container_prism)

assembly_in_universe = openmc.Universe(cells=[assembly_in_container, assembly_outer])

############################################################## ASSEMBLY OUT
assembly_out_lattice = openmc.HexLattice()
assembly_out_lattice.center = (0,0)
assembly_out_lattice.pitch = (pitch,)
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
assembly_out_container = openmc.Cell(fill=assembly_out_lattice, region=assembly_out_container_prism)
assembly_outer = openmc.Cell(fill=Pb, region=~assembly_out_container_prism)

assembly_out_universe = openmc.Universe(cells=[assembly_out_container, assembly_outer])

########################################################################## CORE
core_lattice = openmc.HexLattice()
core_lattice.center = (0,0)
core_lattice.pitch = (pitch*14,)
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

circle = openmc.ZCylinder(r=1200)
main_cell = openmc.Cell(fill=core_lattice, region = -circle)
main_universe = openmc.Universe(cells=[main_cell])

geometry = openmc.Geometry(main_universe)
geometry.export_to_xml()

print(geometry.get_all_materials())




# FAST PLOT for debugging
plot = openmc.Plot.from_geometry(geometry)
plot.basis = 'xy'
plot.pixels = (1500, 1500)
plot.color_by = 'material'
plot.colors = colors = {
    fuel_inner: 'yellow',
    fuel_outer: 'orange',
    Pb: 'grey',
    Pb_gap: 'grey',
    clad: 'black'
}
plot.filename = 'top_view'

plots = openmc.Plots([plot])
plots.export_to_xml()
openmc.plot_geometry()
