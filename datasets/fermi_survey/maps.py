from astropy.io import fits

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
    hdu = fits.ImageHDU(data=map_, header=header, name=name)
    hdu_list.append(hdu)
hdu_list.writeto('all.fits')

# Convert and write 1FHL model map
hdu_list = fits.open('../source_diffuse_separation/galactic_simulations/FD_1FHL.fits')
hdu_list[1].data *= exposure
hdu_list.writeto('model.fits')
