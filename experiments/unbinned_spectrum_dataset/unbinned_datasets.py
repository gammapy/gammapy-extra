import numpy as np
from astropy.io import fits
from gammapy.spectrum import (
    SpectrumDatasetMaker,
    SpectrumDatasetOnOff,
    ReflectedRegionsBackgroundMaker,
)
from gammapy.utils.regions import list_to_compound_region


class UnbinnedSpectrumDatasetOnOff(SpectrumDatasetOnOff):
    """The UnbinnedSpectrumDatasetOnOff has the events and events_off 
    attritubutes compared to the SpectrumDatasetOnOff from which it inherits."""

    def __init__(
        self,
        models=None,
        events=None,
        events_off=None,
        livetime=None,
        aeff=None,
        edisp=None,
        mask_safe=None,
        mask_fit=None,
        acceptance=None,
        acceptance_off=None,
        name="",
        gti=None,
    ):
        SpectrumDatasetOnOff.__init__(
            self,
            models=models,
            counts=None,
            counts_off=None,
            livetime=livetime,
            aeff=aeff,
            edisp=edisp,
            mask_safe=mask_safe,
            mask_fit=mask_fit,
            acceptance=acceptance,
            acceptance_off=acceptance_off,
            name=name,
            gti=gti,
        )
        # events in the ON and OFF regions
        self.events = events
        self.events_off = events_off

    def write(self, datapath, overwrite):
        """write the ON / OFF event lists and the IRFs in a single HDUList"""
        hdr = fits.Header()
        hdr["TEFF"] = self.livetime.to("s").value
        hdr["TEFF_U"] = "s"
        # acceptance and acceptance_off are arrays in SpectrumDatasetOnOff
        hdr["ACC"] = self.acceptance[0]
        hdr["ACC_OFF"] = self.acceptance_off[0]
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
    """Inheriting from ReflectedRegionsBackgroundMaker and 
    adding functions to generate list of events in the ON and OFF region"""

    def make_events(self, dataset, observation):
        """Make list of ON events.

        Parameters
        ----------
        dataset : `UnbinnedSpectrumDataset`
            Spectrum dataset.
        observation : `DatastoreObservation`
            Data store observation.


        Returns
        -------
        events : `EventList`
            list of events in the ON region.
        """
        # the on region is stored in the Counts of the SpectrumDatasetOnOff
        region = dataset.counts.region
        wcs = SpectrumDatasetMaker.geom_ref(region).wcs
        events = observation.events.select_region(region, wcs)
        return events

    def make_events_off(self, dataset, observation):
        """Make list of OFF events.

        Parameters
        ----------
        dataset : `UnbinnedSpectrumDataset`
            Spectrum dataset.
        observation : `DatastoreObservation`
            Data store observation.


        Returns
        -------
        events_off : `EventList`
            list of events in the OFF region
        acceptance_off : int
            number of OFF regions used
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
        dataset_on_off : `UnbinnedSpectrumDatasetOnOff`
            unbinned ON OFF dataset
        """
        events = self.make_events(dataset, observation)
        events_off, acceptance_off = self.make_events_off(dataset, observation)

        return UnbinnedSpectrumDatasetOnOff(
            events=events,
            events_off=events_off,
            livetime=dataset.livetime,
            aeff=dataset.aeff,
            edisp=dataset.edisp,
            mask_safe=dataset.mask_safe,
            mask_fit=dataset.mask_fit,
            acceptance=1,
            acceptance_off=acceptance_off,
            name="",
            gti=dataset.gti,
        )
