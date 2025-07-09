"""
Purpose: This program calculates equivalent elastic properties for thick perforated plates with a square pentration pattern. 

It is based off Tables B.2 and 4.2 of Thomas Slot's 1972 dissertation titled "Stress Analysis of Thick Perforated Plates"

The subscript "p" denotes the in-plane directions—i.e., a Cartesian plane parallel with the the plate.

The subscript "z" denotes the transverse direction—i.e., the direction of the plate's thickness.

This program outputs the ratio of the orthotropic-to-isotropic stiffness—i.e., E_(p or z) / E, where E is the isotropic Elastic Modulus. For use in finite element analysis (FEA), you must multiply these calculated ratios by the material's Elastic (Young's) Modulus.
"""

import numpy as np
from scipy.interpolate import RectBivariateSpline
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt

# User-inputs. These are based off the perforated geometry.
nu = 0.31 # Poisson's Ratio
eta = 0.1114 # Ligament Efficiency

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

vp_array = np.array([[0.0264, 0.0399, 0.0511, 0.0606, 0.0688, 0.0754, 0.0830, 0.0814, 0.0502],
               [0.0354, 0.0551, 0.0721, 0.0873, 0.1010, 0.1132, 0.1317, 0.1411, 0.1316],
               [0.0386, 0.0637, 0.0866, 0.1078, 0.1275, 0.1455, 0.1760, 0.1974, 0.2115],
               [0.0379, 0.0656, 0.0914, 0.1158, 0.1386, 0.1599, 0.1966, 0.2244, 0.2510],
               [0.0356, 0.0657, 0.0946, 0.1222, 0.1484, 0.1730, 0.2165, 0.2509, 0.2903],
               [0.0259, 0.0606, 0.0960, 0.1307, 0.1641, 0.1960, 0.2538, 0.3023, 0.3685],
               [0.0080, 0.0474, 0.0901, 0.1328, 0.1745, 0.2145, 0.2883, 0.3523, 0.4468]])

GpG_array = np.array([[0.0068, 0.0207, 0.0413, 0.0695, 0.1061, 0.1514, 0.2691, 0.4177, 0.7450],
                     [0.0075, 0.0227, 0.0453, 0.0760, 0.1154, 0.1641, 0.2882, 0.4411, 0.7627],
                     [0.0082, 0.0247, 0.0492, 0.0823, 0.1246, 0.1764, 0.3064, 0.4626, 0.7781],
                     [0.0085, 0.0257, 0.0511, 0.0854, 0.1291, 0.1824, 0.3152, 0.4728, 0.7850],
                     [0.0088, 0.0267, 0.0531, 0.0886, 0.1336, 0.1883, 0.3237, 0.4826, 0.7916],
                     [0.0095, 0.0287, 0.0569, 0.0947, 0.1424, 0.1999, 0.3401, 0.5011, 0.8035],
                     [0.0102, 0.0307, 0.0608, 0.1008, 0.1511, 0.2112, 0.3558, 0.5183, 0.8142]])

eta_z_array = np.array([0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

EzE_array = np.array([0.2146, 0.2912, 0.3638, 0.4326, 0.4974, 0.5582, 0.6152, 0.7173, 0.8037, 0.8743, 0.9293, 0.9686, 0.9922, 1.0000])
GzG_array = np.array([0.0000, 0.1260, 0.1965, 0.2607, 0.3221, 0.3822, 0.4415, 0.5585, 0.6716, 0.7767, 0.8680, 0.9391, 0.9844, 1.0000])

# Finds curve fit (returns function to be called)
intrp_Ep = RectBivariateSpline(nu_array, eta_array, EpE_array, kx=4, ky=4) #4th order polynomial found to have R² = 1 in Excel.
intrp_vp = RectBivariateSpline(nu_array, eta_array, vp_array, kx=4, ky=4)
intrp_GpG = RectBivariateSpline(nu_array, eta_array, GpG_array, kx=4, ky=4)


intrp_EzE = make_interp_spline(eta_z_array, EzE_array, k=2) #Quadratic order polynomial found to have R² = 1 in Excel.
intrp_GzG = make_interp_spline(eta_z_array, GzG_array, k=2)


# Interpolates at user-input nu & eta
EpE = intrp_Ep(nu, eta)
vp = intrp_vp(nu, eta)
GpG = intrp_GpG(nu, eta)

# Print outputs to console
print('Ep*/E = ', EpE[0])
print('ν_p* = ', vp[0])
print('Gp*/G = ', GpG[0])

# Plot Eₚ*/E
fig, ax = plt.subplots(); fig.suptitle('Eₚ*/E');
plt.grid()
plt.xlim(0.0, 0.75); plt.ylim(0.1, 0.85)
plt.xlabel('Ligament Efficiency, η'); plt.ylabel('Eₚ*/E')

for v in range(len(nu_array)):
    ax.plot(eta_array, EpE_array[v,:])

ax.legend(labels=nu_array, loc='lower right', title='ν =')
