import logging as log
log.basicConfig(level=log.INFO)

import numpy as np

from astropy.wcs import WCS
from astropy.units import Quantity
from astropy.io import fits
from astropy.coordinates import SkyCoord

from gammapy.data import DataStore
from gammapy.cube import exposure_cube, SkyCube
from gammapy.utils.energy import EnergyBounds

dirname = '$GAMMAPY_EXTRA/datasets/hess-crab4-hd-hap-prod2'
log.info('Reading data from {}'.format(dirname))
data_store = DataStore.from_dir(dirname)
obs = data_store.obs(23523)

events = obs.events
log.info('Number of events in event list: {}'.format(len(events)))
log.info('Max. event energy: {}'.format(events['ENERGY'].max()))
log.info('Min. event energy: {}'.format(events['ENERGY'].min()))
aeff = obs.aeff

counts = SkyCube.empty(emin=0.5, emax=80, enumbins=8, eunit='TeV',
                            nxpix=200, nypix=200, xref=events.meta['RA_OBJ'],
                            yref=events.meta['DEC_OBJ'], dtype='int',
                            coordsys='CEL')

log.info('Bin events into cube.')
counts.fill_events(events)
log.info('Counts cube shape: {}'.format(counts.data.shape))
log.info('Number of events in cube: {}'.format(counts.data.sum()))
counts.write('counts.fits.gz', format='fermi-counts', clobber=True)

# Exposure cube
pointing = SkyCoord(events.meta['RA_PNT'], events.meta['DEC_PNT'], "icrs", unit="deg")
livetime = Quantity(events.meta['LIVETIME'], 's')
exposure = exposure_cube(pointing, livetime, aeff2d=aeff, ref_cube=counts,
                         offset_max=Quantity(2.5, 'deg'))
log.info('Exposure cube shape: {}'.format(exposure.data.shape))
log.info('Exposure unit: {}'.format(exposure.data.unit))
exposure.write('exposure.fits.gz', format='fermi-exposure', clobber=True)



