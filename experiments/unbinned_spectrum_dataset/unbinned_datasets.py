import numpy as np
from astropy.io import fits
from gammapy.spectrum import (
    CountsSpectrum,
    ReflectedRegionsBackgroundMaker,
    SpectrumDatasetMaker,
    SpectrumDataset,
    SpectrumDatasetOnOff,
)
from gammapy.utils.regions import list_to_compound_region


class UnbinnedSpectrumDatasetMaker(SpectrumDatasetMaker):
    """Inheriting SpectrumDatasetMaker but replacing "counts" with "events".

    The irfs and background are computed at a single fixed offset,
    which is recommend only for point-sources.

    Parameters
    ----------
    containment_correction : bool
        Apply containment correction for point sources and circular on regions.
    selection : list
        List of str, selecting which maps to make.
        Available: 'events', 'aeff', 'background', 'edisp'
        By default, all spectra are made.
    """

    available_selection = ["events", "background", "aeff", "edisp"]

    def __init__(self, containment_correction=False, selection=None):
        SpectrumDatasetMaker.__init__(
            self, containment_correction=containment_correction, selection=selection
        )

        if selection is None:
            selection = self.available_selection

        self.selection = selection

    def make_events(self, region, observation):
        """Make list of events in the ON  region.

        Parameters
        ----------
        region : `~regions.SkyRegion`
            Region to compute counts spectrum for.
        observation: `~gammapy.data.DataStoreObservation`
            Observation to compute effective area for.

        Returns
        -------
        events : `~gammapy.data.event_list.EventList`
            list of ON events
        """
        events = observation.events.select_region(region, wcs=self.geom_ref(region).wcs)
        return events

    def run(self, dataset, observation):
        """Make unbinned spectrum dataset.

        Parameters
        ----------
        dataset : `~gammapy.spectrum.SpectrumDataset`
            Spectrum dataset.
        observation: `~gammapy.data.DataStoreObservation`
            Observation to reduce.

        Returns
        -------
        dataset : `~gammapy.spectrum.SpectrumDataset`
            Spectrum dataset.
        """
        kwargs = {
            "name": f"{observation.obs_id}",
            "gti": observation.gti,
            "livetime": observation.observation_live_time_duration,
        }
        energy_axis = dataset.counts.energy
        energy_axis_true = dataset.aeff.data.axis("energy")
        region = dataset.counts.region

        if "events" in self.selection:
            kwargs["events"] = self.make_events(region, observation)
            # array of dummy counts, not filled, the on region will be searched
            # in here by the ReflectedRegionsBackgroundMaker, so we keep it
            kwargs["counts"] = self.make_counts(region, energy_axis, observation)

        if "aeff" in self.selection:
            kwargs["aeff"] = self.make_aeff(region, energy_axis_true, observation)

        if "edisp" in self.selection:
            kwargs["edisp"] = self.make_edisp(
                region.center, energy_axis, energy_axis_true, observation
            )

        return UnbinnedSpectrumDataset(**kwargs)


class UnbinnedSpectrumDataset(SpectrumDataset):
    """Unbinned pectrum dataset for on-off likelihood fitting."""

    def __init__(
        self,
        models=None,
        events=None,
        counts=None,
        livetime=None,
        aeff=None,
        edisp=None,
        background=None,
        mask_safe=None,
        mask_fit=None,
        name="",
        gti=None,
    ):
        SpectrumDataset.__init__(
            self,
            models=models,
            counts=counts,
            livetime=livetime,
            aeff=aeff,
            edisp=edisp,
            background=background,
            mask_safe=mask_safe,
            mask_fit=mask_fit,
            name="",
            gti=gti,
        )
        # events in the signal region
        self.events = events


