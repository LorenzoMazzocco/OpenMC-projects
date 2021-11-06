import openmc
import openmc.model

import numpy as np
import matplotlib.pyplot as plt



###########################################################
#                          SETTINGS                       #
###########################################################

plot_rod_universes = False
plot_geometry = True


###########################################################
#                        MAIN VARIABLES                   #
###########################################################

control_shim_extraction_level = 0
control_trans_extraction_level = 0
control_reg_extraction_level = 0


###########################################################
#                         MATERIALS                       #
###########################################################


ZrH = openmc.Material(name='ZrH')
ZrH.add_element('Zr', 1.)
ZrH.add_element('H', 1.)


U = openmc.Material(name='U_enr')
U.add_element('U', 1., enrichment=20)

fuel = openmc.Material.mix_materials([U, ZrH], [0.08, 0.92], 'wo', name='UZrH')
fuel.set_density('g/cc', 6.3)
fuel.add_s_alpha_beta('c_H_in_ZrH')

Al = openmc.Material(name='Al')
Al.add_element('Al', 1.)
Al.set_density('g/cc', 2.7)

Sm2O3 = openmc.Material(name='Sm2O3')
Sm2O3.add_element('Sm', 2.0)
Sm2O3.add_element('O', 3.0)
Sm2O3.set_density('g/cc', 8.35)

water = openmc.Material(name='H2O')
water.add_element('H', 2.)
water.add_element('O', 1.)
water.set_density('g/cc', 1.)

graphite = openmc.Material(name='graphite')
graphite.add_element('C', 1.)
graphite.set_density('g/cc', 2.6)

B4C = openmc.Material(name='boron')
B4C.add_element('C', 0.2, 'ao')
B4C.add_nuclide('B10', 0.158, 'ao')
B4C.add_nuclide('B11', 0.642, 'ao')
B4C.set_density('g/cc', 2.52)

materials = openmc.Materials([ZrH, U, fuel, Al, Sm2O3, water, graphite, B4C])
materials.export_to_xml()


###########################################################
#                          GEOMETRY                       #
###########################################################

##################
#  FUEL ELEMENT  #
##################

fuel_or_surface = openmc.ZCylinder(r=3.58/2)
clad_or_surface = openmc.ZCylinder(r=3.76/2)

fuel_top_surface = openmc.ZPlane(z0=-(1.27+10.07+0.13))
fuel_bottom_surface = openmc.ZPlane(z0=-(1.27+10.07+0.13+35.56))

BA_down_bottom_surface = openmc.ZPlane(z0=-(1.27+10.07+0.13+35.56+0.13))
BA_up_top_surface = openmc.ZPlane(z0=-(1.27+10.07))

reflector_down_bottom_surface = openmc.ZPlane(z0=-(1.27+10.07+0.13+35.56+0.1+10.07))
reflector_up_top_surface = openmc.ZPlane(z0=-(1.27))

large_plug_down_bottom_surface = openmc.ZPlane(z0=-(1.27+10.07+0.13+35.56+0.1+10.07+1.27))
large_plug_up_top_surface = openmc.ZPlane(z0=0)


fuel_element_A_cell = openmc.Cell(fill=fuel, region=-fuel_or_surface & +fuel_bottom_surface & -fuel_top_surface)

fuel_element_C_down_cell = openmc.Cell(fill=Sm2O3, region=-fuel_or_surface & +BA_down_bottom_surface & -fuel_bottom_surface)
fuel_element_C_up_cell = openmc.Cell(fill=Sm2O3, region=-fuel_or_surface & +fuel_top_surface & -BA_up_top_surface)

fuel_element_B_down_cell = openmc.Cell(fill=graphite, region=-fuel_or_surface & +reflector_down_bottom_surface & -BA_down_bottom_surface)
fuel_element_B_up_cell = openmc.Cell(fill=graphite, region=-fuel_or_surface & +BA_up_top_surface & -reflector_up_top_surface)

fuel_element_D_cell = openmc.Cell(fill=Al, region=+fuel_or_surface & -clad_or_surface & +reflector_down_bottom_surface & -reflector_up_top_surface)

fuel_element_E_down_cell = openmc.Cell(fill=Al, region=-clad_or_surface & +large_plug_down_bottom_surface & -reflector_down_bottom_surface)
fuel_element_E_up_cell = openmc.Cell(fill=Al, region=-clad_or_surface & + reflector_up_top_surface & -large_plug_up_top_surface)

