"""Add some extra info to the TeVCat catalog.
"""
import numpy as np
from astropy.table import Table


def _tevcat_is_galactic(source_class):
    """Re-group sources into rough categories.
    """
    source_class = source_class.strip()

    GAL = ['Binary', 'Cat. Var.', 'Composite SNR', 'DARK', 'Globular Cluster',
           'Massive Star Cluster', 'PSR', 'PWN', 'SNR/Molec. Cloud',
           'Shell', 'Star Forming Region', 'UNID', 'XRB'
           ]

    EGAL = ['Blazar', 'FRI', 'FSRQ', 'HBL', 'IBL', 'LBL', 'Starburst'
            ]

    if source_class in GAL:
        return 'galactic'
    elif source_class in EGAL:
        return 'extra-galactic'
    # elif source_class == '':
    #     return 'unknown'
    else:
        raise ValueError('Unknown source class: {}'.format(source_class))


def add_extra_info():
    table = Table.read('tevcat.fits.gz')

    print(np.unique(sorted(table['source_type_name'])))
    # import IPython; IPython.embed(); 1/0
    table['IS_GALACTIC'] = [_tevcat_is_galactic(_) for _ in table['source_type_name']]

    filename = 'tevcat_extra.fits.gz'
    print('Writing {}'.format(filename))
    table.write(filename, overwrite=True)


if __name__ == '__main__':
    # add_extra_info()