class UnbinnedSpectrumDatasetOnOff(UnbinnedSpectrumDataset):
    """The UnbinnedSpectrumDatasetOnOff has the events_off property
    compared to the UnbinnedSpectrumDataset, as the SpectrumDatasetOnOff has 
    the counts_off property compared to the SpectrumDataset
    """

    def __init__(
        self,
        models=None,
        events=None,
        events_off=None,
        livetime=None,
        aeff=None,
        edisp=None,
        acceptance=None,
        acceptance_off=None,
        mask_safe=None,
        mask_fit=None,
        name="",
        gti=None,
    ):
        UnbinnedSpectrumDataset.__init__(
            self,
            models=models,
            events=events,
            livetime=livetime,
            aeff=aeff,
            edisp=edisp,
            background=None,  # we have off events, so we do need the bkg
            mask_safe=mask_safe,
            mask_fit=mask_fit,
            name="",
            gti=gti,
        )
        # events in the background region
        self.events_off = events_off
        self.acceptance = acceptance
        self.acceptance_off = acceptance_off

    def write(self, datapath, overwrite):
        """write the ON / OFF event lists and the IRFs in a single HDUList"""
        hdr = fits.Header()
        hdr["TEFF"] = self.livetime.to("s").value
        hdr["TEFF_U"] = "s"
        hdr["ACC"] = self.acceptance
        hdr["ACC_OFF"] = self.acceptance_off
        primary_hdu = fits.PrimaryHDU(header=hdr)
        col_energy_on = fits.Column(
            name="ENERGY",
            format="D",
            array=np.asarray(self.events.energy.to("TeV").value),
            unit="TeV",
        )
        col_time_on = fits.Column(
            name="TIME",
            format="D",
            array=np.asarray(self.events.time.value),
            unit="MJD",
        )
        hdu_on = fits.BinTableHDU.from_columns([col_energy_on, col_time_on])
        col_energy_off = fits.Column(
            name="ENERGY",
            format="D",
            array=np.asarray(self.events_off.energy.to("TeV").value),
            unit="TeV",
        )
        col_time_off = fits.Column(
            name="TIME",
            format="D",
            array=np.asarray(self.events_off.time.value),
            unit="MJD",
        )
        hdu_off = fits.BinTableHDU.from_columns([col_energy_off, col_time_off])
        # the effective area can be dumped directly in a HDU table
        hdu_aeff = self.aeff.to_hdulist()[1]
        hdu_aeff.data.columns[2].name = "AEFF"
        # for the energy migration we store bias and resolution
        # such that we have simple 1d columns
        e_true = self.edisp.e_true.center
        bias = self.edisp.get_bias(e_true)
        resolution = self.edisp.get_resolution(e_true)
        col_energy_edisp = fits.Column(
            name="E_TRUE", format="D", array=e_true.value, unit="TeV"
        )
        col_bias_edisp = fits.Column(name="BIAS", format="D", array=bias, unit="")
        col_res_edisp = fits.Column(name="RES", format="D", array=resolution, unit="")
        hdu_edisp = fits.BinTableHDU.from_columns(
            [col_energy_edisp, col_bias_edisp, col_res_edisp]
        )
        hdu_list = fits.HDUList([primary_hdu, hdu_on, hdu_off, hdu_aeff, hdu_edisp])
        hdu_list.writeto(datapath, overwrite=overwrite)


class UnbinnedReflectedRegionsBackgroundMaker(ReflectedRegionsBackgroundMaker):
    """add functions to generate list of off_events"""

    def make_events_off(self, dataset, observation):
        """Make list of off events.

        Parameters
        ----------
        dataset : `UnbinnedSpectrumDataset`
            Spectrum dataset.
        observation : `DatastoreObservation`
            Data store observation.


        Returns
        -------
        events_off : `EventList`
            Off counts.
        """
        finder = self._get_finder(dataset, observation)
        finder.run()

        if len(finder.reflected_regions) > 0:
            region_union = list_to_compound_region(finder.reflected_regions)

            wcs = finder.reference_map.geom.wcs
            events_off = observation.events.select_region(region_union, wcs)
            acceptance_off = len(finder.reflected_regions)
        else:
            # if no OFF regions are found, off is set to None and acceptance_off to zero
            counts_off = None
            acceptance_off = 0

        return events_off, acceptance_off

    def run(self, dataset, observation):
        """Run reflected regions background maker

        Parameters
        ----------
        dataset : `SpectrumDataset`
            Spectrum dataset.
        observation : `DatastoreObservation`
            Data store observation.

        Returns
        -------
        dataset_on_off : `SpectrumDatasetOnOff`
            On off dataset.
        """
        events_off, acceptance_off = self.make_events_off(dataset, observation)

        return UnbinnedSpectrumDatasetOnOff(
            events=dataset.events,
            events_off=events_off,
            gti=dataset.gti,
            name=dataset.name,
            livetime=dataset.livetime,
            edisp=dataset.edisp,
            aeff=dataset.aeff,
            acceptance=1,
            acceptance_off=acceptance_off,
            mask_safe=dataset.mask_safe,
            mask_fit=dataset.mask_fit,
        )
