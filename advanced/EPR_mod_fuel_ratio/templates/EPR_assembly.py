import openmc
import shutil


class EPR_assembly():

    #############################################################################################
    #                                        CLASS ATTRIBUTES
    #############################################################################################

    #fuel variables
    No_BA_fuel_enrichment = 3.0
    BA_fuel_enrichment = 0.25
    BA_percentage = 8.0

    #geometric variables
    pin_fuel_or = 0.3975
    channel_clad_ir = 0.5725
    pitch = 1.26


    ####################################################################################################################################################
    #                                                                CLASS METHODS
    ####################################################################################################################################################

    def __init__(self, config=20, complete=False):

        self.create_materials()
        self.create_geometry(config)
        if complete:
            self.complete_geometry.export_to_xml(path='geometry.xml')
            self.geometry = self.complete_geometry
        else:
            self.partial_geometry.export_to_xml(path='geometry.xml')
            self.geometry = self.partial_geometry


    #############################################################################################
    #                                        MATERIALS
    #############################################################################################


    def create_materials(self):
        UO2_BA = openmc.Material(name='UO2_BA')
        UO2_BA.add_element('U', 1.0, enrichment=self.BA_fuel_enrichment)
        UO2_BA.add_element('O', 2.0)
        UO2_BA.set_density('g/cc', 10.3070)

        # uranium dioxide No_BA
        fuel_No_BA = openmc.Material(name='fuel_No_BA')
        fuel_No_BA.add_element('U', 1.0, enrichment=self.No_BA_fuel_enrichment)
        fuel_No_BA.add_element('O', 2.0)
        fuel_No_BA.set_density('g/cc', 10.3070)

        # gadolinium oxide
        Gd2O3 = openmc.Material(name='Gd2O3')
        Gd2O3.add_element('Gd', 2.0)
        Gd2O3.add_element('O', 3.0)
        Gd2O3.set_density('g/cc', 7.41)

        # cladding alloy (M5)
        M5 = openmc.Material(name='M5')
        M5.add_element('Zr', 0.98875, percent_type='wo')
        M5.add_element('Nb', 0.01, percent_type='wo')
        M5.add_element('O', 0.00125, percent_type='wo')
        M5.set_density('g/cc', 6.55)

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

        #Mixtures
        fuel_BA = openmc.Material.mix_materials([UO2_BA, Gd2O3], [1-0.01*self.BA_percentage, 0.01*self.BA_percentage], 'wo', name='fuel_BA')

        #openmc object to export
        self.materials = openmc.Materials([UO2_BA, Gd2O3, M5, He, H2O, fuel_BA, fuel_No_BA])
        self.materials.export_to_xml(path='materials.xml')

        #create material attributes used by create_geometry() method
        self.UO2_BA = UO2_BA
        self.Gd2O3 = Gd2O3
        self.M5 = M5
        self.He = He
        self.H2O = H2O
        self.fuel_BA = fuel_BA
        self.fuel_No_BA = fuel_No_BA

    #############################################################################################
    #                                        GEOMETRY
    #############################################################################################

    def create_geometry(self, config):

        pin_fuel_or = self.pin_fuel_or
        pin_clad_ir = pin_fuel_or + 0.0150
        pin_clad_or = pin_clad_ir + 0.0625

        self.pin_clad_ir = pin_clad_ir
        self.pin_clad_or = pin_clad_or

        channel_clad_ir = self.channel_clad_ir
        channel_clad_or = channel_clad_ir + 0.0400

        #pin surfaces
        pin_fuel_or = openmc.ZCylinder(r=pin_fuel_or)
        pin_clad_ir = openmc.ZCylinder(r=pin_clad_ir)
        pin_clad_or = openmc.ZCylinder(r=pin_clad_or)

        #channel surfaces
        channel_clad_or = openmc.ZCylinder(r=channel_clad_or)
        channel_clad_ir = openmc.ZCylinder(r=channel_clad_ir)

        #FUEL_BA PIN UNIVERSE
        fuel_BA_cell = openmc.Cell(fill=self.fuel_BA, region=-pin_fuel_or)
        gap_BA_cell = openmc.Cell(fill=self.He, region= +pin_fuel_or & -pin_clad_ir)
        clad_BA_cell = openmc.Cell(fill=self.M5, region= +pin_clad_ir & -pin_clad_or)
        water_BA_cell = openmc.Cell(fill=self.H2O, region= +pin_clad_or)

        b = openmc.Universe(cells=[fuel_BA_cell, gap_BA_cell, clad_BA_cell, water_BA_cell])

        #FUEL_No_BA PIN UNIVERSE
        fuel_No_BA_cell = openmc.Cell(fill=self.fuel_No_BA, region=-pin_fuel_or)
        gap_No_BA_cell = openmc.Cell(fill=self.He, region= +pin_fuel_or & -pin_clad_ir)
        clad_No_BA_cell = openmc.Cell(fill=self.M5, region= +pin_clad_ir & -pin_clad_or)
        water_No_BA_cell = openmc.Cell(fill=self.H2O, region= +pin_clad_or)

        f = openmc.Universe(cells=[fuel_No_BA_cell, gap_No_BA_cell, clad_No_BA_cell, water_No_BA_cell])

        #CHANNEL UNIVERSE
        in_channel_cell = openmc.Cell(fill=self.H2O, region=-channel_clad_ir)
        channel_clad_cell = openmc.Cell(fill=self.M5, region= +channel_clad_ir & -channel_clad_or)
        out_channel_cell = openmc.Cell(fill=self.H2O, region=+channel_clad_or)

        c = openmc.Universe(cells=[in_channel_cell, channel_clad_cell, out_channel_cell])

        #OUTER UNIVERSE
        all_water_cell = openmc.Cell(fill=self.H2O)
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

        configurations = {'8':config_8, '12':config_12, '16':config_16, '20':config_20}

        configuration = configurations['{}'.format(config)]

        #CREATE THE LATTICE
        lattice = openmc.RectLattice()
        lattice.lower_left = (-17*self.pitch/2, -17*self.pitch/2)
        lattice.pitch = (self.pitch,self.pitch)
        lattice.outer = outer_universe
        lattice.universes= configuration['lattice']

        #===================================COMPLETE GEOMETRY

        #boundaries
        left = openmc.XPlane(x0=-17*self.pitch/2, boundary_type='reflective')
        right = openmc.XPlane(x0=17*self.pitch/2, boundary_type='reflective')
        bottom = openmc.YPlane(y0=-17*self.pitch/2, boundary_type='reflective')
        top = openmc.YPlane(y0=17*self.pitch/2, boundary_type='reflective')

        main_cell = openmc.Cell(fill=lattice, region=+left & -right & +bottom & -top)
        self.complete_geometry = openmc.Geometry([main_cell])


        #===================================PARTIAL GEOMETRY

        #boundaries
        left = openmc.XPlane(x0=0, boundary_type='reflective')
        right = openmc.XPlane(x0=17*self.pitch/2, boundary_type='reflective')
        bottom = openmc.YPlane(y0=0, boundary_type='reflective')
        top = openmc.YPlane(y0=17*self.pitch/2, boundary_type='reflective')

        main_cell = openmc.Cell(fill=lattice, region=+left & -right & +bottom & -top)
        self.partial_geometry = openmc.Geometry([main_cell])



    #############################################################################################
    #                                        PLOTS
    #############################################################################################


    def plot_geometry(self, complete=False):

        #top view
        geom_plot_top = openmc.Plot().from_geometry(self.geometry)
        geom_plot_top.basis = 'xy'
        geom_plot_top.origin = (0., 0., 0.)
        geom_plot_top.width = (17*self.pitch, 17*self.pitch)
        geom_plot_top.pixels = (1500, 1500)
        geom_plot_top.color_by = 'material'
        geom_plot_top.colors = {self.fuel_No_BA: (255,255,153), self.fuel_BA:(255,153,255), self.He:'green', self.M5:'grey', self.H2O:(102,178,255)}
        geom_plot_top.filename = 'model_plots/top_view'

        #side view
        geom_plot_side = openmc.Plot().from_geometry(self.geometry)
        geom_plot_side.basis = 'xz'
        geom_plot_side.origin = (0., 0., 0.)
        geom_plot_side.width = (17*self.pitch, 17*self.pitch)
        geom_plot_side.pixels = (1500, 1500)
        geom_plot_side.color_by = 'material'
        geom_plot_side.colors = {self.fuel_No_BA: (255,255,153), self.fuel_BA:(255,153,255), self.He:'green', self.M5:'grey', self.H2O:(102,178,255)}
        geom_plot_side.filename = 'model_plots/side_view'

        plots = openmc.Plots([geom_plot_top, geom_plot_side])
        plots.export_to_xml(path='plots.xml')
        openmc.plot_geometry()


    def set_pitch(self, new_pitch):
        self.pitch = new_pitch

    def set_fuel_or(self, new_fuel_or):
        self.pin_fuel_or = new_fuel_or

    def set_channel_clad_ir(self, new_channel_clad_ir):
        self.channel_clad_ir = new_channel_clad_ir
