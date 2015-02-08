"""Make a FITS version of the ATNF Pulsar catalog.

Unfortunately the catalog is not available in a useful format.
I've contacted both the ATNF maintainer and Vizier ... so far no success.

So here we download the ATNF database and software, compile it
and run it to extract the catalog into an ascii format, which we
then augment with some useful info and store in FITS format.

http://www.atnf.csiro.au/people/pulsar/psrcat/download.html
http://www.atnf.csiro.au/people/pulsar/psrcat/catalogueHistory.html

"""
import logging
logging.basicConfig(level=logging.INFO)
import os
import subprocess
from astropy.table import Table
from astropy.coordinates import SkyCoord


# http://astropy.readthedocs.org/en/latest/io/ascii/read.html#bad-or-missing-values
MISSING_DATA_FILL_VALUE = '__ASDF__'

def execute(cmd):
    print('EXECUTING: {}'.format(cmd))
    subprocess.call(cmd, shell=True)


def atnf_download():
    """Download ATNF pulsar catalog data and software and compile it."""
    url = 'http://www.atnf.csiro.au/research/pulsar/psrcat/psrcat_pkg.tar.gz'
    execute('wget {}'.format(url))
    execute('tar zxvf psrcat_pkg.tar.gz')
    execute('cd psrcat_tar && source makeit')


def _parse_parameter_list_line(line):
    """
    Example: '  210. GLF0\t\tGlitch permanent pulse frequency increment (Hz)\n'
    """
    number = line[2:5]
    tokens = line[7:].split('\t')
    name = tokens[0]
    description = tokens[-1].strip()

    # TODO: we could extract the unit from the description string here.

    return dict(number=number, name=name, description=description)


def _parse_parameter_list(infile, outfile):
    parameters = []

    for line in open(infile).readlines():
        if line[0] != ' ':
            continue

        parameter = _parse_parameter_list_line(line)

        # We have to remove some parameters to prevent the
        # tool that extracts the data from segfaulting
        skipcols = 'ELAT ELONG C1 C2 C3 C4 PAR1 PAR2 PAR3 PAR4'.split()

        if parameter['name'] in skipcols:
            continue
        # if parameter['name'] != 'PSRJ':
        #     continue

        parameters.append(parameter)

    table = Table(parameters)
    table = table['number', 'name', 'description']
    table.write(outfile, format='ascii.fixed_width')


# TODO: For now we don't extract all columns because it results
# in a ``psrcat`` segfault.
# I've reported this via the ATNF feedback form on 2014-02-08.
# For now we'll use a hand-selected list of useful columns
def _get_cols(use_all=False):
    if use_all:
        cols = Table.read('psrcat.columns', format='ascii.fixed_width')['name']
        cols = ' '.join(cols)
    else:
        cols = 'PSRJ PSRB NAME '
        cols += 'RAJ DECJ PMRA PMDEC RAJD DECJD GL GB PML PMB '
        cols += 'DM P0 P1 BINARY DIST_DM DIST_A DIST DIST1 RADDIST '
        cols += 'SURVEY ASSOC TYPE DATE OSURVEY '
        cols += 'AGE AGE_I BSURF_I EDOT_I EDOTD2 PMTOT VTRANS BSURF B_LC EDOT'

    return cols.split()


def atnf_extract_to_ascii():
    """Extract all catalog info to an ascii file."""
    tool = './psrcat -db_file psrcat.db'
    execute('{} -v > {}'.format(tool, 'psrcat.version'))
    execute('{} -p > {}'.format(tool, 'psrcat.parameters'))

    # In order to extract the catalog data we need the column names,
    _parse_parameter_list('psrcat.parameters', 'psrcat.columns')
    cols = _get_cols()

    # execute('echo "# {}" > {}'.format(cols, 'psrcat.ascii'))
    cmd = '{} -o short -c "{}"'.format(tool, ' '.join(cols))
    cmd += ' -nonumber -nohead'
    cmd += ' -null {}'.format(MISSING_DATA_FILL_VALUE)
    cmd += ' > {}'.format('psrcat.ascii')
    execute(cmd)


def _get_versions():
    lines = open('psrcat_tar/psrcat.version').readlines()
    software_version, catalog_version = [_.split()[-1] for _ in lines]
    return software_version, catalog_version


def atnf_cleanup():
    """Clean up the catalog and add some useful info."""
    cols = _get_cols()
    table = Table.read('psrcat_tar/psrcat.ascii', format='ascii.basic',
               names=cols, guess=False,
               fill_values=[(MISSING_DATA_FILL_VALUE, '0')],
    )
    # Add some meta data
    software_version, catalog_version = _get_versions()
    table.meta['version'] = catalog_version
    table.meta['SW_VERS'] = software_version

    # Add useful extra columns
    pos = SkyCoord(table['RAJ'], table['DECJ'], unit='deg')
    table['RAJ2000'] = pos.ra.deg
    table['DEJ2000'] = pos.dec.deg
    table['GLON'] = pos.galactic.l.deg
    table['GLAT'] = pos.galactic.b.deg

    # table.show_in_browser(jsviewer=True)

    filename = 'ATNF_v{}.fits.gz'.format(catalog_version)
    print('Writing {}'.format(filename))
    table.write(filename, overwrite=True)


def main():
    # atnf_download()

    os.chdir('psrcat_tar')
    atnf_extract_to_ascii()
    os.chdir('..')

    atnf_cleanup()


if __name__ == '__main__':
    main()