"""
This script generates reference files for IRF tests
as well as a YAML dict where to find these files
"""

import yaml
from gammapy.utils.testing import data_manager
from gammapy.utils.scripts import make_path

test_args = list()
test_args.append(
    dict(chain='HAP-HD',
         store='hess-crab4-hd-hap-prod2',
         obs=23523,
         aeff2D_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/hap_hd_aeff2D_reference.txt',
         edisp2D_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/hap_hd_edisp2D_reference.txt',
         psf3gauss_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/hap_hd_psf3gauss_reference.txt')
)
test_args.append(
    dict(chain='ParisAnalysis',
         store='hess-crab4-pa',
         obs=23523,
         aeff2D_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/pa_aeff2D_reference.txt',
         edisp2D_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/pa_edisp2D_reference.txt',
         psf3gauss_reference_file='$GAMMAPY_EXTRA/test_datasets/reference/pa_psf3gauss_reference.txt')
)

with open('reference_info.yaml', 'w') as outfile:
    outfile.write(yaml.dump(test_args, default_flow_style=False))

dm = data_manager()
for chain in test_args:
    store = dm[chain['store']]
    aeff = store.load(chain['obs'], filetype='aeff')
    filename = make_path(chain['aeff2D_reference_file'])
    f = open(str(filename), 'w')
    f.write(aeff.info())

    edisp = store.load(chain['obs'], filetype='edisp')
    filename = make_path(chain['edisp2D_reference_file'])
    f = open(str(filename), 'w')
    f.write(edisp.info())

    psf3g = store.load(chain['obs'], filetype='psf')
    filename = make_path(chain['psf3gauss_reference_file'])
    f = open(str(filename), 'w')
    f.write(psf3g.info())
