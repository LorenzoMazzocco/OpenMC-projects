import openmc

from model import *
from bin import *

shim = convert_shim(556)
reg = convert_reg(116)
trans = convert_trans(926)

print('SHIM: {}'.format(shim))
print('REG: {}'.format(reg))
print('TRANS: {}'.format(trans))

make_TRIGA(0,0,0)
openmc.run()
order_folder()
