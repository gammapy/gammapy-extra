"""Copy some of the 1DC files that we use for tests and tutorials.
"""
from pathlib import Path
import os
import shutil
import numpy as np
from astropy.table import Table

CTADATA = Path(os.environ['CTADATA'])
obs_ids = [110380, 111140, 111159]


def make_obs_index():
    filename = CTADATA / 'index/gps/obs-index.fits.gz'
    table = Table.read(filename)
    mask = np.array([_ in obs_ids for _ in table['OBS_ID']])
    table = table[mask]

    filename = 'index/gps/obs-index.fits.gz'
    print(f'Writing {filename}')
    table.write(filename, overwrite=True)


def make_hdu_index():
    filename = CTADATA / 'index/gps/hdu-index.fits.gz'
    table = Table.read(filename)
    mask = np.array([_ in obs_ids for _ in table['OBS_ID']])
    table = table[mask]

    filename = 'index/gps/hdu-index.fits.gz'
    print(f'Writing {filename}')
    table.write(filename, overwrite=True)


def copy_caldb():
    path = Path('caldb/data/cta/1dc/bcf/South_z20_50h')
    path.mkdir(exist_ok=True, parents=True)
    src = CTADATA / path / 'irf_file.fits'
    dst = path / 'irf_file.fits'
    print(f'cp {src} {dst}')
    shutil.copy(str(src), str(dst))


def copy_data():
    path = Path('data/baseline/gps')
    path.mkdir(exist_ok=True, parents=True)

    for obs_id in obs_ids:
        filename = path / f'gps_baseline_{obs_id:06d}.fits'
        src = CTADATA / filename
        dst = filename
        print(f'cp {src} {dst}')
        shutil.copy(src, dst)


def main():
    Path('index/gps').mkdir(exist_ok=True, parents=True)
    make_obs_index()
    make_hdu_index()

    copy_caldb()
    copy_data()


if __name__ == '__main__':
    main()
