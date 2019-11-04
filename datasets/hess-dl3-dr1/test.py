"""Test hess-dl3-dr1 dataset for Gammapy.

pytest test.py
"""
import pytest
from gammapy.data import DataStore


@pytest.fixture(scope="session")
def data_store():
    return DataStore.from_dir(".")


def test_checksums():
    assert 1 == 1


def test_index_tables(data_store):

    assert len(data_store.obs_table) == 105
    assert len(data_store.obs_table.columns) == 31

    assert len(data_store.hdu_table) == 105 * 6
    colnames = [
        "OBS_ID",
        "HDU_TYPE",
        "HDU_CLASS",
        "FILE_DIR",
        "FILE_NAME",
        "HDU_NAME",
        "SIZE",
    ]
    assert data_store.hdu_table.colnames == colnames
    assert data_store.hdu_table["SIZE"].sum() == 114_321_600


def test_data_files(data_store):
    for obs_id in data_store.obs_table["OBS_ID"][::30]:
        obs = data_store.obs(obs_id)
        obs.events
        obs.gti
        obs.aeff
        obs.psf
        obs.edisp
        obs.bkg
