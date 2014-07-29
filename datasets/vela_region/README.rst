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


Details
-------

Commands:

The above files were produced with the Fermi Science Tools. The commands used are included in the respective executable scripts listed below.

* ``counts_commands.sh`` for ``counts_vela.fits``
* ``exposure_commands.sh`` for ``exposure_vela.fits``
* ``background_commands.sh`` for ``background_vela.fits``

See ``model.xml`` for the background model used to produce ``background_vela.fits``. This uses the Fermi Diffuse Background model. 
   