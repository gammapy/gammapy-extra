"""Make a Fermi-LAT counts image in Healpix format.


TODO:
- add option to select the energy band

- let user enter angular resolution in deg
- what is a good nside choice given the Fermi PSF

- Find out command to convert HPX file to HIPS
  http://aladin.u-strasbg.fr/hips/HipsIn10Steps.gml

- Apply this to other Fermi or HESS data
- Generate reference test healpix dataset
"""
import numpy as np
import healpy as hp
from gammapy.data import EventList


def make_healpix_image(events, nside, sigma):
    theta = np.deg2rad(90 - events['B'])
    phi = np.deg2rad(events['L'])
    bins = np.arange(hp.nside2npix(nside) + 1) - 0.5
    data = hp.ang2pix(nside, theta, phi)
    counts, _ = np.histogram(data, bins)
    counts = hp.smoothing(counts, sigma=sigma)

    return counts


if __name__ == '__main__':
    filename = '/Users/deil/code/fhee/data/2fhl_events.fits.gz'
    events = EventList.read(filename)
    events.meta['EUNIT'] = 'GeV'

    counts = make_healpix_image(events, nside=256, sigma=0.001)

    filename = '2fhl_counts_healpix.fits.gz'
    print('Writing {}'.format(filename))
    hp.write_map(filename, m=counts)
    # import matplotlib.pyplot as plt
    # hp.mollview(counts, title="Mollview image RING")
    # plt.show()

    # m = np.arange(hp.nside2npix(NSIDE))
    # zeros = np.zeros(hp.nside2npix(NSIDE))
    # hp.mollview(m, title="Mollview image RING")
    # print (len(counts) == hp.nside2npix(NSIDE))
