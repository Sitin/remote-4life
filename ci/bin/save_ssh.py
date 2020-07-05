#!/usr/bin/env python

import os
import sys
import boto3

client = boto3.client('ssm')

ssh_dir = sys.argv[1]

ssm_path = os.environ.get('AWS_SSM_PATH', '/r4l')
if not ssm_path.endswith('/'):
    ssm_path += '/'
ssm_path += 'ssh/'

files = [f for f in os.listdir(ssh_dir) if f != '.gitignore']

for filename in files:
    file_path = os.path.join(ssh_dir, filename)
    param_name = ssm_path + filename
    print(f'Saving "{file_path}" to "{param_name}"...')
    with open(file_path) as f:
        client.put_parameter(Name=param_name, Value=f.read(), Type='SecureString', Overwrite=True)
