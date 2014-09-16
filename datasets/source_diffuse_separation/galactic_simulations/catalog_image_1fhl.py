"""Produces an image from 1FHL catalog point sources.
"""
from gammapy.datasets import FermiGalacticCenter
from gammapy.image import make_empty_image, catalog_image

# Create image of defined size
reference = make_empty_image(nxpix=3600, nypix=1800, binsz=0.1)
psf_file = FermiGalacticCenter.psf()

# Create image
image = catalog_image(reference, psf, catalog='1FHL', source_type='point',
                  total_flux='True')
hdu = image.to_fits()[0]
hdu.writeto('Image_1FHL.fits', clobber=True)

