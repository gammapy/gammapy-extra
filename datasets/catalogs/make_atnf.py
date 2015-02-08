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
    return dict(number=number, name=name, description=description)


def _parse_parameter_list(infile, outfile):
    parameters = []

    for line in open(infile).readlines():
        if line[0] != ' ':
            continue

        parameters.append(_parse_parameter_list_line(line))

    table = Table(parameters)
    table = table['number', 'name', 'description']
    table.write(outfile, format='ascii.fixed_width')

def atnf_extract_to_ascii():
    """Extract all catalog info to an ascii file."""
    tool = './psrcat -db_file psrcat.db'
    # cols = 'PSRJ PSRB NAME '
    # cols += 'RAJ DECJ PMRA PMDEC RAJD DECJD GL GB PML PMB '
    # cols += 'DM P0 P1 BINARY DIST_DM DIST_A DIST DIST1 RADDIST '
    # cols += 'SURVEY ASSOC TYPE DATE OSURVEY '
    # cols += 'AGE AGE_I BSURF_I EDOT_I EDOTD2 PMTOT VTRANS BSURF B_LC EDOT'
    execute('{} -v > {}'.format(tool, 'psrcat.version'))
    execute('{} -p > {}'.format(tool, 'psrcat.parameters'))

    # In order to extract the catalog data we need the column names,
    _parse_parameter_list('psrcat.parameters', 'psrcat.columns')
    cols = Table.read('psrcat.columns', format='ascii.fixed_width')['name']
    cols = ' '.join(cols)

    # execute('echo "# {}" > {}'.format(cols, 'psrcat.ascii'))
    cmd = ('{} -o short -c "{}"'
           # ' -nonumber -nohead'
           # -null null
           # ' | egrep -v "unknown survey|---|(hms)"'
           # ' | egrep -v "unknown survey"'
           # ' | sed "s/*/null/g"'
           ' >> {}'
    )
    execute(cmd.format(tool, cols, 'psrcat.ascii'))


def _get_versions():
    lines = open('psrcat_tar/psrcat.version').readlines
    software_version, catalog_version = [_.split()[-1] for _ in lines]
    return software_version, catalog_version


def atnf_cleanup():
    """Clean up the catalog and add some useful info."""
    table = Table.read('psrcat_tar/psrcat.ascii', format='ascii.fixed_width')

    # Add some meta data
    software_version, catalog_version = _get_versions()
    table.meta['version'] = catalog_version
    table.meta['SW_version'] = software_version

    # Add useful extra columns
    # cmd = ['addcol Source_Name "NAME"']
    # cmd.append('addcol RAJ2000 "radiansToDegrees(hmsToRadians(RAJ))"')
    # cmd.append('addcol DEJ2000 "radiansToDegrees(dmsToRadians(DECJ))"')
    # cmd.append('addskycoords icrs galactic RAJ2000 DEJ2000 GLON GLAT')

    filename = 'ATNF_v{}.fits.gz'.format(catalog_version)
    print('Writing {}'.format(filename))
    table.write(filename, overwrite=True)


def main():
    # atnf_download()

    os.chdir('psrcat_tar')
    atnf_extract_to_ascii()
    os.chdir('..')

    # atnf_cleanup()


if __name__ == '__main__':
    main()