from gammapy.spectrum import SpectrumFit, SpectrumObservation, SpectrumFitResult
import matplotlib.pyplot as plt
import astropy.units as u

obs = SpectrumObservation.read('pha_obs31415.fits')
fit = SpectrumFit(obs)

obs.peek()
plt.savefig('observation.png')
plt.cla()

fit.run()
fit.result[0].plot_fit()
plt.savefig('debug_fit.png')

# TODO: implement properly
plt.cla()

fig = plt.figure()
ax = fig.add_subplot(111)
fit.result[0].fit.plot_butterfly(ax=ax, label='Fit result')
input_parameters = dict(index = 2.3 * u.Unit(''),
                        norm = 2.5 * 1e-12 * u.Unit('cm-2 s-1 TeV-1'),
                        reference = 1 * u.TeV)
input_parameter_errors = dict(index = 0 * u.TeV,
                              norm = 0 * u.Unit('cm-2 s-1 TeV-1'),
                              reference = 0 * u.TeV)

input_model = SpectrumFitResult(spectral_model = 'PowerLaw',
                                parameters = input_parameters,
                                parameter_errors = input_parameter_errors)


input_model.plot(ax=ax, label='Input model', energy_range = [0.1, 80] * u.TeV)
ax.legend(numpoints=1)
plt.savefig('model_fit.png')



