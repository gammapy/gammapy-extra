#!/usr/bin/env python
"""Generate reference files with ctools.
"""
import ctools

def set_spatial_pars(tool):
    tool['nxpix'] = 200
    tool['nypix'] = 200
    tool['binsz'] = 0.01
    tool['coordsys'] = 'CEL'
    tool['xref'] = 83.5
    tool['yref'] = 22
    tool['proj'] = 'CAR'

def run_ctskymap(outfile='ctskymap.fits.gz'):
    tool = ctools.ctskymap()
    tool['inobs'] = 'hess_events_023523.fits.gz'
    tool['outmap'] = outfile
    tool['emin'] = 0.1
    tool['emax'] = 100
    set_spatial_pars(tool)
    print('Writing {}'.format(outfile))
    tool.execute()


if __name__ == '__main__':
    run_ctskymap()
