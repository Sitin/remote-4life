#!/usr/bin/env python

import os
import sys
from ssm_parameter_store import EC2ParameterStore

store = EC2ParameterStore()

ssh_dir = sys.argv[1]

ssm_path = os.environ.get('AWS_SSM_PATH', '/r4l')
if not ssm_path.endswith('/'):
    ssm_path += '/'
ssm_path += 'ssh/'

ssh_files = store.get_parameters_by_path(ssm_path, recursive=False, strip_path=True)

for filename in ssh_files:
    file_path = os.path.join(ssh_dir, filename)
    print(f'Writing to "{file_path}"...')
    with open(file_path, 'w+') as f:
        f.write(ssh_files[filename])
