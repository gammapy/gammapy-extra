# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
from numpy.testing import assert_allclose
from astropy.table import Column
import numpy as np
from astropy.tests.helper import assert_quantity_allclose
from astropy.coordinates import SkyCoord, Angle
from gammapy.extern.pathlib import Path
from gammapy.data import DataStore
from gammapy.data import ObservationList, ObservationGroupAxis, ObservationGroups
from gammapy.utils.testing import requires_dependency, requires_data
from gammapy.image import SkyMask
from gammapy.cube import StackedObsCubeMaker
from gammapy.cube import SkyCube
from subprocess import call
from gammapy.background import OffDataBackgroundMaker
from gammapy.utils.energy import Energy, EnergyBounds
from gammapy.irf import TablePSF
from astropy.units import Quantity
from gammapy.background import fill_acceptance_image
from gammapy.catalog import load_catalog_tevcat
from regions import CircleSkyRegion
import astropy.units as u
import os
import shutil


def make_empty_cube(image_size, energy, center, data_unit=None):
    """
    Parameters
    ----------
    image_size:int, Total number of pixel of the 2D map
    energy: Tuple for the energy axis: (Emin,Emax,nbins)
    center: SkyCoord of the source
    unit : str, Data unit.
    """
    def_image = dict()
    def_image["nxpix"] = image_size
    def_image["nypix"] = image_size
    def_image["binsz"] = 0.02
    def_image["xref"] = center.galactic.l.deg
    def_image["yref"] = center.galactic.b.deg
    def_image["proj"] = 'TAN'
    def_image["coordsys"] = 'GAL'
    def_image["unit"] = data_unit
    e_min, e_max, nbins = energy
    empty_cube = SkyCube.empty(emin=e_min.value, emax=e_max.value, enumbins=nbins, eunit=e_min.unit, mode='edges',
                               **def_image)
    return empty_cube


def make_mean_psf_cube(image_size, energy_cube, center_maps, center, ObsList,
                       spectral_index=2.3):
    """
    Compute the mean psf for a set of observation for different energy bands
    Parameters
    ----------
    image_size:int, Total number of pixel of the 2D map
    energy: Tuple for the energy axis: (Emin,Emax,nbins)
    center_maps: SkyCoord
            center of the images
    center: SkyCoord 
            position where we want to compute the psf
    ObsList: ObservationList to use to compute the psf (could be different that the data_store for G0p9 for the GC for example)
    spectral_index: assumed spectral index to compute the psf

    Returns
    -------
    ref_cube : `~gammapy.cube.SkyCube`
             PSF mean cube

    """
    ref_cube = make_empty_cube(image_size, energy_cube, center_maps)
    header = ref_cube.sky_image_ref.to_image_hdu().header
    energy_bins = ref_cube.energies()
    for i_E, E in enumerate(energy_bins[0:-1]):
        energy_band = Energy([energy_bins[i_E].value, energy_bins[i_E + 1].value], energy_bins.unit)
        energy = EnergyBounds.equal_log_spacing(energy_band[0].value, energy_band[1].value, 100, energy_band.unit)
        psf_energydependent = ObsList.make_psf(center, energy, theta=None)
        try:
            psf_table = psf_energydependent.table_psf_in_energy_band(energy_band, spectral_index=spectral_index)
        except:
            psf_table = TablePSF(psf_energydependent.offset,
                                 Quantity(np.zeros(len(psf_energydependent.offset)), u.sr ** -1))
        ref_cube.data[i_E, :, :] = fill_acceptance_image(header, center_maps, psf_table._offset.to("deg"),
                                                         psf_table._dp_domega, psf_table._offset.to("deg")[-1]).data
    return ref_cube


