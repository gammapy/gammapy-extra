from collections import OrderedDict

import numpy as np

from astropy import units as u
from astropy.coordinates import Angle

from gammapy.image import SkyImage, SkyImageList
from gammapy.cube import exposure_cube as compute_exposure_cube
from gammapy.cube import SkyCube
from gammapy.spectrum.models import PowerLaw2
from gammapy.utils.energy import EnergyBounds, Energy
from gammapy.spectrum import LogEnergyAxis

SPECTRAL_INDEX = 2.3

class IACTSkyImageEstimator(object):
    """
    Estimate the basic sky images for a set of IACT observations.
    
    The following images will be computed:
    
        * counts
        * exposure
        * background
    
    Parameters
    ----------
    reference : `~gammapy.image.SkyImage`
        Reference sky image.
    emin : `~astropy.units.Quantity`
        Lower bound of energy range.
    emax : `~astropy.units.Quantity`
        Upper bound of energy range.
    offset_max : `~astropy.coordinates.Angle`
        Upper bound of offset range.
    spectral_model : `~gammapy.spectrum.models.SpectralModel`
        Spectral model assumption to compute mean exposure and psf image.
    exclusion_mask : `~gammapy.image.SkyMask`
        Exclusion mask.
    background_estimator : 
        Background estimation method. 
    
    """
    def __init__(self, reference, emin, emax, offset_max=Angle(2.5, 'deg'), spectral_model=None,
                 background_estimator=None, exclusion_mask=None):
        self.reference = reference
        self.background_estimator = background_estimator
        self.exclusion_mask = exclusion_mask
        
        if spectral_model is None:
            index = SPECTRAL_INDEX
            amplitude = u.Quantity(1, '')
            spectral_model = PowerLaw2(index=index, amplitude=amplitude,
                                       emin=emin, emax=emax)

        self.spectral_model = spectral_model
        self.parameters = OrderedDict(emin=emin, emax=emax, offset_max=offset_max)
        
    def _get_empty_skyimage(self):
        """
        Get empty sky image like reference image.
        """
        p = self.parameters
        image = SkyImage.empty_like(self.reference)
        image.meta['emin'] = str(p['emin'])
        image.meta['emax'] = str(p['emax'])
        return image

    def _get_ref_cube(self, enumbins=11):
        p = self.parameters
        
        wcs = self.reference.wcs.deepcopy()
        shape = (enumbins,) + self.reference.data.shape
        data = np.zeros(shape)
        
        energy = Energy.equal_log_spacing(p['emin'], p['emax'], enumbins, 'TeV')
        energy_axis = LogEnergyAxis(energy, mode='center')
        return SkyCube(data=data, wcs=wcs, energy_axis=energy_axis)
    
    def _exposure_image(self, observation):
        p = self.parameters
        kwargs = {}
        kwargs['livetime'] = observation.observation_live_time_duration
        kwargs['pointing'] = observation.pointing_radec
        kwargs['aeff2d'] = observation.aeff
        kwargs['offset_max'] = p['offset_max']
        kwargs['ref_cube'] = self._get_ref_cube()
        exposure_cube = compute_exposure_cube(**kwargs)
        
        energies = exposure_cube.energies('center')
        weights = self.spectral_model(energies)
        
        exposure_cube.data = exposure_cube.data * weights.reshape(-1, 1, 1)
        exposure = exposure_cube.sky_image_integral(emin=p['emin'], emax=p['emax'])
        
        exposure.name = 'exposure'
        exposure.data = np.nan_to_num(exposure.data)
        return exposure
    
    def _psf_image(self, observation):
        raise NotImplementedError
    
    def _counts_image(self, observation):
        """
        Compute counts image in energy band
        """
        p = self.parameters
        events = observation.events.select_energy((p['emin'], p['emax']))
        
        #TODO: check if a lower offset bound different from zero is needed. 
        events = events.select_offset((Angle(0, 'deg'), p['offset_max']))

        counts = self._get_empty_skyimage()
        counts.fill_events(events)
        return counts
    
    def _background_image(self, counts, exposure):
        p = self.parameters
        input_images = SkyImageList()
        input_images['counts'] = counts
        exposure_on = exposure.copy()
        exposure_on.name = 'exposure_on'
        input_images['exposure_on'] = exposure_on
        input_images['exclusion'] = self.exclusion_mask
        
        return self.background_estimator.run(input_images)
    
    def run(self, observations):
        """
        Run sky image estimation.
        
        Parameters
        ----------
        observations : `gammapy.data.ObservationList`
            List of observations
        
        Returns
        -------
        sky_images : `gammapy.image.SkyImageList`
            List of sky images.
        """
        result = SkyImageList()
        result['counts'] = self._get_empty_skyimage()
        result['exposure'] = self._get_empty_skyimage()
        result['background'] = self._get_empty_skyimage()
        
        for observation in observations:
            counts = self._counts_image(observation)
            result['counts'].data += counts.data
            
            exposure = self._exposure_image(observation)
            result['exposure'].data += exposure.data
            
            background = self._background_image(counts, exposure)
            result['background'].data += np.nan_to_num(background['background'].data)
            
        return result
