"""
Make a FITS version of the SNRs in Table 2 of this paper:
http://adsabs.harvard.edu/abs/2014PASA...31...42G

Note that two of these SNRs or in the the Green 2014 catalog:
- G296.7-0.9 (published by Robbins et al. 2011)
- G308.4-1.4 (De Horta et al. 2013 claim only part is an SNR)
"""
from astropy.coordinates import SkyCoord
from astropy.table import Table
from make_green import compute_mean_diameter


def anne_catalog_cleanup(table):

    # Add Galactic coordinates
    pos = SkyCoord(table['RAJ2000'], table['DEJ2000'], unit=('hourangle', 'deg'))
    table['RAJ2000'] = pos.ra.to('deg')
    table['DEJ2000'] = pos.dec.to('deg')
    table['GLON'] = pos.galactic.l.to('deg')
    table['GLAT'] = pos.galactic.b.to('deg')

    table['MajDiam'].unit = 'arcmin'
    table['MinDiam'].unit = 'arcmin'
    table['MeanDiam'] = compute_mean_diameter(table['MajDiam'], table['MinDiam'])

    # Finally, sort and group table columns in a sensible way
    cols = ['Source_Name', 'RAJ2000', 'DEJ2000', 'GLON', 'GLAT',
            'MeanDiam', 'MajDiam', 'MinDiam']
    table = table[cols]

    return table


def main():
    filename = '2014PASA...31...42G_table2.csv'
    print('Reading {}'.format(filename))
    table = Table.read(filename, format='ascii.basic', delimiter='&', guess=False)

    table = anne_catalog_cleanup(table)

    filename = '2014PASA...31...42G_table2.fits.gz'
    print('Writing {}'.format(filename))
    table.write(filename, overwrite=True)


if __name__ == '__main__':
    main()