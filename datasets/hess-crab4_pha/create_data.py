from gammapy.spectrum.tests.test_extract import obs, target, bkg
from gammapy.datasets import gammapy_extra
from gammapy.spectrum import SpectrumExtraction
import numpy as np 
import astropy.units as u

outdir = gammapy_extra.filename("datasets/hess-crab4_pha")

# Restrict energy range to what is covered by HAP exporters
e_true = np.logspace(-1, 1.9, 70) * u.TeV

extraction = SpectrumExtraction(obs=obs(),
                                target=target(),
                                background=bkg(),
                                e_true=e_true,
                               )
extraction.estimate_background(extraction.background)
extraction.extract_spectrum()
extraction.observations.write(outdir, use_sherpa=True)
