"""Make hess-dl3-dr1 dataset for Gammapy.

You have to download the data and background models
and set the `PATH` variables at the top, then run `make.py`
"""
import logging
import shutil
from pathlib import Path
from astropy.io import fits
from astropy.table import Table

log = logging.getLogger(__name__)

PATH_DATA = Path("/Users/deil/work/data/hess/hess-dl3-dr1")
PATH_BKG = Path("/Users/deil/work/code/hess_ost_paper_material/background_model")
PATH_OUT = Path(".")

DEBUG_RUN = False


def get_obs_ids():
    obs_id = Table.read(PATH_DATA / "obs-index.fits.gz")["OBS_ID"]
    return obs_id[:3] if DEBUG_RUN else obs_id


def make_obs_index():
    """Copy existing OBS index file, no changes needed."""
    src = PATH_DATA / "obs-index.fits.gz"
    dst = PATH_OUT / "obs-index.fits.gz"
    log.info(f"Writing {dst}")
    shutil.copyfile(src, dst)


def make_hdu_index():
    """Copy existing HDU index file, add background HDU rows."""
    log.info("Make hdu-index.fits.gz")
    path = PATH_DATA / "hdu-index.fits.gz"
    table = Table.read(path)

    for obs_id in get_obs_ids():
        filename = f"hess_dl3_dr1_obs_id_{obs_id:06d}.fits.gz"
        size = fits.open(PATH_OUT / f"data/{filename}")["bkg"].filebytes()
        table.add_row([obs_id, "bkg", "bkg_3d", "data", filename, "bkg", size])

    table.sort(["OBS_ID", "HDU_TYPE"])

    path = PATH_OUT / "hdu-index.fits.gz"
    log.info(f"Writing {path}")
    table.write(path, overwrite=True)


def make_background_hdu(obs_id):
    """Make background HDU, basically copy, but change to float32."""
    path = PATH_BKG / f"data/hess_bkg_3d_{obs_id:06d}.fits.gz"
    table = Table.read(path)

    for colname in table.colnames:
        table[colname] = table[colname].astype("float32")

    hdu = fits.BinTableHDU(table)
    hdu.name = "bkg"

    return hdu


def make_data_file(obs_id):
    """Copy existing data file, add background HDU."""
    log.info(f"Make data file for OBS_ID = {obs_id}")
    path = PATH_DATA / f"data/hess_dl3_dr1_obs_id_{obs_id:06d}.fits.gz"
    hdu_list = fits.open(path)

    hdu_bkg = make_background_hdu(obs_id)
    hdu_list.append(hdu_bkg)

    path = PATH_OUT / f"data/hess_dl3_dr1_obs_id_{obs_id:06d}.fits.gz"
    log.info(f"Writing {path}")
    hdu_list.writeto(path, overwrite=True)


def main():
    """Combine data release and background models, update index tables."""
    logging.basicConfig(level=logging.INFO)

    (PATH_OUT / "data").mkdir(exist_ok=True)
    for obs_id in get_obs_ids():
        make_data_file(obs_id)

    make_obs_index()
    make_hdu_index()


if __name__ == "__main__":
    main()
