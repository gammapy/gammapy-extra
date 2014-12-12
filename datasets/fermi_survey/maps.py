"""
This script prepares and bundles the input maps into a single 'all.fits' file, that can be
read by the gammapy-ts-image command line tool.
"""
from astropy.io import fits
import numpy as np

# Load data from files
counts = fits.getdata('../source_diffuse_separation/galactic_simulations/fermi_counts.fits')
background = fits.getdata('../source_diffuse_separation/galactic_simulations/fermi_diffuse.fits')[1:-1, :]
exposure = fits.getdata('../source_diffuse_separation/galactic_simulations/fermi_exposure_gal.fits')[0]

# Multiply with exposure to obtain a background counts image 
background = (background * exposure)

# Diffuse model is contained in background, so diffuse is set to zero
diffuse = np.zeros(background.shape)

# Write to fits
header = fits.getheader('../source_diffuse_separation/galactic_simulations/fermi_counts.fits')
maps = [counts, background, diffuse, exposure]
maps_names = ['On', 'Background', 'Diffuse', 'ExpGammaMap']

hdu_list = fits.HDUList()
for map_, name in zip(maps, maps_names):
    if name == 'On':
	hdu = fits.ImageHDU(data=map_, header=header, name=name)
    else:
	hdu = fits.ImageHDU(data=map_, header=header, name=name)
    hdu_list.append(hdu)
hdu_list.writeto('all.fits.gz')

# Convert and write 1FHL model map
hdu_list = fits.open('../source_diffuse_separation/galactic_simulations/FD_1FHL.fits')
hdu_list[1].data *= exposure
hdu_list.writeto('model.fits.gz')
