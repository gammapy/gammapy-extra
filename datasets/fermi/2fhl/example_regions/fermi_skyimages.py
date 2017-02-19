"""
Generate sky images for the Fermi 2FHL dataset.
"""
import logging
from scipy.ndimage import convolve
from astropy.convolution import Tophat2DKernel, Ring2DKernel, Gaussian2DKernel
from gammapy.data import EventList
from gammapy.image import SkyMap, SkyMapCollection
from gammapy.background import IterativeKernelBackgroundEstimator as IKBE
from gammapy.background import GammaImages
from gammapy.detect import compute_lima_map

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def gaussian_smooth(skyimage, width):
    kernel = Gaussian2DKernel(width, mode='oversample').array
    skyimage.data = convolve(skyimage.data, kernel)
    return skyimage


def counts_skyimage_2fhl(**kwargs):
    log.info('Computing counts map.')
    events = EventList.read('2fhl_events.fits.gz')
    counts = SkyMap.empty('Counts', **kwargs)
    counts.fill(events)
    return counts


def background_skyimage_2fhl(counts):
    log.info('Computing background map.')
    images = GammaImages(counts.data, header=counts.wcs.to_header())

    source_kernel = Tophat2DKernel(5)
    source_kernel.normalize('peak')

    background_kernel = Ring2DKernel(20, 20)
    background_kernel.normalize('peak')

    ikbe = IKBE(
        images=images,
        source_kernel=source_kernel.array,
        background_kernel=background_kernel.array,
        significance_threshold=5,
        mask_dilation_radius=3,
    )

    mask_data, background_data = ikbe.run()

    mask = SkyMap.empty_like(counts)
    mask.data = mask_data

    background = SkyMap.empty_like(counts)
    background.data = background_data
    return mask, background


def skyimages_2fhl(**kwargs):
    # Counts
    skyimages = SkyMapCollection()
    skyimages.counts = counts_skyimage_2fhl(**kwargs)
    skyimages['counts_smoothed_0.25'] = gaussian_smooth(skyimages.counts.copy(), 2.5)

    # Background & Exclusion
    exclusion, background = background_skyimage_2fhl(skyimages.counts)
    skyimages.exclusion = exclusion
    skyimages.background = background

    # Significance
    log.info('Computing counts map.')
    tophat = Tophat2DKernel(5)
    tophat.normalize('peak')
    result = compute_lima_map(skyimages.counts, skyimages.background, tophat)
    skyimages['significance_0.5'] = result['significance']
    return skyimages


if __name__ == '__main__':
    # Galactic center
    filename = 'fermi_2fhl_gc.fits.gz'
    kwargs = dict(nxpix=320, nypix=180, binsz=0.1)
    gc_skyimages = skyimages_2fhl(**kwargs)
    log.info('Writing {}'.format(filename))
    gc_skyimages.write(filename, clobber=True)

    # Vela region
    filename = 'fermi_2fhl_vela.fits.gz'
    kwargs = dict(nxpix=320, nypix=180, binsz=0.1, xref=266, yref=-1.2)
    vela_skyimages = skyimages_2fhl(**kwargs)
    log.info('Writing {}'.format(filename))
    vela_skyimages.write(filename, clobber=True)
