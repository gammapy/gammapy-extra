"""
This script converts `2HWC.yaml` to ECSV format.

2HWC is the HAWC catalog from this paper:
http://adsabs.harvard.edu/abs/2017ApJ...843...40A

The file `2HWC.yaml` was obtained via email by Colas Rivière
on August 16, 2017

TODO: change to public version and note URL here as soon
as it becomes available on the HAWC webpage
"""
import yaml
from astropy.table import Table, Column


def make_2hwc():
    with open('2HWC.yaml') as fh:
        data = yaml.load(fh)

    from pprint import pprint;
    pprint(data[0])

    table = Table()
    table.meta['catalog_name'] = '2HWC'
    table.meta['reference'] = 'http://adsabs.harvard.edu/abs/2017ApJ...843...40A'

    table['source_name'] = Column(
        data=[_['name'] for _ in data],
        description='Source name',
    )
    table['ra'] = Column(
        data=[_['RA'] for _ in data],
        description='Right Ascension (J2000)', unit='deg', format='.3f',
    )
    table['dec'] = Column(
        data=[_['Dec'] for _ in data],
        description='Declination (J2000)', unit='deg', format='.3f',
    )
    table['glon'] = Column(
        data=[_['l'] for _ in data],
        description='Galactic longitude', unit='deg', format='.3f',
    )
    table['glat'] = Column(
        data=[_['b'] for _ in data],
        description='Galactic latitude', unit='deg', format='.3f',
    )
    table['pos_err'] = Column(
        data=[_['position uncertainty'] for _ in data],
        description='Position error (1 sigma)', unit='deg', format='.3f',
    )
    table['search_radius'] = Column(
        data=[_['search radius'] for _ in data],
        description='Search radius (see Table 2 in the paper)', unit='deg', format='.1f',
    )
    table['ts'] = Column(
        data=[_['TS'] for _ in data],
        description='Detection test statistic', format='.1f',
    )
    # For some sources one, for some two spectra are given
    # In the catalog we always put two, filling `NaN` values
    # for the second if only one is given.
    add_flux_measurements(table, data, idx=0)
    add_flux_measurements(table, data, idx=1)

    filename = '2HWC.ecsv'
    print(f'Writing {filename}')
    table.write(filename, format='ascii.ecsv', overwrite=True)


def add_flux_measurements(table, data, idx):
    def get_flux_measurement(flux_measurements):
        if idx < len(flux_measurements):
            return flux_measurements[idx]
        else:
            return {key: float('nan') for key in flux_measurements[0]}

    flux_data = [get_flux_measurement(_['flux measurements']) for _ in data]

    table[f'spec{idx}_dnde'] = Column(
        data=[_['flux'] for _ in flux_data],
        description='Differential flux at 7 TeV', unit='cm-2 s-1 TeV-1', format='.3g',
    )
    table[f'spec{idx}_dnde_err'] = Column(
        data=[_['flux uncertainty'] for _ in flux_data],
        description=f'Statistical error on spec{idx}_dnde', unit='cm-2 s-1 TeV-1', format='.3g',
    )
    table[f'spec{idx}_index'] = Column(
        data=[_['index'] for _ in flux_data],
        description='Spectral index', format='.2f',
    )
    table[f'spec{idx}_index_err'] = Column(
        data=[_['index uncertainty'] for _ in flux_data],
        description=f'Statistical error on spec{idx}_index', format='.2f',
    )
    table[f'spec{idx}_radius'] = Column(
        data=[_['tested radius'] for _ in flux_data],
        description=f'Spectrum test radius', unit='deg', format='.3f',
    )


if __name__ == '__main__':
    make_2hwc()
