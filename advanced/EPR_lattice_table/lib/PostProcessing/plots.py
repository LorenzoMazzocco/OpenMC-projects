import matplotlib.pyplot as plt
import numpy as np
import string



##################################################################
#                        LATTICE PLOT                            #
##################################################################

def lattice_plot(lattice_data,title,filename, colormap):
    lattice_dim=lattice_data.shape[0]

    color_map = plt.cm.get_cmap(colormap).copy()
    color_map.set_bad(color='black')

    plt.figure(figsize=(12, 12))
    plt.imshow(lattice_data,cmap = color_map, origin='lower', extent=[0,17,0,17])
    plt.hlines(np.arange(1,17), 0,17, color='black', linewidth=1.5)
    plt.vlines(np.arange(1,17), 0,17, color='black', linewidth=1.5)
    for index, value in np.ndenumerate(lattice_data) :
        plt.text(0.5+index[0],0.6+index[1],'{:.2e}'.format(value)[:4], size=9, weight='bold', ha='center', va='center')
        plt.text(0.5+index[0],0.25+index[1],'{:.2e}'.format(value)[4:], size=7, weight='bold', ha='center', va='center')
    plt.xticks(np.arange(0.5,17.5,1), list(string.ascii_uppercase)[0:17], size=15, weight='bold')
    plt.yticks(np.arange(0.5,17.5,1), np.arange(1,18), size=15, weight='bold')
    plt.title(title,fontsize=20, weight='bold', pad = 40)
    plt.colorbar()
    plt.savefig("images/{}.png".format(filename), dpi=700)
    plt.clf()



##################################################################
#                           MESH PLOT                            #
##################################################################

def mesh_plot(mesh_data,title,filename, neutrons_per_batch, extent, cmap='coolwarm'):
    mesh_shape=np.shape(mesh_data)
    plt.imshow(mesh_data, cmap=cmap, origin='lower', extent = extent)
    plt.suptitle(title,fontsize=14)
    plt.title('mesh size: [{},{}]   |   neutrons/batch: {}'.format(mesh_shape[0],mesh_shape[1],neutrons_per_batch),fontsize=10)
    plt.xlabel('Distance from center [cm]')
    plt.ylabel('Distance from center [cm]')
    plt.colorbar()
    plt.savefig("images/mesh_plots/{}.png".format(filename), dpi=700)
    plt.clf()



##################################################################
#                         RADIAL PLOT                            #
##################################################################

def plot_radially(radial_data, ylabel, title, filename, horizontal_dimension, neutrons_per_batch, alpha=0.5, diag=False):
    if diag:
        geom_image = mpimg.imread('images/geometry/side_view_diag.ppm')
        directory = 'diagonal'
        dimension = math.sqrt(2)*horizontal_dimension
    else:
        geom_image = mpimg.imread('images/geometry/side_view_partial.ppm')
        directory = 'horizontal'
        dimension = horizontal_dimension
    fig, axs = plt.subplots(2,1, sharex=True,sharey=True, figsize=(15,10))
    fig.suptitle('{}'.format(title), fontsize=19)
    axs[0].set_title('mesh size: [{},{}]   |   neutrons/batch: {}'.format(len(radial_data),len(radial_data),neutrons_per_batch),fontsize=14, pad=30)
    axs[0].plot(np.linspace(0,dimension/2,len(radial_data)),radial_data, 'r-', linewidth=1.5)
    axs[1].imshow(geom_image, alpha=alpha, origin='lower', extent=[0,dimension/2,0,1.2*max(radial_data)])
    axs[1].plot(np.linspace(0,dimension/2,len(radial_data)), radial_data,'r-', linewidth=1.5)
    axs[1].xaxis.tick_top()
    axs[1].xaxis.set_label_position('top')
    axs[1].set_xlabel('Radial distance from center [cm]')
    axs[1].set_aspect('auto')
    for ax in axs:
        ax.set_ylabel('{}'.format(ylabel))
    plt.savefig("images/radial_plots/{}/{}.png".format(directory,filename), dpi=700)
    plt.clf()
