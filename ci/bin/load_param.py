#!/usr/bin/env python

import os
import sys
from ssm_parameter_store import EC2ParameterStore

store = EC2ParameterStore()

ssm_path = os.environ.get('AWS_SSM_PATH', '/r4l')
if not ssm_path.endswith('/'):
    ssm_path += '/'

param_name = sys.argv[1]
param_path = f'{ssm_path}{param_name}'
parameter = store.get_parameter(param_path, decrypt=True)

print(parameter[param_name])
