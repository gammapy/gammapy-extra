"""
Make a nice version of the TeGeV Catalogue @ ASDC

http://www.asdc.asi.it/tgevcat/
http://adsabs.harvard.edu/abs/2015arXiv151008681C

(v2, July 2015)

The input file `asdc-tegev.csv` was obained by going to the website,
selecting "all columns" and "CSV export" and saving the file.


"""
from pathlib import Path
from astropy.io import ascii
from astropy.table import Table
from astropy.coordinates import Angle

filename = 'asdc-tegev.csv'

# Remove unicode characters -- they only cause problems
print('Reading {}'.format(filename))
text = Path(filename).read_text()
for a, b in [('\u2013', '-'), ('\u2019', "'")]:
    text = text.replace(a, b)
filename = 'asdc-tegev2.csv'
print('Writing {}'.format(filename))
Path(filename).write_text(text)

# Read CSV table
print('Reading {}'.format(filename))
t1 = ascii.read(filename, format='csv',
    quotechar='"',
    fast_reader=False,
    fill_values=[('-', '')],
)
# t1.info('stats')
# t1.show_in_browser(jsviewer=True)

# Make new table and fill with good column names,
# units and values converted to numbers where appropriate
t2 = Table()
t2['id'] = t1['id']
t2['Source_Name'] = t1['TEV NAME']
t2['Other_Names'] = t1['OTHER NAMES']
t2['TYPE'] = t1['TYPE']

t2['RA'] = Angle(t1['RA (J2000)'], unit='hourangle').deg
t2['RA'].unit = 'deg'
t2['DEC'] = Angle(t1['Dec (J2000)'], unit='deg').deg
t2['DEC'].unit = 'deg'
t2['GLON'] = t1['LII(degrees)']
t2['GLON'].unit = 'deg'
t2['GLAT'] = t1['BII(degrees)']
t2['GLAT'].unit = 'deg'

# TODO: continue cleaning up those columns and adding them:
# 'ErrRaStat[s]', 'ErrRaSys[s]', 'ErrDecStat[arcsec]', 'ErrDecSys[arcsec]', 'EXTENDED', 'SEMIMAJOR[deg]', 'ERRMAJOR[deg]', 'SEMIMINOR[deg]', 'ERRMINOR[deg]', 'ROTATION ANGLE[deg]', 'DIFF. FLUX NORMALIZATION[x TeV^-1 cm^-2 s^-1]', 'DIFF. FLUX NORMALIZATION ERRSTAT[x TeV^-1 cm^-2 s^-1]', 'DIFF. FLUX NORMALIZATION ERRSYS[x TeV^-1 cm^-2 s^-1]', 'SPECTRAL SLOPE', 'ERRSLOPESTAT', 'ERRSLOPESYS', 'INTEGRAL FLUX', 'ErrFluxStat[x 10^-12 cm^-2 s^-1]', 'ErrFluxSys[x 10^-12 cm^-2 s^-1]', 'OTHER SPECTRAL COMPONENTS', 'Flux in CU[%]', 'THR ENERGY [GeV]', 'MIN ZENITH[deg]', 'MAX ZENITH[deg]', 'MEAN ZENITH[deg]', 'DISTANCE[kPc]', 'Distance', 'Discoverer', 'Observatory', 'START TIME[MJD]', 'END OBSERVATION[MJD]', 'EXPOSURE TIME[ksec]', 'POS. ERROR CIRCLE[deg]', 'Diff. Flux. Norm. Energy[TeV]', 'REFERENCE', 'COMMENTS'

# t2.info()
# t2.info('stats')
# t2.show_in_browser(jsviewer=True)
# import IPython; IPython.embed()

filename = 'asdc-tegev.fits.gz'
print('Writing {}'.format(filename))
t2.write(filename, overwrite=True)
