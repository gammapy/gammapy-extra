"""
This script generates reference files for IRF tests
as well as a YAML dict where to find these files
"""

import yaml
import astropy.units as u
import numpy as np
from gammapy.utils.testing import data_manager
from gammapy.utils.scripts import make_path

test_args = list()
test_args.append(
    dict(chain='HAP-HD',
         store='hess-crab4-hd-hap-prod2',
         obs=0,
         aeff2D_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/hap_hd_aeff2D_reference.txt',
         edisp2D_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/hap_hd_edisp2D_reference.txt',
         psf_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/hap_hd_psf_reference.txt',
         obs_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/hap_hd_obs_reference.txt',
         location_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/hap_hd_location_reference.txt')
)
test_args.append(
    dict(chain='ParisAnalysis',
         store='hess-crab4-pa',
         obs=0,
         aeff2D_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/pa_aeff2D_reference.txt',
         edisp2D_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/pa_edisp2D_reference.txt',
         psf_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/pa_psf_reference.txt',
         obs_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/pa_obs_reference.txt',
         location_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/pa_location_reference.txt')
)

test_energy = [0.1, 1, 5, 10] * u.TeV
test_offset = [0.1, 0.2, 0.4] * u.deg


dm = data_manager()
for chain in test_args:
    store = dm[chain['store']]
    chain['obs_id'] = int(store.obs_table['OBS_ID'][chain['obs']])
    obs = store.obs(obs_id = chain['obs_id'])

    filename = make_path(chain['location_reference_file'])
    f = open(str(filename), 'w')
    f.write(str(obs.location(hdu_type='events').path(abs_path=False)))

    filename = make_path(chain['obs_reference_file'])
    f = open(str(filename), 'w')
    f.write(str(obs))


    aeff = obs.aeff
    print(aeff)
    aeff_val = aeff.evaluate(energy=test_energy, offset=test_offset)
    filename = make_path(chain['aeff2D_reference_file'])
    np.savetxt(str(filename), aeff_val)

    edisp = obs.edisp
    filename = make_path(chain['edisp2D_reference_file'])
    f = open(str(filename), 'w')
    f.write(edisp.info())

    psf = obs.psf
    filename = make_path(chain['psf_reference_file'])
    f = open(str(filename), 'w')
    f.write(psf.info())


#Write reference file
with open('reference_info.yaml', 'w') as outfile:
    outfile.write(yaml.dump(test_args, default_flow_style=False))
