Fermi-LAT small data sets
=========================

We add simulated galactic images including source and diffuse contributions. Additionally, the Fermi-LAT exposure for the galactic plane is included.

Parameters
----------

* Energy range: 10 to 500 GeV
* Galactic latitude range: -5 < b < 5 degrees
* Galactic longitude range: -100 < l < 100 degrees


* Source contributions from 1FHL catalog and 2 simulated galactic populations
* Diffuse contribution from integral flux from Fermi Diffuse model gll_iem_v05_rev1.fit between 10 and 500 GeV

Source Population Parameters
----------------------------

* ``FD_GAL1.fits`` -- Simulated catalog with rho_sun = 3 kpc^-3, L_min = 10 ^ 34 ph s^-1, L_max = 10 ^ 37 ph s^-1
* ``FD_GAL2.fits`` --	Simulated catalog with rho_sun = 10 kpc^-3, L_min = 4 * 10 ^ 33 ph s^-1, L_max = 4 * 10 ^ 36 ph s^-1
* ``FD_FHL.fits`` -- 1FHL Catalog of Fermi Sources above 10 GeV (see: http://fermi.gsfc.nasa.gov/ssc/data/access/lat/1FHL/)

In the simulated populations, a power law luminosity is assumed of index -1.5 between the stated L_min and L_max luminosities. For further details see this Proceeding: http://pos.sissa.it/cgi-bin/reader/conf.cgi?confid=218
(Not yet available)
