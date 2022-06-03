import numpy as np
import astropy.units as u
from regions import CircleSkyRegion
from astropy.coordinates import SkyCoord, Angle
from gammapy.data import DataStore
from gammapy.maps import MapAxis, RegionGeom
from gammapy.datasets import SpectrumDataset
from gammapy.makers import SpectrumDatasetMaker, ReflectedRegionsBackgroundMaker
from unbinned_datasets import (
    UnbinnedSpectrumDatasetOnOff,
    UnbinnedReflectedRegionsBackgroundMaker,
)
import matplotlib.pyplot as plt

#  load the datasets
datastore = DataStore.from_dir("../../datasets/hess-dl3-dr1/")
obs_ids = [23523, 23526, 23559, 23592]
observations = datastore.get_observations(obs_ids)

# define the on region
target_position = SkyCoord(ra=83.63, dec=22.01, unit="deg", frame="icrs")
on_region_radius = Angle("0.11 deg")
on_region = CircleSkyRegion(center=target_position, radius=on_region_radius)
# and the energy binning
energy_axis = MapAxis.from_energy_bounds(
    0.1, 50, nbin=200, per_decade=False, unit="TeV", name="energy"
)
energy_axis_true = MapAxis.from_energy_bounds(
    0.05, 100, nbin=200, per_decade=False, unit="TeV", name="energy_true"
)

# create the empty dataset
geom = RegionGeom.create(region=on_region, axes=[energy_axis])
dataset_empty = SpectrumDataset.create(geom=geom, energy_axis_true=energy_axis_true)
dataset_maker = SpectrumDatasetMaker(
    containment_correction=True, selection=["counts", "exposure", "edisp"]
)

# binned and unbinned background makers and list to host the SpectrumDatasets
bkg_maker = ReflectedRegionsBackgroundMaker()
unbinned_bkg_maker = UnbinnedReflectedRegionsBackgroundMaker()
datasets = []
unbinned_datasets = []

for observation in observations:
    # binned datasets
    dataset = dataset_maker.run(dataset_empty, observation)
    dataset_on_off = bkg_maker.run(dataset, observation)
    datasets.append(dataset_on_off)
    # unbinned datasets
    unbinned_dataset_on_off = unbinned_bkg_maker.run(dataset, observation)
    unbinned_datasets.append(unbinned_dataset_on_off)
    # write the unbinned to disk
    unbinned_dataset_on_off.write(
        f"data/obs_id_{observation.obs_id}_unbinned_spectrum.fits", overwrite=True
    )

# check that the same events have been stored by checking the histograms
# of the ON and OFF counts from the two datasets
for binned, unbinned in zip(datasets, unbinned_datasets):
    fig, ax = plt.subplots(1, 2)
    binned.counts.plot_hist(ax=ax[0], label="binned data")
    energy_edges_on = binned.counts.geom.axes["energy"].edges
    ax[0].hist(
        unbinned.events.energy.value,
        bins=list(energy_edges_on),
        histtype="step",
        ls="--",
        lw=2,
        label="unbinned",
    )
    ax[0].set_title("ON counts")
    ax[0].legend()
    binned.counts_off.plot_hist(ax=ax[1], label="binned data")
    energy_edges_off = binned.counts.geom.axes["energy"].edges
    ax[1].hist(
        unbinned.events_off.energy.value,
        bins=list(energy_edges_off),
        histtype="step",
        ls="--",
        lw=2,
        label="unbinned",
    )
    ax[1].set_title("OFF counts")
    ax[1].legend()
    plt.show()
