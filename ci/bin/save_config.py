#!/usr/bin/env python

import os
import sys
import boto3
import yaml

client = boto3.client('ssm')

SECRET_WORDS = 'secret', 'key', 'password'

ssm_path = os.environ.get('AWS_SSM_PATH', '/r4l')
if not ssm_path.endswith('/'):
    ssm_path += '/'

with open(sys.argv[1]) as f:
    parameters = yaml.load(f.read(), yaml.Loader)

for key in parameters.keys():
    value = parameters[key]
    ssm_type = 'String'
    for w in SECRET_WORDS:
        if w in key.lower():
            ssm_type = 'SecureString'

    print(f'Saving {key} as {ssm_type} ...')
    client.put_parameter(Name=f'{ssm_path}{key}', Value=parameters[key], Type=ssm_type, Overwrite=True)