fuel_water_out = openmc.Cell(fill=water, region=+clad_or_surface)
fuel_water_in = openmc.Cell(fill=water, region=-clad_or_surface & -large_plug_down_bottom_surface)

fuel_element_universe = openmc.Universe(cells=[fuel_element_A_cell, fuel_element_C_down_cell, fuel_element_C_up_cell, fuel_element_D_cell, fuel_element_B_down_cell, fuel_element_B_up_cell, fuel_element_E_down_cell, fuel_element_E_up_cell, fuel_water_out, fuel_water_in])


######################
#    CONTROL RODS    #
######################

# COMMON
control_rods_container_surface = openmc.ZCylinder(r=3.76/2, name='control_rods_container_surface')


##################### SHIM
shim_top = openmc.ZPlane(z0=control_shim_extraction_level)
shim_boron_top_surface = openmc.ZPlane(z0=control_shim_extraction_level-2.54)
shim_boron_bottom_surface = openmc.ZPlane(z0=control_shim_extraction_level-2.54-45.47)
shim_bottom = openmc.ZPlane(z0=control_shim_extraction_level-2.54-45.47-1.6)

shim_id_surface = openmc.ZCylinder(r=2.85/2)
shim_od_surface = openmc.ZCylinder(r=3.18/2)

shim_boron_cell = openmc.Cell(fill=B4C, region=-shim_id_surface & +shim_boron_bottom_surface & -shim_boron_top_surface)
shim_cladding_cell = openmc.Cell(fill=Al, region=+shim_id_surface & -shim_od_surface & +shim_bottom & -shim_top)

shim_down_plug_cell = openmc.Cell(fill=Al, region=-shim_od_surface & +shim_bottom & -shim_boron_bottom_surface)
shim_up_plug_cell = openmc.Cell(fill=Al, region=-shim_od_surface & +shim_boron_top_surface & -shim_top)

shim_out_water = openmc.Cell(fill=water, region=+shim_od_surface & -shim_top)
shim_in_water = openmc.Cell(fill=water, region=-shim_od_surface & -shim_bottom)

shim_universe = openmc.Universe(cells=[shim_boron_cell, shim_cladding_cell, shim_down_plug_cell, shim_up_plug_cell, shim_out_water, shim_in_water])


##################### TRANS
trans_top = openmc.ZPlane(z0=control_trans_extraction_level)
trans_boron_top_surface = openmc.ZPlane(z0=control_trans_extraction_level-2.54)
trans_boron_bottom_surface = openmc.ZPlane(z0=control_trans_extraction_level-2.54-45.47)
trans_bottom = openmc.ZPlane(z0=control_trans_extraction_level-2.54-45.47-1.6)

trans_id_surface = openmc.ZCylinder(r=2.21/2)
trans_od_surface = openmc.ZCylinder(r=2.54/2)

trans_boron_cell = openmc.Cell(fill=B4C, region=-trans_id_surface & +trans_boron_bottom_surface & -trans_boron_top_surface)
trans_cladding_cell = openmc.Cell(fill=Al, region=+trans_id_surface & -trans_od_surface & +trans_bottom & -trans_top)

trans_down_plug_cell = openmc.Cell(fill=Al, region=-trans_od_surface & +trans_bottom & -trans_boron_bottom_surface)
trans_up_plug_cell = openmc.Cell(fill=Al, region=-trans_od_surface & +trans_boron_top_surface & -trans_top)

trans_out_water = openmc.Cell(fill=water, region=+trans_od_surface & -trans_top)
trans_in_water = openmc.Cell(fill=water, region=-trans_od_surface & -trans_bottom)

trans_universe = openmc.Universe(cells=[trans_boron_cell, trans_cladding_cell, trans_down_plug_cell, trans_up_plug_cell, trans_out_water, trans_in_water])


##################### REG
reg_top = openmc.ZPlane(z0=control_reg_extraction_level)
reg_boron_top_surface = openmc.ZPlane(z0=control_reg_extraction_level-2.54)
reg_boron_bottom_surface = openmc.ZPlane(z0=control_reg_extraction_level-2.54-45.47)
reg_bottom = openmc.ZPlane(z0=control_reg_extraction_level-2.54-45.47-1.6)

reg_id_surface = openmc.ZCylinder(r=1.93/2)
reg_od_surface = openmc.ZCylinder(r=2.22/2)

