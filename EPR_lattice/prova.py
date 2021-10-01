import numpy as np

originale = np.matrix([
                        [1,4],
                        [1,1]])

flip_down = np.flip(originale,0)
flip_left = np.flip(originale,1)
flip_diag = np.flip(flip_left,0)


completa = np.block([[flip_left,originale],[flip_diag,flip_down]])
print(completa)
