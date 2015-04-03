"""
Generate region file from the catalogs.
"""

from astropy.table import Table
from gammapy.catalog import to_ds9_region


if __name__ == '__main__':
    filenames = ['ATNF_v1.51.fits.gz', 'Green_2014-05.fits.gz',
                 '2014PASA...31...42G_table2.fits.gz']
    radius_columns = [None, 'Dmean', 'Dmean']
    colors = ['yellow', 'cyan', 'red']

    for filename, column, color in zip(filenames, radius_columns, colors):
        catalog = Table.read(filename)
        if column == 'Dmean':
            # Convert arcmin to deg
            catalog['Dmean'] /= 120.
        outfilename = filename.replace('fits.gz', 'reg')
        print('Writing {}'.format(outfilename))
        with open(outfilename, 'w') as region_file:
            region_file.write(to_ds9_region(catalog, radius=column, label='Source_Name',
                                            color=color, width=2))
