"""
Plot example Lomb-Scargle figures for the Gammapy docs at
http://docs.gammapy.org/en/latest/time/period.html
"""
import numpy as np
from astropy.table import Table
from astropy.stats import LombScargle
from astropy.stats.lombscargle import _statistics
from gammapy.time import robust_periodogram, plot_periodogram

# get data
url = 'https://github.com/gammapy/gamma-cat/raw/master/input/data/2006/2006A%2526A...460..743A/tev-000119-lc.ecsv'
table = Table.read(url, format='ascii.ecsv')
time = (table['time_max'].data + table['time_min'].data) / 2
flux = table['flux'].data
flux_err = table['flux_err'].data

# set up period grid for periodogram
dt = 0.001
max_period = 10
periods = np.linspace(dt, 10, max_period / dt)

# compute robust periodogram
periodogram = robust_periodogram(time, flux, flux_err,
                            periods=periods, loss='linear', scale=1
                            )

# compute false alarm probability
fap = _statistics.false_alarm_probability(periodogram['power'].max(), 1. / periodogram['periods'].max(),
                                          time, flux, flux_err, 'standard', 'baluev')

# plot periodogram and save figure
fig = plot_periodogram(
    time, flux, periods=periodogram['periods'], power=periodogram['power'],
    flux_err = flux_err, best_period=periodogram['best_period'], fap=fap,
)
fig.savefig('example_robust_periodogram.png', bbox_inches='tight')

# print period of the highest periodogram peak and its false alarm probability
print('Detected period: {} +/- {}'.format(periodogram['best_period'], dt))
print('False alarm probability of period:')
print(fap)

# set up window function
dt = 0.1
time_win = np.rint(time / dt) * dt
t_max = np.max(time_win)
t_min = np.min(time_win)
window_grid = np.arange(t_min, t_max + dt, dt)
window_grid = np.rint(window_grid / dt) * dt  # round again since np.arange is not robust
window = np.zeros(len(window_grid))
window[np.searchsorted(window_grid, time_win, side='right') - 1] = 1

# compute spectral window function
# spectral_window_function = LombScargle(window_grid, window, 1).power(1. / periods)
spectral_window_function = robust_periodogram(window_grid, window, np.ones_like(window),
                                              periods=periods, loss='linear', scale=1
                                              )

# plot spectral window function and save figure
fig = plot_periodogram(
    window_grid, window, periods=spectral_window_function['periods'], power=spectral_window_function['power']
)
fig.savefig('example_spectral_window_function', bbox_inches='tight')
