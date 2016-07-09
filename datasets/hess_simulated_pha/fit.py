from gammapy.spectrum import SpectrumFit, SpectrumObservation
import matplotlib.pyplot as plt

obs = SpectrumObservation.read('pha_obs31415.fits')
fit = SpectrumFit(obs)

obs.peek()
plt.savefig('observation.png')
plt.cla()

fit.run()
fit.result[0].plot_fit()
plt.savefig('fit.png')

