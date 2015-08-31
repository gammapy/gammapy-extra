#!/usr/bin/env python
"""Simulate using ``hess_events_023523.fits.gz`` as **input**.

This is "Method 1" described in ``README.rst``.
"""

import ctools


def run_obssim():
    sim = ctools.ctobssim()
    sim['inmodel'] = 'model.xml'
    sim['inobs'] = 'inobs1.xml'
    sim['outevents'] = 'outevents1.xml'
    sim['prefix'] = 'events1_'
    sim['emin'] = 0.5
    sim['emax'] = 70
    sim['rad'] = 3
    sim['logfile'] = 'make1.log'
    sim.execute()

if __name__ == '__main__':
    run_obssim()
