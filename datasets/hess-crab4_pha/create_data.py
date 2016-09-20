from gammapy.spectrum.tests.test_extract import obs, target, bkg
from gammapy.datasets import gammapy_extra
from gammapy.spectrum import SpectrumExtraction

outdir = gammapy_extra.filename("datasets/hess-crab4_pha")

extraction = SpectrumExtraction(obs=obs(),
                                target=target(),
                                background=bkg(),
                               )
extraction.estimate_background(extraction.background)
extraction.extract_spectrum()
extraction.observations.write(outdir, use_sherpa=True)
