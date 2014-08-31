"""Make simulated gamma-ray source catalogs for the
gammapy-viewer experiment.
"""
from gammapy.astro import population

def make_snr_catalog():
	"""A catalog of supernova remnants distributed in a disk.
	"""
	table = population.make_base_catalog_galactic(n_sources=1000)
	table = population.add_snr_parameters(table)
	table = table[table['L_SNR'] > 0]
	table.write('snr.csv', format='ascii.csv')

def make_cube_catalog():
	"""A catalog of point sources distributed in a cube.
	"""
	table = population.make_cat_cube()
	table.write('cube.csv', format='ascii.csv')

if __name__ == '__main__':
	make_snr_catalog()
	make_cube_catalog()