def make_mean_rmf(energy_true, energy_reco, center, ObsList):
    """
    Compute the mean psf for a set of observation and a given energy band
    Parameters
    ----------
    energy_true: Tuple for the energy axis: (Emin,Emax,nbins)
         for the true energy array
    energy_reco: Tuple for the energy axis: (Emin,Emax,nbins)   
         for the reco energy array
    source_name: name of the source you want to compute the image
    center: SkyCoord of the source
    ObsList: ObservationList to use to compute the psf (could be different that the data_store for G0p9 for the GC for example)


    Returns
    -------
    rmf: `~gammapy.irf.EnergyDispersion`
        Stacked EDISP for a set of observation
    """

    # Here all the observations have a center at less than 2 degrees from the Crab so it will be ok to estimate the mean psf on the Crab source postion (the area is define for offset equal to 2 degrees...)
    emin_true, emax_true, nbin_true = energy_true
    emin_reco, emax_reco, nbin_reco = energy_reco
    energy_true_bins = EnergyBounds.equal_log_spacing(emin_true, emax_true, nbin_true, 'TeV')
    energy_reco_bins = EnergyBounds.equal_log_spacing(emin_reco, emax_reco, nbin_reco, 'TeV')
    rmf = ObsList.make_mean_edisp(position=center, e_true=energy_true_bins, e_reco=energy_reco_bins)
    return rmf


def make_cubes(ereco, etrue, use_etrue, center):
    tmpdir = os.path.expandvars('$GAMMAPY_EXTRA') + "/test_datasets/cube/data"
    outdir = tmpdir
    outdir2 = os.path.expandvars('$GAMMAPY_EXTRA') + '/test_datasets/cube/background'

    if os.path.isdir("data"):
        shutil.rmtree("data")
    if os.path.isdir("background"):
        shutil.rmtree("background")
    Path(outdir2).mkdir()

    ds = DataStore.from_dir("$GAMMAPY_EXTRA/datasets/hess-crab4-hd-hap-prod2")
    ds.copy_obs(ds.obs_table, tmpdir)
    data_store = DataStore.from_dir(tmpdir)
    # Create a background model from the 4 crab run for the counts ouside the exclusion region. it's just for test, normaly you take 8000 thousands AGN runs to build this kind of model
    axes = [ObservationGroupAxis('ZEN_PNT', [0, 49, 90], fmt='edges')]
    obs_groups = ObservationGroups(axes)
    obs_table_with_group_id = obs_groups.apply(data_store.obs_table)
    obs_groups.obs_groups_table.write(outdir2 + "/group-def.fits", overwrite=True)
    # Exclusion sources table
    Tevcatsources = load_catalog_tevcat()
    Tevcatsources.rename_column('coord_dec', 'DEC')
    Tevcatsources.rename_column('coord_ra', 'RA')
    radius = Tevcatsources["size_x"]
    radius[np.where(Tevcatsources["size_x"] < Tevcatsources["size_y"])] = Tevcatsources["size_y"]
    radius[np.isnan(radius)] = 0.3
    c = Column(radius, name='Radius')
    Tevcatsources.add_column(c)
    bgmaker = OffDataBackgroundMaker(data_store, outdir2, run_list=None,
                                     obs_table=obs_table_with_group_id
                                     , ntot_group=obs_groups.n_groups, excluded_sources=Tevcatsources)

    bgmaker.make_model("2D")
    bgmaker.smooth_models("2D")
    bgmaker.save_models("2D")
    bgmaker.save_models(modeltype="2D", smooth=True)

    fn = outdir2 + '/group-def.fits'
    hdu_index_table = bgmaker.make_total_index_table(
        data_store=data_store,
        modeltype='2D',
        out_dir_background_model=outdir2,
        filename_obs_group_table=fn, smooth=True
    )
    fn = outdir + '/hdu-index.fits.gz'
    hdu_index_table.write(fn, overwrite=True)

    offset_band = Angle([0, 2.49], 'deg')

    ref_cube_images = make_empty_cube(image_size=50, energy=ereco, center=center)
    ref_cube_exposure = make_empty_cube(image_size=50, energy=etrue, center=center, data_unit="m2 s")

    data_store = DataStore.from_dir(tmpdir)

    refheader = ref_cube_images.sky_image_ref.to_image_hdu().header
    exclusion_mask = SkyMask.read('$GAMMAPY_EXTRA/datasets/exclusion_masks/tevcat_exclusion.fits')
    exclusion_mask = exclusion_mask.reproject(reference=refheader)

    # Pb with the load psftable for one of the run that is not implemented yet...
    data_store.hdu_table.remove_row(14)

    cube_maker = StackedObsCubeMaker(empty_cube_images=ref_cube_images, empty_exposure_cube=ref_cube_exposure,
                                     offset_band=offset_band, data_store=data_store, obs_table=data_store.obs_table,
                                     exclusion_mask=exclusion_mask, save_bkg_scale=True)
    cube_maker.make_cubes(make_background_image=True, radius=10.)
    obslist = [data_store.obs(id) for id in data_store.obs_table["OBS_ID"]]
    ObsList = ObservationList(obslist)
    mean_psf_cube = make_mean_psf_cube(image_size=50, energy_cube=etrue, center_maps=center, center=center,
                                       ObsList=ObsList,
                                       spectral_index=2.3)
    if use_etrue:
        mean_rmf = make_mean_rmf(energy_true=etrue, energy_reco=ereco, center=center, ObsList=ObsList)

    filename_mask = 'exclusion_mask.fits'
    filename_counts = 'counts_cube.fits'
    filename_bkg = 'bkg_cube.fits'
    filename_significance = 'significance_cube.fits'
    filename_excess = 'excess_cube.fits'
    if use_etrue:
        filename_exposure = 'exposure_cube_etrue.fits'
        filename_psf = 'psf_cube_etrue.fits'
        filename_rmf = 'rmf.fits'
        mean_rmf.write(filename_rmf, clobber=True)
    else:
        filename_exposure = 'exposure_cube.fits'
        filename_psf = 'psf_cube.fits'
    exclusion_mask.write(filename_mask, clobber=True)
    cube_maker.counts_cube.write(filename_counts, format="fermi-counts", clobber=True)
    cube_maker.bkg_cube.write(filename_bkg, format="fermi-counts", clobber=True)
    cube_maker.significance_cube.write(filename_significance, format="fermi-counts", clobber=True)
    cube_maker.excess_cube.write(filename_excess, format="fermi-counts", clobber=True)
    cube_maker.exposure_cube.write(filename_exposure, format="fermi-counts", clobber=True)
    mean_psf_cube.write(filename_psf, format="fermi-counts", clobber=True)


