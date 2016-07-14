from gammapy.utils.fits import get_hdu
from gammapy.background import Cube

import matplotlib.pyplot as plt

irf_path = 'perf_prod2/South_5h/irf_file.fits.gz'

table_hdu_bg = get_hdu(irf_path + '[BACKGROUND]')
# Need to fix that
table_hdu_bg.header['TTYPE7'] = 'Bgd'
table_hdu_bg.header['TUNIT7'] = '1 / (MeV s sr)'
#

cube_bg = Cube.from_fits_table(table_hdu_bg, scheme='bg_cube')

### Bkg integrated on the entire FOV
bkg_rate_diff = cube_bg.integral_images
delta_energy = cube_bg.energy_edges[1:] - cube_bg.energy_edges[:-1]
bkg_rate = bkg_rate_diff * delta_energy.to('MeV')

plt.figure('bkg rate')
plt.plot(cube_bg.energy_edges.log_centers.to('TeV'),
         bkg_rate, 'o', drawstyle='default')
plt.axis([1.e-2, 1.e3, 1.e-8, 1.e2])
plt.loglog()
plt.show(block=False)

