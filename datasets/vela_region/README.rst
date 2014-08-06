Fermi-LAT small data sets
=========================

We add a few small Fermi-LAT data files for the Vela region that we use for unit tests, examples and tutorials.

Parameters
----------

* 5 years of observation time (2008-08-05 to 2013-08-05)
* Event class and IRF: P7REP_CLEAN_V15
* Max zenith angle cut: 105 deg
* 10 GeV < Energy < 500 GeV

Files
-----

* ``counts_vela.fits`` -- Vela region counts cube 
* ``exposure_vela.fits`` --	Vela region exposure cube
* ``background_vela.fits`` -- Vela region estimated background counts cube
* ``psf_vela.fits`` -- Fermi PSF for the Vela region
* ``gll_iem_v05_rev1_cutout.fit`` -- Cutout of the v05 rev.1 Fermi Diffuse Background model with search radius 30 degrees for the Vela Region


Details
-------

Commands:

The above files were produced with the Fermi Science Tools. The commands used are included in the respective executable scripts listed below.

* ``counts_commands.sh`` for ``counts_vela.fits``
* ``exposure_commands.sh`` for ``exposure_vela.fits``
* ``background_commands.sh`` for ``background_vela.fits``
* ``psf_commands.sh`` for ``psf_vela.fits``

See ``model.xml`` for the background model used to produce ``background_vela.fits``. This uses the Fermi Diffuse Background model, and the FSSC published extended source model VelaX.fits (also included here).

For create the file ``gll_iem_v05_rev1_cutout.fit``, the following commands were run:

	$ wget http://fermi.gsfc.nasa.gov/ssc/data/analysis/software/aux/gll_iem_v05_rev1.fit
	$ ftcopy 'gll_iem_v05_rev1.fit[612:772, 696:856]' gll_iem_v05_rev1_cutout.fits
	$ fchecksum gll_iem_v05_rev1_cutout.fit update+ datasum+
