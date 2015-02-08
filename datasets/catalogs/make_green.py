"""
Make a FITS version of Green's SNR catalog.

What this script does:
- Download the catalog from Vizier
- Add some convenient extra columns
"""
# TODO: remove this once the issue is fixed:
import sys
if sys.version_info[0] == 3:
    print("This currently doesn't work on Python 3 ... use Python 2 instead.")
    print('https://github.com/astropy/astroquery/issues/477')
    sys.exit(1)

import numpy as np
from astropy.coordinates import SkyCoord
from astropy.table import Column


def green_catalog_download():
    # This allows easy access to Vizier tables:
    # https://astroquery.readthedocs.org/en/latest/vizier/vizier.html
    from astroquery.vizier import Vizier
    Vizier.ROW_LIMIT = -1
    # This is the 2014-05 version of Green's catalog
    # http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=VII/272
    results = Vizier.get_catalogs(['VII/272'])
    table = results[0]
    return table


def green_catalog_cleanup(table):
    # The table has float columns in deg `_RAJ2000`, `_DEJ2000`
    # as well as string columns in hms `RAJ2000` and in dms `DEJ2000`
    # Here we convert to the more common form where `RAJ2000` and
    # `DEJ2000` are float columns and remove the string columns
    # table['RAJ2000'] = table['_RAJ2000']
    # table['DEJ2000'] = table['_DEJ2000']
    table.remove_columns(['RAJ2000', 'DEJ2000'])
    table.rename_column('_RAJ2000', 'RAJ2000')
    table.rename_column('_DEJ2000', 'DEJ2000')

    # Add Galactic coordinates
    skycoord = SkyCoord(table['RAJ2000'], table['DEJ2000'], unit='deg').galactic
    table['GLON'], table['GLAT'] = skycoord.l, skycoord.b

    # The extension unit is `arcm`, which is a bit cryptic ... change to `arcmin`:
    table['MajDiam'].unit = 'arcmin'
    table['MinDiam'].unit = 'arcmin'

    # Add average radius as geometric mean (preserves area)
    radius = np.sqrt(table['MajDiam'] * table['MinDiam'])
    # If no `MinDiam` is given, use `MaxDiam` as mean radius
    with np.errstate(invalid='ignore'):
        radius = np.where(table['MinDiam'] > 0, radius, table['MajDiam'])
    table['MeanDiam'] = Column(radius, unit='arcmin')

    table.rename_column('SNR', 'Source_Name')

    # Finally, sort and group table columns in a sensible way
    cols = ['Source_Name', 'RAJ2000', 'DEJ2000', 'GLON', 'GLAT',
            'MeanDiam', 'MajDiam', 'MinDiam', 'u_MinDiam',
            'l_S_1GHz_', 'S_1GHz_', 'u_S_1GHz_',
            'Sp-Index', 'u_Sp-Index',
            'type', 'Names']
    # Make sure we don't accidentally remove columns
    assert set(cols) == set(table.colnames)
    table = table[cols]

    return table


def main():
    table = green_catalog_download()
    table = green_catalog_cleanup(table)
    filename = 'Green_2014-05.fits'
    print('Writing {}'.format(filename))
    table.write(filename, overwrite=True)


if __name__ == '__main__':
    main()