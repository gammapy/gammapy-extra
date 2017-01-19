"""
Convert CTA's IRF from ROOT to FITS format.

The ROOT files originate from the official release which can be found here:
https://portal.cta-observatory.org/CTA_Observatory/performance/SitePages/Home.aspx
"""
from astropy.io import fits
import astropy.units as u
from gammapy.utils.root.convert import hist1d_to_table, TH2_to_FITS_data
from gammapy.utils.nddata import BinnedDataAxis
from gammapy.irf import EnergyDispersion


def cta_perf_root_to_fits(root_filename, fits_filename):
    """
    Convert CTA performance file from ROOT to FITS format.

    Parameters
    ----------
    root_filename : str
        Input ROOT filename
    fits_filename : str
        Output FITS filename
    """
    from ROOT import TFile

    print('Reading {}'.format(root_filename))
    root_file = TFile(root_filename)

    # Bg rate
    bg_rate = hist1d_to_table(hist=root_file.Get('BGRate'))
    # ENERG_LO
    bg_rate.rename_column('x_bin_lo', 'ENERG_LO')
    bg_rate['ENERG_LO'].unit = u.TeV
    bg_rate['ENERG_LO'].format = 'E'
    bg_rate.replace_column('ENERG_LO', 10 ** (bg_rate['ENERG_LO']))
    # ENERG_HI
    bg_rate.rename_column('x_bin_hi', 'ENERG_HI')
    bg_rate['ENERG_HI'].unit = u.TeV
    bg_rate['ENERG_HI'].format = 'E'
    bg_rate.replace_column('ENERG_HI', 10 ** (bg_rate['ENERG_HI']))
    # BGD
    bg_rate.rename_column('y', 'BGD')
    bg_rate['BGD'].unit = u.Hz
    bg_rate['BGD'].format = 'E'

    bg_rate_hdu = fits.BinTableHDU.from_columns([
        fits.Column('ENERG_LO',
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
                    array=bg_rate['BGD']),
    ])

    bg_rate_hdu.header.set("EXTNAME", "BACKGROUND")

    # EffectiveAreaEtrue
    area = hist1d_to_table(hist=root_file.Get('EffectiveAreaEtrue'))
    # ENERG_LO
    area.rename_column('x_bin_lo', 'ENERG_LO')
    area['ENERG_LO'].unit = u.TeV
    area['ENERG_LO'].format = 'E'
    area.replace_column('ENERG_LO', 10 ** (area['ENERG_LO']))
    # ENERG_HI
    area.rename_column('x_bin_hi', 'ENERG_HI')
    area['ENERG_HI'].unit = u.TeV
    area['ENERG_HI'].format = 'E'
    area.replace_column('ENERG_HI', 10 ** (area['ENERG_HI']))
    # EFFAREA
    area.rename_column('y', 'SPECRESP')
    area['SPECRESP'].unit = u.meter * u.meter
    area['SPECRESP'].format = 'E'
    area.replace_column('SPECRESP', area['SPECRESP'])

    area_hdu = fits.BinTableHDU.from_columns([
        fits.Column('ENERG_LO',
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
                    array=area['SPECRESP']),
    ])

    area_hdu.header.set("EXTNAME", "SPECRESP")

    # PSF
    psf = hist1d_to_table(hist=root_file.Get('AngRes'))
    # ENERG_LO
    psf.rename_column('x_bin_lo', 'ENERG_LO')
    psf['ENERG_LO'].unit = u.TeV
    psf['ENERG_LO'].format = 'E'
    psf.replace_column('ENERG_LO', 10 ** (psf['ENERG_LO']))
    # ENERG_HI
    psf.rename_column('x_bin_hi', 'ENERG_HI')
    psf['ENERG_HI'].unit = u.TeV
    psf['ENERG_HI'].format = 'E'
    psf.replace_column('ENERG_HI', 10 ** (psf['ENERG_HI']))
    # PSF68
    psf.rename_column('y', 'PSF68')
    psf['PSF68'].unit = u.degree
    psf['PSF68'].format = 'E'
    psf.replace_column('PSF68', psf['PSF68'])

    psf_hdu = fits.BinTableHDU.from_columns([
        fits.Column('ENERG_LO',
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
                    array=psf['PSF68']),
    ])

    psf_hdu.header.set("EXTNAME", "POINT SPREAD FUNCTION")

    # MigMatrix (x=e_reco, y=e_true, z=prob)
    histo_edisp = root_file.Get('MigMatrix')
    # data
    data = TH2_to_FITS_data(hist=histo_edisp, flipx=False)
    # get e_reco
    x_axis = histo_edisp.GetXaxis()
    x_nbins = x_axis.GetNbins()
    x_min = 10 ** (x_axis.GetBinLowEdge(1))
    x_max = 10 ** (x_axis.GetBinUpEdge(x_nbins))
    e_reco = BinnedDataAxis.logspace(x_min, x_max, x_nbins, unit=u.TeV)
    # get e_true
    y_axis = histo_edisp.GetYaxis()
    y_nbins = y_axis.GetNbins()
    y_min = 10 ** (y_axis.GetBinLowEdge(1))
    y_max = 10 ** (y_axis.GetBinUpEdge(y_nbins))
    e_true = BinnedDataAxis.logspace(y_min, y_max, y_nbins, unit=u.TeV)
    e_disp = EnergyDispersion(data=data, e_true=e_true, e_reco=e_reco)

    edisp_hdus = e_disp.to_hdulist()

    # Sensitivity
    sens = hist1d_to_table(hist=root_file.Get('DiffSens'))
    # ENERG_LO
    sens.rename_column('x_bin_lo', 'ENERG_LO')
    sens['ENERG_LO'].unit = u.TeV
    sens['ENERG_LO'].format = 'E'
    sens.replace_column('ENERG_LO', 10 ** (sens['ENERG_LO']))
    # ENERG_HI
    sens.rename_column('x_bin_hi', 'ENERG_HI')
    sens['ENERG_HI'].unit = u.TeV
    sens['ENERG_HI'].format = 'E'
    sens.replace_column('ENERG_HI', 10 ** (sens['ENERG_HI']))
    # BGD
    sens.rename_column('y', 'SENSITIVITY')
    sens['SENSITIVITY'].unit = u.erg / (u.cm * u.cm * u.s)
    sens['SENSITIVITY'].format = 'E'

    sens_hdu = fits.BinTableHDU.from_columns([
        fits.Column('ENERG_LO',
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
                    array=sens['SENSITIVITY']),
    ])

    sens_hdu.header.set("EXTNAME", "SENSITIVITY")

    hdulist = fits.HDUList([
        edisp_hdus[0], area_hdu, psf_hdu,
        edisp_hdus[1], edisp_hdus[2],
        bg_rate_hdu, sens_hdu,
    ])

    print('Writing {}'.format(fits_filename))
    hdulist.writeto(fits_filename, overwrite=True)


def main():
    sites = ['South', 'North']
    obs_times = ['0.5h', '5h', '50h']
    prod = '20150511'
    repo = './perf_prod2/'

    for site in sites:
        prod_dir = 'CTA-Performance-' + site + '-' + prod + '/'
        for obs_time in obs_times:
            base_filename = 'CTA-Performance-' + site + '-' + obs_time + '_' + prod
            root_filename = repo + '/' + prod_dir + '/' + base_filename + '.root'
            fits_filename = repo + '/' + prod_dir + '/' + base_filename + '.fits'

            cta_perf_root_to_fits(root_filename, fits_filename)


if __name__ == '__main__':
    main()
