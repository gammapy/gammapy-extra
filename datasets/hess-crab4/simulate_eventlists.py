#!/usr/bin/env python

# Simulate event list using gammalib ctobssim
import gammalib
import ctools
from astropy.io import fits


def run_obssim():
    sim = ctools.ctobssim()
    sim['inmodel'] = 'model.xml'
    sim['inobs'] = 'observation_definition.xml'
    sim['outevents'] = 'outevents.xml'
    sim['prefix'] = 'hess_events_'
    sim['emin'] = 0.5
    sim['emax'] = 70
    sim['rad'] = 3
    sim['logfile'] = 'simulation_output.log'
    sim.execute()


def write_file(f, hdu_name):
    hdu = fits.open(f)[1]
    hdu.name = hdu_name
    temp_name = f.split('.')[0] + '_temp.fits'
    print('Writing {}'.format(temp_name))
    hdu.writeto(temp_name, clobber=True)


def make_temp_irfs():

    #PSF
    filenames = [
        'hess_psf_023523.fits.gz',
        'hess_psf_023526.fits.gz',
        'hess_psf_023559.fits.gz',
        'hess_psf_023592.fits.gz',
    ]
    for f in filenames:
        write_file(f, 'POINT SPREAD FUNCTION')
        
    #AEFF2D
    filenames = [
        'hess_aeff_023523.fits.gz',
        'hess_aeff_023526.fits.gz',
        'hess_aeff_023559.fits.gz',
        'hess_aeff_023592.fits.gz',
    ]
    for f in filenames:
        write_file(f, 'EFFECTIVE AREA')

    #EDISP2D
    filenames = [
        'hess_edisp_023523.fits.gz',
        'hess_edisp_023526.fits.gz',
        'hess_edisp_023559.fits.gz',
        'hess_edisp_023592.fits.gz',
    ]
    for f in filenames:
        write_file(f, 'ENERGY DISPERSION')


if __name__ == '__main__':
    make_dummy_eventlist()
    make_temp_irfs()
    run_obssim()
