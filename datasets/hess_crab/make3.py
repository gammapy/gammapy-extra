#!/usr/bin/env python
"""Simulate using dummy generated ``dummy_events_023523.fits`` as **input**.

This is "Method 2" described in ``README.rst``.
"""
import gammalib
import ctools


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
    obs = createobs()

    filename = 'dummy_events_023523.fits'
    print('Writing {}'.format(filename))
    obs.save(filename, clobber=True)


def run_obssim():
    sim = ctools.ctobssim()
    sim['inmodel'] = 'model.xml'
    sim['inobs'] = 'inobs2.xml'
    sim['outevents'] = 'outevents2.xml'
    sim['prefix'] = 'events2_'
    sim['emin'] = 0.5
    sim['emax'] = 70
    sim['rad'] = 3
    sim['logfile'] = 'make2.log'
    sim.execute()


if __name__ == '__main__':
    make_dummy_eventlist()
    # run_obssim()
