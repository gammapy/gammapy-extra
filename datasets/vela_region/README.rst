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
* ``point_vela.fits`` -- Vela region estimated backgrounnd cube with Vela Pulsar as point source
* ``psf_vela.fits`` -- Fermi PSF for the Vela region
* ``gll_iem_v05_rev1_cutout.fits`` -- Cutout of the v05 rev.1 Fermi Diffuse Background model with search radius 30 degrees for the Vela Region


Details
-------

Commands:

The above files were produced with the Fermi Science Tools. The commands used to create all files are included in sequence in the executable script ``make.sh``. All commands take a few minutes to run, **with the exception of gtltcube, which will run for a few hours.**

This reflects the preparation steps outlined in option 2 of the FSSC page for excluding atmospheric background events: http://fermi.gsfc.nasa.gov/ssc/data/analysis/documentation/Cicerone/Cicerone_Likelihood/Exposure.html

See ``background_model.xml`` for the background model used to produce ``background_vela.fits``. This uses the Fermi Diffuse Background model, ``gll_iem_v05_rev1_cutout.fits`` (also included here). Additionally ``total_model.xml`` additionally includes a point source model for the Vela Pulsar with the Fermi Diffuse Background to produce ``total_model.fits``.

For create the file ``gll_iem_v05_rev1_cutout.fit``, the following commands were run:

.. code-block:: bash
	$ wget http://fermi.gsfc.nasa.gov/ssc/data/analysis/software/aux/gll_iem_v05_rev1.fit
	$ ftcopy 'gll_iem_v05_rev1.fit[588:748, 617:777]' gll_iem_v05_rev1_cutout.fits
	$ fchecksum gll_iem_v05_rev1_cutout.fit update+ datasum+

