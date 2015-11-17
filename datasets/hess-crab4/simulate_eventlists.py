#!/usr/bin/env python

# Simulate event list using gammalib ctobssim
import gammalib
import ctools
from astropy.io import fits

def createobs(ra=86.171648, dec=-1.4774586, rad=5.0,
              emin=0.1, emax=100.0, duration=360000.0, deadc=0.95,
              ):
    obs = gammalib.GCTAObservation()

    # Set pointing direction
    pntdir = gammalib.GSkyDir()
    pntdir.radec_deg(ra, dec)
    pnt = gammalib.GCTAPointing()
    pnt.dir(pntdir)
    obs.pointing(pnt)

    # Set ROI
    roi = gammalib.GCTARoi()
    instdir = gammalib.GCTAInstDir()
    instdir.dir(pntdir)
    roi.centre(instdir)
    roi.radius(rad)

    # Set GTI
    gti = gammalib.GGti()
    start = gammalib.GTime(0.0)
    stop = gammalib.GTime(duration)
    gti.append(start, stop)

    # Set energy boundaries
    ebounds = gammalib.GEbounds()
    e_min = gammalib.GEnergy()
    e_max = gammalib.GEnergy()
    e_min.TeV(emin)
    e_max.TeV(emax)
    ebounds.append(e_min, e_max)

    # Allocate event list
    events = gammalib.GCTAEventList()
    events.roi(roi)
    events.gti(gti)
    events.ebounds(ebounds)
    obs.events(events)

    # Set ontime, livetime, and deadtime correction factor
    obs.ontime(duration)
    obs.livetime(duration * deadc)
    obs.deadc(deadc)

    # Return observation
    return obs


def make_dummy_eventlist():

    filenames = [
        'hess_events_023523_empty.fits',
        'hess_events_023526_empty.fits',
        'hess_events_023559_empty.fits',
        'hess_events_023592_empty.fits',
    ]

    for f in filenames:
        obs = createobs()
        print('Writing {}'.format(f))
        obs.save(f, True)


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
