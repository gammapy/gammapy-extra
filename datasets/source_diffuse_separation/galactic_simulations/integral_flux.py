"""Produces an integral flux image of the Fermi Diffuse image between 10 and 500 GeV
Note: This step can take more than 10 hours to run for the all sky cube.
"""

from gammapy.data import spectral_cube
from astropy.units import Quantity

diffuse = spectral_cube.SpectralCube.read('gll_iem_v05_rev1.fit')
energy_band = Quantity([10, 500], 'GeV')
integral_diffuse = diffuse.integral_flux_image(energy_band)
image_hdu = diffuse.to_fits()[0]

# Return values as can't save hdu with Quantities
image_hdu.data = image_hdu.data.value
image_hdu.writeto('fermi_diffuse.fits', clobber=True)
