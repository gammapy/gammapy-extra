Fermi-LAT 2FHL dataset
======================

This folder contains the dataset files, that were used for the `Fermi 2FHL catalog <https://arxiv.org/abs/1508.04449/>`_.
The data files were recreated with the script `fermi_2fhl_data.sh`, which is a bash script that calls into the Fermi
science tools. For a basic guide trough data preparation see `here <http://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/LAT_weekly_allsky.html/>`_.

To run the script two environment variable have to be set:

.. code:: bash

    PHOTON_FILES=path_to_weekly_fermi_photon_files
    SPACECRAFT=path_to_merged_fermi_spacecraft_files

Where `PHOTON_FILES` points to the folder, where the weekly photon files are contained and `SPACECRAFT`
points to the merged spacecraft file.


Source catalog
--------------

The Fermi-LAT 2FHL catalog is in `catalog/gll_psch_v08.fit.gz` (downloaded from FSSC)

::

    Name               Type       Dimensions
    ----               ----       ----------
    HDU 1   Count Map          Image      Int4(3600x1800)
    HDU 2   2FHL Source Catalog BinTable    39 cols x 360 rows
    HDU 3   Extended Sources   BinTable    10 cols x 25 rows
    HDU 4   ROIs               BinTable     6 cols x 154 rows


Event list
----------

The event list corresponding to 2FHL (obtained from Marco Ajello with permission
to share publicly on November 12, 2015) is in `events/fermi_2fhl_events_reference.fits.gz`.

::

    Name               Type       Dimensions
    ----               ----       ----------
    HDU 1   Primary Array      Null Array
    HDU 2   EVENTS             BinTable    23 cols x 60978 rows
    HDU 3   GTI                BinTable     2 cols x 36589 rows


The second, recreated event list is contained in `events/fermi_2fhl_events.fits.gz`. Please
note that the events are not exactly the same. Please check the notebook `fermi_2fhl_events_check.ipynb`
for details.

Counts
------

A counts cube is contained in `fermi_2fhl_counts.fits.gz`. In general it is recommended to recreate it from the
event list, with the WCS specifications needed for the application.

Exposure
--------

The exposure cube is contained in `fermi_2fhl_exposure.fits.gz`

::

    Name                       Type         Dimensions
    ----                       ----         ----------
    HDU 1   PRIMARY            Image        Real4(9400x500x6)
    HDU 2   ENERGIES           BinTable     1 cols x 6 rows
    HDU 3   GTI                BinTable     2 cols x 36164 rows


PSF
---

The PSF computed for the Galactic Center is contained in `fermi_2fhl_psf_gc.fits.gz`.

::

    Name                       Type         Dimensions
    ----                       ----         ----------
    HDU 1   PRIMARY            Null Array
    HDU 2   PSF                BinTable     3 cols x 5 rows
    HDU 3   THETA              BinTable     1 cols x 300 rows