reg_boron_cell = openmc.Cell(fill=B4C, region=-reg_id_surface & +reg_boron_bottom_surface & -reg_boron_top_surface)
reg_cladding_cell = openmc.Cell(fill=Al, region=+reg_id_surface & -reg_od_surface & +reg_bottom & -reg_top)

reg_down_plug_cell = openmc.Cell(fill=Al, region=-reg_od_surface & +reg_bottom & -reg_boron_bottom_surface)
reg_up_plug_cell = openmc.Cell(fill=Al, region=-reg_od_surface & +reg_boron_top_surface & -reg_top)

reg_out_water = openmc.Cell(fill=water, region=+reg_od_surface & -reg_top)
reg_in_water = openmc.Cell(fill=water, region=-reg_od_surface & -reg_bottom)

reg_universe = openmc.Universe(cells=[reg_boron_cell, reg_cladding_cell, reg_down_plug_cell, reg_up_plug_cell, reg_in_water, reg_out_water])


##################### GRAPHITE
graphite_top = openmc.ZPlane(z0=0)
graphite_graphite_top_surface = openmc.ZPlane(z0=0-1.27)
graphite_graphite_bottom_surface = openmc.ZPlane(z0=-(1.27+10.07+0.13+35.56+0.1+10.07+1.27-1.27))
graphite_bottom = openmc.ZPlane(z0=-(1.27+10.07+0.13+35.56+0.1+10.07+1.27))

graphite_id_surface = openmc.ZCylinder(r=3.58/2)
graphite_od_surface = openmc.ZCylinder(r=3.76/2)

graphite_graphite_cell = openmc.Cell(fill=graphite, region=-graphite_id_surface & +graphite_graphite_bottom_surface & -graphite_graphite_top_surface)
graphite_cladding_cell = openmc.Cell(fill=Al, region=+graphite_id_surface & -graphite_od_surface & +graphite_bottom & -graphite_top)

graphite_down_plug_cell = openmc.Cell(fill=Al, region=-graphite_od_surface & +graphite_bottom & -graphite_graphite_bottom_surface)
graphite_up_plug_cell = openmc.Cell(fill=Al, region=-graphite_od_surface & +graphite_graphite_top_surface & -graphite_top)

graphite_water = openmc.Cell(fill=water, region=-graphite_od_surface & -graphite_bottom)

graphite_universe = openmc.Universe(cells=[graphite_graphite_cell, graphite_cladding_cell, graphite_down_plug_cell, graphite_up_plug_cell, graphite_water])

##################### FULL WATER
water_cell = openmc.Cell(fill=water)
water_universe = openmc.Universe(cells=[water_cell])


##################################
#            CORE LATTICE        #
##################################

num_pins = [1,6,12,18,24,30]
angles = [0.,0.,0.,0.,0.,0.]
distances = [0., 4.2, 8.15, 12.15, 16.33, 20.34] #cm

shim_position = (2,10)
trans_position = (3,9)
reg_position = (4,4)
water_position = (5,20)

fuel_outer_positions = (3,4,5,6) #j for every fuel element in the last layer

core_cells = []

for i, (r,n,a) in enumerate(zip(distances, num_pins, angles)):
    for j in range(n):
        theta = (a + j/n*360) * np.pi/180 + np.pi/2
        x = r*np.cos(theta)
        y = r*np.sin(theta)



        pin_boundary = openmc.ZCylinder(x0=x, y0=y, r=3.76/2, name='pin_boundary')

        if i == shim_position[0] and j == shim_position[1]:
            pin = openmc.Cell(fill=shim_universe, region=-pin_boundary)
            print('Adding SHIM - ({}, {})'.format(x,y))
        elif i == trans_position[0] and j == trans_position[1]:
            pin = openmc.Cell(fill=trans_universe, region=-pin_boundary)
            print('Adding TRANS - ({}, {})'.format(x,y))
        elif i == reg_position[0] and j == reg_position[1]:
            pin = openmc.Cell(fill=reg_universe, region=-pin_boundary)
            print('Adding REG - ({}, {})'.format(x,y))
        elif i == water_position[0] and j == water_position[1]:
            pin = openmc.Cell(fill=water_universe, region=-pin_boundary)
            print('Adding WATER - ({}, {})'.format(x,y))
        elif i == 5:
            if j in fuel_outer_positions:
                pin = openmc.Cell(fill=fuel_element_universe, region=-pin_boundary)
                print('Adding FUEL')
            else:
                pin = openmc.Cell(fill=graphite_universe, region=-pin_boundary)
                print('Adding GRAPHITE')
        else:
            pin = openmc.Cell(fill=fuel_element_universe, region=-pin_boundary)
            print('Adding FUEL - ({}, {})'.format(x,y))

        pin.translation = (x, y, 0)
        pin.id = (i + 1)*100 + j
        core_cells.append(pin)


