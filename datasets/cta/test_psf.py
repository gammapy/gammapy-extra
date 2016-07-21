from gammapy.irf import EnergyDependentMultiGaussPSF

irf_path = 'perf_prod2/South_5h/irf_file.fits.gz'

psf = EnergyDependentMultiGaussPSF.read(irf_path, hdu='POINT SPREAD FUNCTION')

psf.peek()


