# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Simulate test dataset.
"""
from __future__ import print_function, division
import json
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.modeling.models import Gaussian2D, Const2D
from gammapy.utils.random import get_random_state
from gammapy.image import SkyImageList, SkyImage
from gammapy.scripts.image_ts import image_ts_main


def make_psf(psf_sigma):
    psf_fwhm = psf_sigma * 2 * np.sqrt(2 * np.log(2))
    psf = {}
    psf['psf1'] = {'ampl': 1, 'fwhm': psf_fwhm}
    psf['psf2'] = {'ampl': 0, 'fwhm': 1E-5}
    psf['psf3'] = {'ampl': 0, 'fwhm': 1E-5}

    filename = 'psf.json'
    print('Writing {}'.format(filename))
    with open(filename, 'w') as f:
        json.dump(psf, f, indent=4)


def make_images(psf_sigma):
    # Define width of the source and the PSF
    source_sigma = 4
    sigma = np.sqrt(psf_sigma ** 2 + source_sigma ** 2)
    amplitude = 1E3 / (2 * np.pi * sigma ** 2)

    source = Gaussian2D(amplitude, 99, 99, sigma, sigma)
    background = Const2D(1)
    model = source + background

    # Define data shape
    shape = (200, 200)
    y, x = np.indices(shape)

    # Create a new WCS object
    wcs = WCS(naxis=2)

    # Set up an Galactic projection
    wcs.wcs.crpix = [100.5, 100.5]
    wcs.wcs.cdelt = np.array([0.02, 0.02])
    wcs.wcs.crval = [0, 0]
    wcs.wcs.ctype = ['GLON-CAR', 'GLAT-CAR']

    # Fake data
    random_state = get_random_state(0)
    data = random_state.poisson(model(x, y))

    # Save data
    header = wcs.to_header()

    hdu = fits.PrimaryHDU(data=data.astype('int32'), header=header)
    filename = 'counts.fits.gz'
    print('Writing {}'.format(filename))
    hdu.writeto(filename, clobber=True)

    hdu = fits.PrimaryHDU(data=model(x, y).astype('float32'), header=header)
    filename = 'model.fits.gz'
    print('Writing {}'.format(filename))
    hdu.writeto(filename, clobber=True)

    hdu = fits.PrimaryHDU(data=background(x, y).astype('float32'), header=header)
    filename = 'background.fits.gz'
    print('Writing {}'.format(filename))
    hdu.writeto(filename, clobber=True)

    hdu = fits.PrimaryHDU(data=source(x, y).astype('float32'), header=header)
    filename = 'source.fits.gz'
    print('Writing {}'.format(filename))
    hdu.writeto(filename, clobber=True)

    exposure = 1E12 * np.ones(shape)
    hdu = fits.PrimaryHDU(data=exposure.astype('float32'), header=header)
    filename = 'exposure.fits.gz'
    print('Writing {}'.format(filename))
    hdu.writeto(filename, clobber=True)


def make_images_grouped():
    images = SkyImageList([
        SkyImage.read('counts.fits.gz'),
        SkyImage.read('background.fits.gz'),
        SkyImage.read('exposure.fits.gz'),
    ])
    images[0].name = 'counts'
    images[1].name = 'background'
    images[2].name = 'exposure'

    filename = 'input_all.fits.gz'
    print('Writing {}'.format(filename))
    images.write(filename, clobber=True)


def make_ts_image(scale):
    filename = 'expected_ts_{}.fits.gz'.format(scale)
    args = ['input_all.fits.gz', filename, "--psf", 'psf.json', "--scales", scale, '--overwrite']
    print('Executing command: gammapy-image-ts {}'.format(' '.join(args)))
    print('Writing {}'.format(filename))
    image_ts_main(args)


def make_ts_image(scale):
    filename = 'expected_ts_{}.fits.gz'.format(scale)
    args = ['input_all.fits.gz', filename, "--psf", 'psf.json', "--scales", scale, '--overwrite']
    print('Executing command: gammapy-image-ts {}'.format(' '.join(args)))
    print('Writing {}'.format(filename))
    image_ts_main(args)

if __name__ == '__main__':
    psf_sigma = 3

    make_psf(psf_sigma)
    make_images(psf_sigma)
    make_images_grouped()

    scales = ['0.000', '0.050', '0.100', '0.200']
    for scale in scales:
        make_ts_image(scale)
