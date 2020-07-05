#!/usr/bin/env python

import os
import sys
from ssm_parameter_store import EC2ParameterStore
import yaml

store = EC2ParameterStore()

ssm_path = os.environ.get('AWS_SSM_PATH', '/r4l')
if not ssm_path.endswith('/'):
    ssm_path += '/'

parameters = store.get_parameters_by_path(ssm_path, recursive=False, strip_path=True)

config_file = sys.argv[1]
print(f'Loading config into "{config_file}"...')
with open(config_file, 'w+') as outfile:
    yaml.dump(parameters, outfile, default_flow_style=False)
