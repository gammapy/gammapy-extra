# coding: utf8
"""
Convert CTA's IRF from ROOT to FITS format.
Internal IRF from the consortium.
"""
try:
    from ROOT import TFile
except ImportError:
    raise

import re
import os

from os import listdir
from os.path import isfile, join

from astropy.io import fits
import astropy.units as u
from astropy.table import Table

import numpy as np

from gammapy.utils.root.convert import hist1d_to_table, TH2_to_FITS_data

def convert_root_to_fits(in_dir, in_file, out_dir):
    """
    Convert ROOT CTA performance file to FITS format

    Parameters
    ----------
    in_dir : str
        input directory
    in_file : str
        input ROOT file name
    out_dir : str
        output directory

    Todo : meta data and more
    """
    root_file = TFile(in_dir + '/' + in_file)

    # Background rate
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

    # Sensitivity
    sens = hist1d_to_table(hist=root_file.Get('DiffSens'))
    # ENERG_LO
    sens.rename_column('x_bin_lo', 'ENERG_LO')
    sens['ENERG_LO'].unit = u.TeV
    sens['ENERG_LO'].format = 'E'
    sens.replace_column('ENERG_LO', 10**(sens['ENERG_LO']))
    # ENERG_HI
    sens.rename_column('x_bin_hi', 'ENERG_HI')
    sens['ENERG_HI'].unit = u.TeV
    sens['ENERG_HI'].format = 'E'
    sens.replace_column('ENERG_HI', 10**(sens['ENERG_HI']))
    # BGD
    sens.rename_column('y', 'SENSITIVITY')
    sens['SENSITIVITY'].unit = u.erg / (u.cm * u.cm * u.s)
    sens['SENSITIVITY'].format = 'E'

    sens_hdu = fits.BinTableHDU.from_columns(
        [fits.Column('ENERG_LO',
                     sens['ENERG_LO'].format,
                     unit=sens['ENERG_LO'].unit.to_string(),
                     array=sens['ENERG_LO']),
         fits.Column('ENERG_HI',
                     sens['ENERG_HI'].format,
                     unit=sens['ENERG_HI'].unit.to_string(),
                     array=sens['ENERG_HI']),
         fits.Column('SENSITIVITY',
                     sens['SENSITIVITY'].format,
                     unit=sens['SENSITIVITY'].unit.to_string(),
                     array=sens['SENSITIVITY'])]
    )
    sens_hdu.header.set("EXTNAME", "SENSITIVITY")

    # Root file
    # EestOverEtrue (x=e_true, y=migra, z=counts)
    # EnergyDispersion2D
    # ETRUE_LO, ETRUE_HI (true energy)
    # MIGRA_LO, MIGRA_HI (energy migration E_reco/E_true, 1/3 < mu < 3)
    # THETA_LO, THETA_HI (offset)
    # MATRIX (probability)
    histo_matrix = root_file.Get('EestOverEtrue')

    # get e_true (on s'intéresse a la définition des bins)
    proj_x = histo_matrix.ProfileX('x_proj')
    e_true = hist1d_to_table(hist=proj_x)
    # ETRUE_LO
    e_true.rename_column('x_bin_lo', 'ETRUE_LO')
    e_true['ETRUE_LO'].unit = u.TeV
    e_true['ETRUE_LO'].format = str(len(e_true['ETRUE_LO'])) + 'E'
    e_true.replace_column('ETRUE_LO', 10**(e_true['ETRUE_LO']))
    # ETRUE_HI
    e_true.rename_column('x_bin_hi', 'ETRUE_HI')
    e_true['ETRUE_HI'].unit = u.TeV
    e_true['ETRUE_HI'].format = str(len(e_true['ETRUE_HI'])) + 'E'
    e_true.replace_column('ETRUE_HI', 10**(e_true['ETRUE_HI']))

    # get migration (on s'intéresse a la définition des bins)
    proj_y = histo_matrix.ProfileY('y_proj')
    migra = hist1d_to_table(hist=proj_y)
    # MIGRA_LO
    migra.rename_column('x_bin_lo', 'MIGRA_LO')
    migra['MIGRA_LO'].unit = u.Unit('')
    migra['MIGRA_LO'].format = str(len(migra['MIGRA_LO'])) + 'E'
    # MIGRA_HI
    migra.rename_column('x_bin_hi', 'MIGRA_HI')
    migra['MIGRA_HI'].unit = u.Unit('')
    migra['MIGRA_HI'].format = str(len(migra['MIGRA_HI'])) + 'E'

    # Define theta (trick to get the good data for a given offset (only one offset is stored))
    theta_lo = [0., 1.]
    theta_hi = [1., 2.]
    theta = Table([theta_lo, theta_hi], names=('THETA_LO', 'THETA_HI'))
    theta['THETA_LO'].unit = u.degree
    theta['THETA_LO'].format = str(len(theta['THETA_LO'])) + 'E'
    theta['THETA_HI'].unit = u.degree
    theta['THETA_HI'].format = str(len(theta['THETA_HI'])) + 'E'

    # Deal with the energy dispersion
    mig_matrix = TH2_to_FITS_data(hist=histo_matrix, flipx=False)
    extended_mig_matrix = np.resize(mig_matrix, (len(theta_lo),
                                                 mig_matrix.shape[0],
                                                 mig_matrix.shape[1]))
    matrix = Table([extended_mig_matrix.ravel()], names=['MATRIX'])
    matrix['MATRIX'].unit = u.Unit('')
    dim_matrix = len(e_true['ETRUE_LO']) * \
        len(migra['MIGRA_LO']) * len(theta['THETA_LO'])
    matrix['MATRIX'].format = str(dim_matrix) + 'E'

    migra_hdu = fits.BinTableHDU.from_columns(
        [fits.Column(name='ETRUE_LO',
                     format=e_true['ETRUE_LO'].format,
                     unit=e_true['ETRUE_LO'].unit.to_string(),
                     array=np.atleast_2d(e_true['ETRUE_LO'])),
         fits.Column('ETRUE_HI',
                     e_true['ETRUE_HI'].format,
                     unit=e_true['ETRUE_HI'].unit.to_string(),
                     array=np.atleast_2d(e_true['ETRUE_HI'])),
         fits.Column('MIGRA_LO',
                     migra['MIGRA_LO'].format,
                     unit=migra['MIGRA_LO'].unit.to_string(),
                     array=np.atleast_2d(migra['MIGRA_LO'])),
         fits.Column('MIGRA_HI',
                     migra['MIGRA_HI'].format,
                     unit=migra['MIGRA_HI'].unit.to_string(),
                     array=np.atleast_2d(migra['MIGRA_HI'])),
         fits.Column('THETA_LO',
                     theta['THETA_LO'].format,
                     unit=theta['THETA_LO'].unit.to_string(),
                     array=np.atleast_2d(theta['THETA_LO'])),
         fits.Column('THETA_HI',
                     theta['THETA_HI'].format,
                     unit=theta['THETA_HI'].unit.to_string(),
                     array=np.atleast_2d(theta['THETA_HI'])),
         fits.Column('MATRIX',
                     matrix['MATRIX'].format,
                     unit=matrix['MATRIX'].unit.to_string(),
                     array=np.expand_dims(matrix['MATRIX'], 0))]
    )

    migra_hdu.header.set("TDIM7",
                         "(" + str(len(e_true['ETRUE_LO'])) + "," + str(len(migra['MIGRA_LO'])) + "," + str(len(theta['THETA_LO'])) + ")")
    migra_hdu.header.set("EXTNAME", "ENERGY DISPERSION",
                         "name of this binary table extension ")

    # Primary header
    n = np.arange(100.0)
    primary_hdu = fits.PrimaryHDU(n)

    # Fill HDU
    hdulist = fits.HDUList([primary_hdu,
                            area_hdu,
                            psf_hdu,
                            migra_hdu,
                            bg_rate_hdu,
                            sens_hdu])

    # Save file
    name = re.split('.root', str(in_file))[0]
    output_file = out_dir + '/' + name + '.fits.gz'
    hdulist.writeto(output_file, clobber=True)

# @Christoph, file is available here: https://forge.in2p3.fr/attachments/download/31444
in_dir = 'CTA-Performance-South-IRFreco1_ROOT_20170627'
out_dir = os.getcwd() + '/' + in_dir + '_fits'

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

from os import listdir
from os.path import isfile, join
files_to_convert = [f for f in listdir(in_dir) if isfile(join(in_dir, f))]

for f in files_to_convert:

    print ('Working on {}'.format(f))
    convert_root_to_fits(in_dir, f, out_dir)

print('Job done.')
