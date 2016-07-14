from astropy import units as u

from gammapy.utils.fits import get_hdu
from gammapy.irf import EnergyDispersion2D

import matplotlib.pyplot as plt

irf_path = 'perf_prod2/South_5h/irf_file.fits.gz'

table_hdu_disp = get_hdu(irf_path + '[ENERGY DISPERSION]')
e_disp_2d = EnergyDispersion2D.from_fits(table_hdu_disp)
# Theta values are weird, nedd to be investiguated:
# THETA_LO: 0., 4.5
# THETA_HI: 4.5, 9.0
e_disp = e_disp_2d.to_energy_dispersion(offset=4.5 * u.deg)

#plt.figure('edisp')
#e_disp.plot_matrix()
#plt.show()
