#!/usr/bin/env python
"""
Simulate event list using gammalib ctobssim
"""
import ctools


def make_obsdef(obs_ids)

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


def cleanup():
    import os
    os.system("rm *temp*")
    os.system("mv hess_events_0.fits hess_events_simulated_023523.fits")
    os.system("mv hess_events_1.fits hess_events_simulated_023559.fits")
    os.system("mv hess_events_2.fits hess_events_simulated_023526.fits")
    os.system("mv hess_events_3.fits hess_events_simulated_023592.fits")
        

if __name__ == '__main__':
    obs_ids = [23523]
    make_obsdef(obs_ids)
    run_obssim()
    # cleanup()
