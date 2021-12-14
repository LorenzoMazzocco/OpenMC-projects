import shutil

# order the folder from xml files
def order_folder():
    shutil.move("materials.xml", "model_xml/materials.xml")
    shutil.move("geometry.xml", "model_xml/geometry.xml")
    shutil.move("settings.xml", "model_xml/settings.xml")

    shutil.move("summary.h5", "output/summary.h5")
    shutil.move("statepoint.1000.h5", "output/statepoint.1000.h5")


# the convertion funcitons take as input the displayed level of the control rods and return the position in cm
# to adjust the model

def convert_shim(x):
    z = (38.1/(835-130))*(x-130) # 835 ALL OUT
    return z                     # 130 ALL IN

def convert_trans(x):
    z = (47.2/(926-53))*(x-53)   # 926 ALL OUT
    return z                     # 53 ALL IN

def convert_reg(x):
    z = (38.1/(821-116))*(x-116) # 821 ALL OUT
    return z                     # 116 ALL IN




# compute reactivity in dollars
def reactivity(k_eff):
    beta_eff = 0.0073
    rho = (k_eff-1)/k_eff
    return rho/beta_eff
