import numpy as np
from astropy.table import Table
from gammapy.spectrum import FluxPoints
from pathlib import Path


# ### HAWC flux points for Crab Nebula 
# The HAWC flux point are taken from https://arxiv.org/pdf/1905.12518.pdf
# assigned to a `FluxPoints` object, then written to FITS.

e_ref = np.array([1.04, 1.83, 3.24, 5.84, 10.66, 19.6, 31.6, 66.8, 118])
e2dnde = np.array(
    [
        3.63e-11,
        2.67e-11,
        1.92e-11,
        1.24e-11,
        8.15e-12,
        5.23e-12,
        3.26e-12,
        1.23e-12,
        8.37e-13,
    ]
)
e2dnde_err = np.array(
    [
        0.08e-11,
        0.05e-11,
        0.04e-11,
        0.03e-11,
        0.31e-12,
        0.29e-12,
        0.28e-12,
        0.24e-12,
        2.91e-13,
    ]
)
dnde = e2dnde / e_ref ** 2.0
dnde_err = dnde * e2dnde_err / e2dnde

table = Table()
table.meta["SED_TYPE"] = "dnde"
table["dnde"] = dnde
table["dnde"].unit = "cm-2 s-1 TeV-1"
table["dnde_err"] = dnde_err
table["dnde_err"].unit = "cm-2 s-1 TeV-1"
table["e_ref"] = e_ref
table["e_ref"].unit = "TeV"

flux_points_hawc = FluxPoints(table)

filename = Path("$GAMMAPY_EXTRA/datasets/hawc_crab/HAWC19_flux_points.fits")
flux_points_hawc.write(filename, overwrite=True)