core_cells.append(water_cell)
core_universe = openmc.Universe(cells=core_cells)

##################################
#           CORE GEOMETRY        #
##################################

reactor_wall = openmc.ZCylinder(r=50.0, boundary_type='vacuum')
reactor_top = openmc.ZPlane(z0=0.0, boundary_type='vacuum')
reactor_bottom = openmc.ZPlane(z0=-114.3, boundary_type='vacuum')
reactor = openmc.Cell()
reactor.region = -reactor_wall & -reactor_top & +reactor_bottom
reactor.fill = core_universe
reactor_universe = openmc.Universe(cells=[reactor])

geometry = openmc.Geometry(reactor_universe)
geometry.export_to_xml()

###########################################################
#                           PLOTS                         #
###########################################################


if plot_rod_universes:
    # FUEL
    fuel_element_universe.plot(origin=(0.0, 0.0, -40), width=(5.0, 30.0), pixels=(600, 300), basis='xz', color_by='material', colors={fuel:'grey', Sm2O3: 'red', Al:'black', graphite:'yellow', water:'blue'})
    plt.savefig('images/fuel/close.png')
    plt.clf()
    fuel_element_universe.plot(origin=(0.0, 0.0, -40), width=(5.0, 100.0), pixels=(600, 300), basis='xz', color_by='material', colors={fuel:'grey', Sm2O3: 'red', Al:'black', graphite:'yellow', water:'blue'})
    plt.savefig('images/fuel/complete.png')
    plt.clf()

    # SHIM
    shim_universe.plot(origin=(0.0, 0.0, -40.), width=(7.0, 30.0), pixels=(600, 300), basis='xz', color_by='material', colors={B4C:'red', Al:'grey', water:'blue'})
    plt.savefig('images/shim/close.png')
    plt.clf()
    shim_universe.plot(origin=(0.0, 0.0, -40), width=(7.0, 80.0), pixels=(600, 300), basis='xz', color_by='material', colors={B4C:'red', Al:'grey', water:'blue'})
    plt.savefig('images/shim/complete.png')
    plt.clf()

    # TRANS
    trans_universe.plot(origin=(0.0, 0.0, -40), width=(7.0, 30.0), pixels=(600, 300), basis='xz', color_by='material', colors={B4C:'red', Al:'grey', water:'blue'})
    plt.savefig('images/trans/close.png')
    plt.clf()
    trans_universe.plot(origin=(0.0, 0.0, -40), width=(7.0, 80.0), pixels=(600, 300), basis='xz', color_by='material', colors={B4C:'red', Al:'grey', water:'blue'})
    plt.savefig('images/trans/complete.png')
    plt.clf()

    # REG
    reg_universe.plot(origin=(0.0, 0.0, -40), width=(7.0, 30.0), pixels=(600, 300), basis='xz', color_by='material', colors={B4C:'red', Al:'grey', water:'blue'})
    plt.savefig('images/reg/close.png')
    plt.clf()
    reg_universe.plot(origin=(0.0, 0.0, -40), width=(7.0, 80.0), pixels=(600, 300), basis='xz', color_by='material', colors={B4C:'red', Al:'grey', water:'blue'})
    plt.savefig('images/reg/complete.png')
    plt.clf()

if plot_geometry:
    """
    reactor_universe.plot(origin=(0,0,-40), width=(60,120), pixels=(500,500), basis='yz', color_by='material', colors={B4C:'red', fuel:'grey', Sm2O3: 'fuchsia', Al:'black', graphite:'yellow', water:'blue'})
    plt.savefig('images/core/side.png')
    plt.clf()
    """
    reactor_universe.plot(origin=(0,0, -30), width=(30,30), pixels=(500,500), basis='xy', color_by='cell')
    plt.savefig('images/core/top.png')
    plt.clf()


###########################################################
#                      RUN SIMULATION                     #
###########################################################

batches = 100
inactive = 10
particles = 10000

settings_file = openmc.Settings()
settings_file.batches = batches
settings_file.inactive = inactive
settings_file.particles = particles

bounds = [-28.527375, -28.527375, -28.527375, 28.527375, 28.527375, 28.527375]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings_file.source = openmc.Source(space=uniform_dist)

settings_file.export_to_xml()

openmc.run()
