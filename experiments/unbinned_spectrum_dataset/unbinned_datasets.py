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

    def __init__(self, events, events_off, **kwargs):
        self.events = events
        self.events_off = events_off
        super().__init__(**kwargs)

    def write(self, datapath, overwrite):
        """write the ON / OFF event lists and the IRFs in a single HDUList"""
        hdu = fits.BinTableHDU(self.events.table)
        hdu_off = fits.BinTableHDU(self.events_off.table)
        # add the ON and OFF acceptances on the respective header of the events
        # acceptance and acceptance_off are arrays in SpectrumDatasetOnOff
        hdu.header["ACC"] = self.acceptance[0]
        hdu_off.header["ACC"] = self.acceptance_off[0]
        # the effective area can be dumped directly in a HDU table
        hdu_aeff = self.aeff.to_hdulist()[1]
        # we'll use the primary of the edisp hdulist for the final hdu_list
        hdu_edisp = self.edisp.to_hdulist()
        hdu_list = fits.HDUList(
            [hdu_edisp[0], hdu, hdu_off, hdu_aeff, hdu_edisp[1], hdu_edisp[2]]
        )
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
