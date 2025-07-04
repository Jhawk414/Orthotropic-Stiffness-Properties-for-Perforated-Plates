"""
Purpose: This program calculates equivalent elastic properties for thick perforated plates with a square pentration pattern. 

It is based off Tables B.2 and 4.2 of Thomas Slot's 1972 dissertation titled "Stress Analysis of Thick Perforated Plates"

The subscript "p" denotes the in-plane directions—i.e., a Cartesian plane parallel with the the plate.

The subscript "z" denotes the transverse direction—i.e., the direction of the plate's thickness.

This program outputs the ratio of the orthotropic-to-isotropic stiffness—i.e., E_(p or z) / E, where E is the isotropic Elastic Modulus. For use in finite element analysis (FEA), you must multiply these calculated ratios by the material's Elastic (Young's) Modulus.
"""

import numpy as np
from scipy.interpolate import RectBivariateSpline
import matplotlib.pyplot as plt

# User-inputs. These are based off the perforated geometry
nu = 0.31
eta = 0.1114

# Axes
nu_array = np.array([0, 0.1, 0.2, 0.25, 0.3, 0.4, 0.5])
eta_array = np.array([0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.7])

# Do not change this data! From Table B.2 of (Slot 1972)
EpE_array = np.array([[0.1200, 0.1857, 0.2444, 0.3000, 0.3539, 0.4069, 0.5117, 0.6168, 0.8244],
                     [0.1207, 0.1866, 0.2455, 0.3012, 0.3552, 0.4082, 0.5132, 0.6183, 0.8253],
                     [0.1229, 0.1894, 0.2487, 0.3048, 0.3591, 0.4125, 0.5176, 0.6226, 0.8281],
                     [0.1246, 0.1916, 0.2512, 0.3076, 0.3622, 0.4157, 0.5210, 0.6259, 0.8303],
                     [0.1267, 0.1943, 0.2511, 0.3111, 0.3659, 0.4197, 0.5253, 0.6300, 0.8329],
                     [0.1324, 0.2015, 0.2627, 0.3203, 0.3759, 0.4302, 0.5363, 0.6407, 0.8396],
                     [0.1406, 0.2116, 0.2742, 0.3330, 0.3895, 0.4445, 0.5512, 0.6549, 0.8483]])

# Finds curve fit (returns function)
intrp = RectBivariateSpline(nu_array, eta_array, EpE_array)

EpE = intrp(nu, eta); # Interpolates at user-input nu & eta

print('Ep*/E = ', EpE[0])

fig, ax = plt.subplots(); fig.suptitle('Ep*/E');
plt.grid()
plt.xlim(0.0, 0.75); plt.ylim(0.1, 0.85)
plt.xlabel('Ligament Efficiency, η'); plt.ylabel('Eₚ*/E')
ax.legend(labels=nu_array, loc='lower right', title='ν =')

for v in range(len(nu_array)):
    ax.plot(eta_array, EpE_array[v,:])