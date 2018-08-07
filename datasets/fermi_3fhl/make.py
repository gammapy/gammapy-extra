"""Make 3FHL example files."""
from astropy.coordinates import SkyCoord, Angle
from gammapy.maps import Map

m = Map.read('gll_iem_v06.fits')
m2 = m.make_cutout(
    SkyCoord(0, 0, unit='deg', frame='galactic'),
    (Angle('6 deg'), Angle('11 deg')),
)[0]
print(m2.geom)
m2.write('gll_iem_v06_cutout.fits', overwrite=True)
