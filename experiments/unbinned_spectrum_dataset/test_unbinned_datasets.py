import numpy as np
import astropy.units as u
from regions import CircleSkyRegion
from astropy.coordinates import SkyCoord, Angle
from gammapy.data import DataStore
from unbinned_datasets import (
    UnbinnedSpectrumDatasetMaker,
    UnbinnedSpectrumDataset,
    UnbinnedSpectrumDatasetOnOff,
    UnbinnedReflectedRegionsBackgroundMaker,
)

datastore = DataStore.from_dir("../../datasets/hess-dl3-dr1/")
obs_ids = [23523, 23526, 23559, 23592]
observations = datastore.get_observations(obs_ids)

# define the on region
target_position = SkyCoord(ra=83.63, dec=22.01, unit="deg", frame="icrs")
on_region_radius = Angle("0.11 deg")
on_region = CircleSkyRegion(center=target_position, radius=on_region_radius)
# and the energy binning
e_reco = np.logspace(-1, np.log10(50), 200) * u.TeV
e_true = np.logspace(np.log10(0.05), 2, 200) * u.TeV

# empty dataset, the create method is inherited from SpectrumDataset
unbinned_dataset_empty = UnbinnedSpectrumDataset.create(
    e_reco=e_reco, e_true=e_true, region=on_region
)
# dataset and background makers
unbinned_dataset_maker = UnbinnedSpectrumDatasetMaker(
    containment_correction=True, selection=["events", "aeff", "edisp"]
)
bkg_maker = UnbinnedReflectedRegionsBackgroundMaker()

datasets = []
for observation in observations:
    dataset = unbinned_dataset_maker.run(unbinned_dataset_empty, observation)
    dataset_on_off = bkg_maker.run(dataset, observation)
    dataset_on_off.write(
        f"data/obs_id_{observation.obs_id}_unbinned_spectrum.fits", overwrite=True
    )
    datasets.append(dataset_on_off)
