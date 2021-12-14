import openmc
import openmc.lib

from model import *
from utils import *


"""
# ALL IN
shim = convert_shim(130)
trans = convert_trans(53)
reg = convert_reg(116)
"""

"""
# ALL OUT
shim = convert_shim(835)
trans = convert_trans(926)
reg = convert_reg(821)
"""

"""
shim = convert_shim(556)
trans = convert_trans(433)
reg = convert_reg(503)
"""


##################################
#       REACTIVITY OF CRs        #
##################################
"""
# REACTIVITY OF REG
# REG ALL IN (others in)
shim = convert_shim(130)
trans = convert_trans(53)
reg = convert_reg(116)

make_TRIGA(shim,trans,reg, plot_core=False)
openmc.lib.init()
openmc.lib.run()
k_eff_reg_in = openmc.lib.keff()
openmc.lib.finalize()

# REG ALL OUT (others in)
shim = convert_shim(130)
trans = convert_trans(53)
reg = convert_reg(821)

make_TRIGA(shim,trans,reg, plot_core=False)
openmc.lib.init()
openmc.lib.run()
k_eff_reg_out = openmc.lib.keff()
openmc.lib.finalize()
"""
k_eff_reg_in = 0.9836626941765727
k_eff_reg_out = 0.9992017510911007

print('keff_reg_in: {}'.format(k_eff_reg_in))
print('keff_reg_out: {}'.format(k_eff_reg_out))

print('rho_in: {}'.format(reactivity(k_eff_reg_in)))
print('rho_out: {}'.format(reactivity(k_eff_reg_out)))
print('delta_rho: {}'.format(reactivity(k_eff_reg_out)-reactivity(k_eff_reg_in)))


order_folder()
