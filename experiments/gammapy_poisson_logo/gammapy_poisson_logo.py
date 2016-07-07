"""
Script to simulate a gammapy logo shaped source on the sky.
"""

import os

import logging
log = logging.getLogger(__name__)

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

from scipy.ndimage import imread
from scipy.ndimage.filters import gaussian_filter
from scipy.stats import rv_discrete

from gammapy.image import SkyMap, SkyMapCollection


EVENTS_PER_TIME_INTERVAL = 100

def create_gammapy_skymap(smooth=3):
	"""
	Parameters
	----------
	smooth : 3
		 Gaussian smoothing width in pixel.
	"""
	# create logo cutout
	filename = os.environ.get('GAMMAPY_EXTRA') + '/logo/gammapy_logo.png'
	gammapy_logo = (imread(filename, flatten=True) > 1).astype('float')

	shape = gammapy_logo.shape
	gammapy_cutout = SkyMap.empty(nxpix=shape[1], nypix=shape[0], binsz=0.02)
	
	# flip upside down
	gammapy_cutout.data = np.flipud(gammapy_logo)

	# reproject to larger sky map
	gammapy_skymap = SkyMap.empty(nxpix=320, nypix=180, binsz=0.08)
	gammapy_skymap = gammapy_cutout.reproject(gammapy_skymap)
	gammapy_skymap.name = 'gp_logo'

	gammapy_skymap.data = np.nan_to_num(gammapy_skymap.data)
	gammapy_skymap.data = gaussian_filter(gammapy_skymap.data, smooth)
	
	# normalize
	gammapy_skymap.data /= gammapy_skymap.data.sum()
	return gammapy_skymap


def animate(n, image, counts, bins, counts_generator):
	idx = counts_generator.rvs(size=EVENTS_PER_TIME_INTERVAL)
	sample, _ = np.histogram(idx, bins)
	counts += sample.reshape(counts.shape)
	image.set_data(counts)
	return image

def main():
	fig = plt.figure(figsize=(3.2, 1.8))
	ax = fig.add_axes([0, 0, 1, 1])

	signal = create_gammapy_skymap().data
	background = np.ones(signal.shape)
	background /= background.sum()

	data = (1 * signal + background) / 2.

	# setup counts generator
	pdf = data.copy().flatten()
	x = np.arange(pdf.size)
	counts_generator = rv_discrete(name='counts', values=(x, pdf))

	counts = np.zeros_like(data)

	image = ax.imshow(counts, cmap='afmhot', origin='lower', vmin=0, vmax=9,
					  interpolation='None')
	bins = np.arange(counts.size + 1) - 0.5

	anim = FuncAnimation(fig, animate, fargs=[image, counts, bins, counts_generator],
                         frames=200, interval=50)
	
	filename = 'gammapy_logo.gif'
	anim.save(filename, writer='imagemagick')
		
	

if __name__ == '__main__':
	main()