def make_skymaskcube(ereco, center, exclusion_region):
    """
    Compute a SkyCube mask for the region we want to exclude in the fit.

    Parameters
    ----------
    ereco: Tuple for the reconstructed energy axis: (Emin,Emax,nbins)
    center: SkyCoord of the source
    exclusion_region: CircleSkyRegion containing the center and the radius of the position to exclude

    """
    sky_mask_cube = make_empty_cube(image_size=50, energy=ereco, center=center)
    energies = sky_mask_cube.energies(mode='edges').to("TeV")
    coord_center_pix = sky_mask_cube.sky_image_ref.coordinates(mode="center").icrs
    lon = np.tile(coord_center_pix.data.lon.degree, (len(energies) - 1, 1, 1))
    lat = np.tile(coord_center_pix.data.lat.degree, (len(energies) - 1, 1, 1))
    coord_3d_center_pix = SkyCoord(lon, lat, unit="deg")
    index_excluded_region = np.where(
        (exclusion_region.center).separation(coord_3d_center_pix) < exclusion_region.radius)
    sky_mask_cube.data[:] = 1
    sky_mask_cube.data[index_excluded_region] = 0

    sky_mask_cube.write("mask.fits", format="fermi-counts", clobber=True)


if __name__ == '__main__':
    energy_true = [Energy(0.1, "TeV"), Energy(100, "TeV"), 20]
    energy_reco = [Energy(0.5, "TeV"), Energy(40, "TeV"), 5]
    center = SkyCoord(83.63, 22.01, unit='deg').galactic
    make_cubes(ereco=energy_reco, etrue=energy_true, use_etrue=True, center=center)
    make_cubes(ereco=energy_reco, etrue=energy_reco, use_etrue=False, center=center)

    # This is just a test case for the test for the 3d Analysis if we want to exclude a region in the fit
    exclude_region = CircleSkyRegion(SkyCoord(83.60, 21.88, unit='deg'), Angle(0.1, "deg"))
    make_skymaskcube(ereco=energy_reco, center=center, exclusion_region=exclude_region)
