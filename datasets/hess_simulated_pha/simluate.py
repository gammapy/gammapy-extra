"""Simulate one H.E.S.S. SpectrumObservation

This script creates on SpecturmObservation of the crab nebula to be used for
the Gammapy docs or presentations. It uses the Abramowski parametrization for
the effective area and a gaussian energy dispersion with 20% resolution

"""

from gammapy.irf import (
    EnergyDispersion,
    EffectiveAreaTable,
    abramowski_effective_area,
)
from gammapy.spectrum.models import PowerLaw
from gammapy.spectrum import (
    calculate_predicted_counts,
    SpectrumExtraction,
    PHACountsSpectrum,
    SpectrumObservation
)
from gammapy.utils.random import get_random_state
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt

e_true = SpectrumExtraction.DEFAULT_TRUE_ENERGY
e_reco = SpectrumExtraction.DEFAULT_RECO_ENERGY

# EDISP
edisp = EnergyDispersion.from_gauss(e_true=e_true,
                                    e_reco=e_true,
                                    sigma=0.2
                                   )

# AEFF
nodes = np.sqrt(e_true[:-1] * e_true[1:])
data = abramowski_effective_area(energy=nodes)
aeff = EffectiveAreaTable(data=data, energy=e_true)
lo_threshold = aeff.find_energy(0.1 * aeff.max_area)


# MODEL
model = PowerLaw(
    index = 2.3 * u.Unit(''),
    amplitude = 2.5 * 1e-12 * u.Unit('cm-2 s-1 TeV-1'),
    reference = 1 * u.TeV
)

# COUNTS
livetime = 2 * u.h
npred = calculate_predicted_counts(model=model,
                                   aeff=aeff,
                                   edisp=edisp,
                                   livetime=livetime)

bkg = 0.2 * npred.data
alpha = 0.1
counts_kwargs = dict(energy=npred.energy,
                     exposure=livetime,
                     obs_id = 31415,
                     creator = 'Simulation',
                     hi_threshold = 50 * u.TeV,
                     lo_threshold = lo_threshold)

rand = get_random_state(42)

on_counts = rand.poisson(npred.data) + rand.poisson(bkg)
on_vector = PHACountsSpectrum(data=on_counts,
                              backscal = 1,
                              **counts_kwargs 
                             )

off_counts = rand.poisson(1. / alpha * bkg)
off_vector = PHACountsSpectrum(data=off_counts,
                               backscal = 1. / alpha,
                               is_bkg=True,
                               **counts_kwargs)


obs = SpectrumObservation(on_vector = on_vector,
                          off_vector = off_vector,
                          aeff = aeff,
                          edisp = edisp
                         )

obs.write()
