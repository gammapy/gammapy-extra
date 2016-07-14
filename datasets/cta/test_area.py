from astropy.table import Table
from astropy import units as u

from gammapy.utils.fits import get_hdu
from gammapy.irf import EffectiveAreaTable2D

import matplotlib.pyplot as plt

irf_path = 'perf_prod2/South_5h/irf_file.fits.gz'

table_hdu_area = get_hdu(irf_path + '[EFFECTIVE AREA]')
table_area = Table(table_hdu_area.data)

# Needed fix
table_area['ENERG_LO'].unit = u.TeV
table_area['ENERG_HI'].unit = u.TeV
table_area['THETA_LO'].unit = u.deg
table_area['THETA_HI'].unit = u.deg
table_area['EFFAREA'].unit = u.m * u.m
table_area['EFFAREA_RECO'].unit = u.m * u.m
# End

eff_area_2d = EffectiveAreaTable2D.from_table(table_area)
eff_area = eff_area_2d.to_effective_area_table(offset=0.5 * u.deg)

plt.figure('AREA')
ax = eff_area.plot()
ax.set_yscale('log')
plt.show(block=False)


