"""
Plot example Lomb-Scargle figures for the Gammapy docs at
http://docs.gammapy.org/en/latest/time/period.html
"""
from astropy.table import Table
from gammapy.time import lomb_scargle, plot_periodogram

# get data
url = 'https://github.com/gammapy/gamma-cat/raw/master/input/data/2006/2006A%2526A...460..743A/tev-000119-lc.ecsv'
table = Table.read(url, format='ascii.ecsv')
time = (table['time_max'].data + table['time_min'].data) / 2
flux = table['flux'].data
flux_err = table['flux_err'].data

# set up parameters for Lomb-Scargle periodogram
dt = 0.001
max_period = 10

# compute Lomb-Scargle periodogram
result = lomb_scargle(time, flux, flux_err, dt=dt, max_period=max_period)

# plot periodogram and save figure
fig = plot_periodogram(
    time, flux, flux_err,
    periods=result['pgrid'],
    psd_data=result['psd'],
    psd_win=result['swf'],
    best_period=result['period'],
    fap=result['fap'],
)
fig.savefig('example_lomb_scargle.png', bbox_inches='tight')

# print period of the highest periodogram peak and its false alarm probability
print('Detected period: {} +/- {}'.format(result['period'], dt))
print('False alarm probability of period:')
print(result['fap'])
