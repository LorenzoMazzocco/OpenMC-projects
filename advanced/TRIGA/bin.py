import shutil

def order_folder():
    shutil.move("materials.xml", "model_xml/materials.xml")
    shutil.move("geometry.xml", "model_xml/geometry.xml")
    shutil.move("settings.xml", "model_xml/settings.xml")

    shutil.move("summary.h5", "output/summary.h5")
    shutil.move("statepoint.100.h5", "output/statepoint.100.h5")


# the convertion funcitons take as input the displayed level of the control rods and return the position in cm
# to adjust the model

def convert_shim(x):
    z = (38.1/(835-130))*(x-130)
    return z

def convert_trans(x):
    z = (38.1/(926-53))*(x-53)
    return z

def convert_reg(x):
    z = (38.1/(821-116))*(x-116)
    return z
