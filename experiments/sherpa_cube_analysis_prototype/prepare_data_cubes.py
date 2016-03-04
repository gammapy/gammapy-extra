import logging as log
log.basicConfig(level=log.INFO)

import numpy as np

from astropy.wcs import WCS
from astropy.units import Quantity
from astropy.io import fits
from astropy.coordinates import SkyCoord

from gammapy.data import DataStore
from gammapy.image import bin_events_in_cube
from gammapy.cube import exposure_cube, SpectralCube
from gammapy.utils.energy import EnergyBounds

dirname = '$GAMMAPY_EXTRA/datasets/hess-crab4-hd-hap-prod2'
log.info('Reading data from {}'.format(dirname))
data_store = DataStore.from_dir(dirname)

events = data_store.load(obs_id=23523, filetype='events')
log.info('Number of events in event list: {}'.format(len(events)))
log.info('Max. event energy: {}'.format(events['ENERGY'].max()))
log.info('Min. event energy: {}'.format(events['ENERGY'].min()))
aeff = data_store.load(obs_id=23523, filetype='aeff')

# Define WCS reference header
refheader = fits.Header()
refheader['WCSAXES'] = 3
refheader['NAXIS'] = 3
refheader['CRPIX1'] = 100.5
refheader['CRPIX2'] = 100.5
refheader['CRPIX3'] = 1.0
refheader['CDELT1'] = -0.02
refheader['CDELT2'] = 0.02

# shouldn't matter, but must contain sufficient number of digits,
# so that CDELT1 and CDELT2 are not truncated, when wcs.to_header() is called
# seems to be a bug...
refheader['CDELT3'] = 2.02  

refheader['CTYPE1'] = 'RA---CAR'
refheader['CTYPE2'] = 'DEC--CAR'
refheader['CTYPE3'] = 'log_Energy'  # shouldn't matter
refheader['CUNIT1'] = 'deg'
refheader['CUNIT2'] = 'deg'
refheader['CRVAL1'] = events.meta['RA_OBJ']
refheader['CRVAL2'] = events.meta['DEC_OBJ']
refheader['CRVAL3'] = 10.0  # shouldn't matter

energies = EnergyBounds.equal_log_spacing(0.5, 80, 8, 'TeV')
data = Quantity(np.zeros((len(energies), 200, 200)))
wcs = WCS(refheader)
refcube = SpectralCube(data, wcs, energy=energies)

# Counts cube
log.info('Bin events into cube.')
counts_hdu = bin_events_in_cube(events, refcube, energies)
counts = SpectralCube(Quantity(counts_hdu.data, 'count'), wcs, energies)
log.info('Counts cube shape: {}'.format(counts_hdu.shape))
log.info('Number of events in cube: {}'.format(counts_hdu.data.sum()))
counts.writeto('counts.fits', clobber=True)

# Exposure cube
pointing = SkyCoord(events.meta['RA_PNT'], events.meta['DEC_PNT'], "icrs", unit="deg")
livetime = Quantity(events.meta['LIVETIME'], 's')
exposure = exposure_cube(pointing, livetime, aeff2d=aeff, ref_cube=counts,
                         offset_max=Quantity(2.5, 'deg'))
log.info('Exposure cube shape: {}'.format(exposure.data.shape))
log.info('Exposure unit: {}'.format(exposure.data.unit))
exposure.writeto('exposure.fits', clobber=True)



