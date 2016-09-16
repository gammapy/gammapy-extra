"""
Generate the ``expected_ts_*`` files in this directory
that are used for `gammapy/scripts/tests/test_image_ts.py`

The code here has been copy & pasted & adapted from that test.
"""
from astropy.io import fits
from gammapy.datasets import load_poisson_stats_image
from gammapy.scripts.image_ts import image_ts_main


def make_input_all():
    data = load_poisson_stats_image(extra_info=True)
    header = data['header']
    images = [data['counts'], data['background'], data['exposure']]
    image_names = ['Counts', 'Background', 'Exposure']

    hdu_list = fits.HDUList()
    for image, name in zip(images, image_names):
        hdu = fits.ImageHDU(data=image, header=header, name=name)
        hdu_list.append(hdu)

    filename = 'input_all.fits.gz'
    print('Writing {}'.format(filename))
    hdu_list.writeto(filename, clobber=True)


def make_ts_image(scale):
    filename = 'expected_ts_{}.fits.gz'.format(scale)
    args = ['input_all.fits.gz', filename, "--psf", 'psf.json', "--scales", scale, '--overwrite']
    print('Executing command: gammapy-image-ts {}'.format(' '.join(args)))
    print('Writing {}'.format(filename))
    image_ts_main(args)


if __name__ == '__main__':
    make_input_all()

    scales = ['0.000', '0.050', '0.100', '0.200']
    for scale in scales:
        make_ts_image(scale)
