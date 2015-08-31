Simulate event lists for HESS with ctobssim
===========================================

See https://gammapy.readthedocs.org/en/latest/datasets/make_datasets.html


Setup
-----

On @cdeil's computer::

    #export HESSFITS=/Users/deil/work/_Data/hess/HESSFITS/fits_prod02/pa/Model_Deconvoluted_Prod26/Mpp_Std/
    export HESSFITS=/Users/deil/work/_Data/hess/HESSFITS/fits_prod02/pa/
    # export IRF_DIR=$PWD/../../test_datasets/irf/hess/pa/
    export IRF_DIR=/Users/deil/code/gammapy-extra/test_datasets/irf/hess/pa/


Method 1: with input event list
-------------------------------

So far I haven't been able to figure out how to simulate events without providing an **input** event list,
which contains some parameters like ``ra``, ``dec``, ``tmin``, ...
(see http://cta.irap.omp.eu/ctools-devel/reference_manual/ctobssim.html for a list).

But using the real HESS event list as input does work::

    ./make1.py

creates a ``events1_0.fits`` file (and a ``outevents1.xml`` file we don't care about).

This method has serious drawbacks:

- the input event lists aren't public.
- this doesn't work for future observations.
- some info from the input event list (like ALT / AZ) is just copied to the output event list,
  leading to leaked private data and incorrect parameters.


Method 2: without input events list
-----------------------------------

I've asked on the ctools mailing list for help (2015-08-31), but as a workaround I'll try to
write a Python script which **fakes** an input event list with the required info,
and then use that as the input to ctobssim.

Work in progress ... will be ``make2.py``.

These scripts are useful examples:

* https://github.com/ctools/ctools/blob/devel/examples/simulate_events.py
* https://github.com/ctools/ctools/blob/devel/cscripts/obsutils.py

