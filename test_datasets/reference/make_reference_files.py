"""
This script generates reference files for IRF tests
as well as a YAML dict where to find these files
"""

import yaml
from gammapy.utils.testing import data_manager
from gammapy.utils.scripts import make_path

test_args = dict(test_run = 23523, chains = list())
test_args['chains'].append(
    dict(chain = 'HAP-HD',
         store = 'hess-crab4-hd-hap-prod2',
         aeff2D_reference_file = '$GAMMAPY_EXTRA/test_datasets/reference/hap_hd_aeff2D_reference.txt')
)
test_args['chains'].append(
    dict(chain = 'ParisAnalysis',
         store = 'hess-crab4-pa',
         aeff2D_reference_file = '$GAMMAPY_EXTRA/test_datasets/reference/pa_aeff2D_reference.txt')
)


with open('reference_info.yaml', 'w') as outfile:
    outfile.write(yaml.dump(test_args, default_flow_style=False) )



dm = data_manager()
for chain in test_args['chains']:
    store = dm[chain['store']]
    aeff = store.load(test_args['test_run'], filetype='aeff')
    filename = make_path(chain['aeff2D_reference_file'])
    f = open(str(filename), 'w')
    f.write(aeff.info())
