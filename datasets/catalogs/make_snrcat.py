"""
Make a FITS version of the SNRCat.

The input CVS file was obtained from Gilles Ferrand via email on 2015-01-30.
"""
from astropy.units import Quantity
from astropy.coordinates import SkyCoord
from astropy.table import Table
from make_green import compute_mean_diameter


def main():
    table = Table.read('SNRcat20150129.csv', format='ascii')

    # Rename and add some useful columns
    table.rename_column('SNR', 'Source_Name')

    pos = SkyCoord(table['alpha'], table['delta'], unit=('hourangle', 'deg'))
    table['RAJ2000'] = pos.ra.to('deg')
    table['DEJ2000'] = pos.dec.to('deg')
    table['GLON'] = pos.galactic.l.to('deg')
    table['GLAT'] = pos.galactic.b.to('deg')
    mean_diameter = compute_mean_diameter(table['angular_size_major'], table['angular_size_minor'])
    table['MeanDiam'] = Quantity(mean_diameter, 'arcmin')

    # This is useful for checking the output
    # table.show_in_browser(jsviewer=True)

    filename = 'SNRcat20150129.fits.gz'
    print('Writing {}'.format(filename))
    table.write(filename, overwrite=True)


if __name__ == '__main__':
    main()