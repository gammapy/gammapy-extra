# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
import logging

import os
from pathlib import Path

import astropy.units as u
from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS

log = logging.getLogger(__name__)

KEEP = ['Significance', 'SignificanceExtended', 'On', 'Off',
        'OnCorrelated', 'Background', 'BackgroundCorrelated',
        'ExpGammaMap', 'Alpha', 'AlphaCorrelated', 'OnExposure',
        'OffExposure', 'Exclusion']

filename = Path(os.environ['HGPS_DATA']) / 'hap_output_all.fits.gz'
hdu_list = fits.open(str(filename))

#Filter HDU list
for name in [_.name for _ in hdu_list]:
    if not name in KEEP:
        del hdu_list[name]

# Make cutouts
hdu_list_cutout = fits.HDUList()
size = (5 * u.deg, 5 * u.deg)
position = SkyCoord(252, 1, frame='galactic', unit='deg')

for hdu in hdu_list:
    wcs = WCS(hdu.header)
    header = hdu.header.copy()
    
    cutout = Cutout2D(hdu.data, position, size, wcs=wcs, copy=True)

    position_pix = wcs.wcs_world2pix(position.l.value, position.b.value, 1)    
    
    # Update header information
    cutout_header = {'NAXIS1': cutout.shape[1],
                     'NAXIS2': cutout.shape[0],
                     'CRPIX1': (cutout.shape[1] + 1) / 2,
                     'CRPIX2': (cutout.shape[0] + 1) / 2,
                     'CRVAL1': position.l.value,
                     'CRVAL2': position.b.value}
    value = cutout.data[cutout.shape[0] // 2, cutout.shape[1] // 2]
    value_ref = hdu.data[int(position_pix[1]), int(position_pix[0])]  
    assert value == value_ref

    header.update(cutout_header)
    cutout_hdu = fits.ImageHDU(data=cutout.data, header=header, name=hdu.name)
    hdu_list_cutout.append(cutout_hdu)

output_filename = 'hess_survey_snippet.fits.gz'
log.info('Writing {}'.format(output_filename))
hdu_list_cutout.writeto(output_filename, clobber=True)

