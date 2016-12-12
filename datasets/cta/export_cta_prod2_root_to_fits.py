"""
Convert CTA's IRF from ROOT to FITS format.
The ROOT files originate from the official release which can be
found here: 
https://portal.cta-observatory.org/CTA_Observatory/performance/SitePages/Home.aspx
""" 
try:
    from ROOT import TFile
except ImportError:
    raise

import os
import re

from astropy.io import fits
import astropy.units as u

import numpy as np

from gammapy.utils.root.convert import hist1d_to_table, TH2_to_FITS_data
from gammapy.utils.nddata import BinnedDataAxis
from gammapy.irf import EnergyDispersion
from gammapy.irf import EffectiveAreaTable

def root_to_fits_cta_perf(in_dir, in_file):
    """
    Convert ROOT CTA performance file to FITS format

    Parameters
    ----------
    in_file : str
        input ROOT file name
    output_dir : str
        output directory
    """
    root_file = TFile(in_dir + '/' + in_file)
    
    # Bg rate
    bg_rate = hist1d_to_table(hist=root_file.Get('BGRate'))
    # ENERG_LO
    bg_rate.rename_column('x_bin_lo', 'ENERG_LO')
    bg_rate['ENERG_LO'].unit = u.TeV
    bg_rate['ENERG_LO'].format = 'E'
    bg_rate.replace_column('ENERG_LO', 10**(bg_rate['ENERG_LO']))
    # ENERG_HI
    bg_rate.rename_column('x_bin_hi', 'ENERG_HI')
    bg_rate['ENERG_HI'].unit = u.TeV
    bg_rate['ENERG_HI'].format = 'E'
    bg_rate.replace_column('ENERG_HI', 10**(bg_rate['ENERG_HI']))
    # BGD
    bg_rate.rename_column('y', 'BGD')
    bg_rate['BGD'].unit = u.Hz
    bg_rate['BGD'].format = 'E'

    bg_rate_hdu = fits.BinTableHDU.from_columns(
        [fits.Column('ENERG_LO',
                     bg_rate['ENERG_LO'].format,
                     unit=bg_rate['ENERG_LO'].unit.to_string(),
                     array=bg_rate['ENERG_LO']),
         fits.Column('ENERG_HI',
                     bg_rate['ENERG_HI'].format,
                     unit=bg_rate['ENERG_HI'].unit.to_string(),
                     array=bg_rate['ENERG_HI']),
         fits.Column('BGD',
                     bg_rate['BGD'].format,
                     unit=bg_rate['BGD'].unit.to_string(),
                     array=bg_rate['BGD'])]
    )

    bg_rate_hdu.header.set("EXTNAME", "BACKGROUND")

    # EffectiveAreaEtrue
    area = hist1d_to_table(hist=root_file.Get('EffectiveAreaEtrue'))
    # ENERG_LO
    area.rename_column('x_bin_lo', 'ENERG_LO')
    area['ENERG_LO'].unit = u.TeV
    area['ENERG_LO'].format = 'E'
    area.replace_column('ENERG_LO', 10**(area['ENERG_LO']))
    # ENERG_HI
    area.rename_column('x_bin_hi', 'ENERG_HI')
    area['ENERG_HI'].unit = u.TeV
    area['ENERG_HI'].format = 'E'
    area.replace_column('ENERG_HI', 10**(area['ENERG_HI']))
    # EFFAREA
    area.rename_column('y', 'SPECRESP')
    area['SPECRESP'].unit = u.meter * u.meter
    area['SPECRESP'].format = 'E'
    area.replace_column('SPECRESP', area['SPECRESP'])
    
    area_hdu = fits.BinTableHDU.from_columns(
        [fits.Column('ENERG_LO',
                     area['ENERG_LO'].format,
                     unit=area['ENERG_LO'].unit.to_string(),
                     array=area['ENERG_LO']),
         fits.Column('ENERG_HI',
                     area['ENERG_HI'].format,
                     unit=area['ENERG_HI'].unit.to_string(),
                     array=area['ENERG_HI']),
         fits.Column('SPECRESP',
                     area['SPECRESP'].format,
                     unit=area['SPECRESP'].unit.to_string(),
                     array=area['SPECRESP'])]
    )

    area_hdu.header.set("EXTNAME", "SPECRESP")


    # PSF
    psf = hist1d_to_table(hist=root_file.Get('AngRes'))
    # ENERG_LO
    psf.rename_column('x_bin_lo', 'ENERG_LO')
    psf['ENERG_LO'].unit = u.TeV
    psf['ENERG_LO'].format = 'E'
    psf.replace_column('ENERG_LO', 10**(psf['ENERG_LO']))
    # ENERG_HI
    psf.rename_column('x_bin_hi', 'ENERG_HI')
    psf['ENERG_HI'].unit = u.TeV
    psf['ENERG_HI'].format = 'E'
    psf.replace_column('ENERG_HI', 10**(psf['ENERG_HI']))
    # PSF68
    psf.rename_column('y', 'PSF68')
    psf['PSF68'].unit = u.degree
    psf['PSF68'].format = 'E'
    psf.replace_column('PSF68', psf['PSF68'])

    psf_hdu = fits.BinTableHDU.from_columns(
        [fits.Column('ENERG_LO',
                     psf['ENERG_LO'].format,
                     unit=psf['ENERG_LO'].unit.to_string(),
                     array=psf['ENERG_LO']),
         fits.Column('ENERG_HI',
                     psf['ENERG_HI'].format,
                     unit=psf['ENERG_HI'].unit.to_string(),
                     array=psf['ENERG_HI']),
         fits.Column('PSF68',
                     psf['PSF68'].format,
                     unit=psf['PSF68'].unit.to_string(),
                     array=psf['PSF68'])]
    )

    psf_hdu.header.set("EXTNAME", "POINT SPREAD FUNCTION")

    # MigMatrix (x=e_reco, y=e_true, z=prob)
    histo_edisp = root_file.Get('MigMatrix')
    # data
    data = TH2_to_FITS_data(hist=histo_edisp, flipx=False)
    # get e_reco
    x_axis = histo_edisp.GetXaxis()
    x_nbins = x_axis.GetNbins()
    x_min = 10**(x_axis.GetBinLowEdge(1))
    x_max = 10**(x_axis.GetBinUpEdge(x_nbins))
    e_reco = BinnedDataAxis.logspace(x_min, x_max, x_nbins, unit=u.TeV)
    # get e_true
    y_axis = histo_edisp.GetYaxis()
    y_nbins = y_axis.GetNbins()
    y_min = 10**(y_axis.GetBinLowEdge(1))
    y_max = 10**(y_axis.GetBinUpEdge(y_nbins))
    e_true = BinnedDataAxis.logspace(y_min, y_max, y_nbins, unit=u.TeV)
    e_disp = EnergyDispersion(e_true=e_true, e_reco=e_reco)
    e_disp.e_true = e_true
    e_disp.e_reco = e_reco
    e_disp.data = data

    edisp_hdus = e_disp.to_hdulist()

    hdulist = fits.HDUList([edisp_hdus[0],
                            area_hdu,
                            psf_hdu,
                            edisp_hdus[1], edisp_hdus[2],
                            bg_rate_hdu])

    name = re.split('.root', str(in_file))[0]
    output_file = in_dir + '/' + name + '.fits'
    hdulist.writeto(output_file, clobber=True)
    
site = ['South', 'North']
opti = ['0.5h', '5h', '50h']
prod = '20150511'

repo = './perf_prod2/'

for isite in site:
    prod_dir = 'CTA-Performance-' + isite + '-' + prod + '/'
    for iopti in opti:
        in_file = 'CTA-Performance-' + isite + '-' + iopti + '_' + prod + '.root'
        print('Working on {}'.format(in_file))
        root_to_fits_cta_perf(repo + '/'+prod_dir, in_file)
        print('done.')
