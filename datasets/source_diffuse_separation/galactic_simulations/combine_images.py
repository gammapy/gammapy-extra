"""Adds source and diffuse contributions together to return a total image
"""

from astropy.io import fits

diffuse = fits.open('fermi_diffuse.fits')[0]
source = fits.open('Image_1FHL.fits')[0]

total = diffuse
total.data = diffuse.data + source.data

total.writeto('FD_1FHL.fits')
