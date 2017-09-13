"""
Plot example Lomb-Scargle figures for the Gammapy docs at
http://docs.gammapy.org/en/latest/time/period.html
"""
import numpy as np
from astropy.table import Table
import sys

from gammapy.time.lomb_scargle import lomb_scargle
from gammapy.time.plot_periodogram import plot_periodogram

table = Table.read('https://github.com/gammapy/gamma-cat/raw/master/input/data/2006/2006A%2526A...460..743A/tev-000119-lc.ecsv', format='ascii.ecsv')
time = (table['time_max'].data + table['time_min'].data) / 2
flux = table['flux'].data
flux_err = table['flux_err'].data

result = lomb_scargle(time, flux, flux_err, 0.001, 10, 'boot')
fig = plot_periodogram(time, flux, flux_err, result['pgrid'],
                       result['psd'], result['swf'], result['period'],
                       result['significance']
                       )
fig.savefig('example_lomb_scargle', bbox_inches='tight')
