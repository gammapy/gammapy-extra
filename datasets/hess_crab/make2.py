#!/usr/bin/env python
"""Simulate using dummy generated ``dummy_events_023523.fits`` as **input**.

This is "Method 2" described in ``README.rst``.
"""
import shutil

def remove_events(infile, outfile):
    from astropy.io import fits

    print('Reading {}'.format(infile))
    hdu_list = fits.open(infile)
    hdu_list['EVENTS'].data = None


    print('Writing {}'.format(outfile))
    hdu_list.writeto(outfile, clobber=True)


def run_obssim():
    import ctools
    sim = ctools.ctobssim()
    sim['inmodel'] = 'model.xml'
    sim['inobs'] = 'inobs2.xml'
    sim['outevents'] = 'outevents2.xml'
    sim['prefix'] = 'events2_'
    sim['emin'] = 0.463794
    sim['emax'] = 80
    sim['rad'] = 5
    sim['logfile'] = 'make2.log'
    sim.execute()


if __name__ == '__main__':
    remove_events(infile='hess_events_023523.fits.gz',
                  outfile='hess_events_023523_empty.fits')
    run_obssim()
    filename = '../../test_datasets/irf/hess/pa/hess_events_023523.fits'
    print('Moving events2_0.fits to {}'.format(filename))
    shutil.move('events2_0.fits', filename)
