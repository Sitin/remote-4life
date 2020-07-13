#!/usr/bin/env python

import sys
from datetime import timezone 
import datetime
import time
import digitalocean


TIMEOUT = 10

api_token = sys.argv[1]
region = sys.argv[2]
volume_name = sys.argv[3]

manager = digitalocean.Manager(token=api_token)

volumes = manager.get_all_volumes(region=region)
volumes = [v for v in volumes if v.name == volume_name]

if len(volumes) == 1:
    volume: digitalocean.Volume = volumes[0]
    print(f'Found "{volume_name}" in region "{region}".')
    
    dt = datetime.datetime.now() 
    utc_time = dt.replace(tzinfo = timezone.utc) 
    utc_timestamp = utc_time.timestamp()
    snapshot_id = str(int(utc_timestamp))
    snapshot_name = f'{volume_name}-{snapshot_id}'

    try:
        volume.snapshot(name=snapshot_name)
        time.sleep(TIMEOUT)
        
        snapshots = volume.get_snapshots()
        snapshots = [s for s in snapshots if s.name == snapshot_name]
        if len(snapshots) > 0:
            snapshot = snapshots[0]
        else:
            raise RuntimeError(f'Recently created snapshot "{snapshot_name}" does not exists.')

        print(f'Createad a snapshot "{snapshot.name}" for volume "{volume_name}" in "{region}" region (ID={snapshot.id}).')
    except digitalocean.DataReadError as err:
        if 'failed to create snapshot: this operation is rate-limited' in str(err):
            print(f'You hane resently created a snapshot for "{volume_name}" in "{region}" region. Skipping.')
        else:
            raise err
elif len(volumes) > 1:
    raise RuntimeError(f'Found multiple volumes of name "{volume_name}"" in region "{region}".')
else:
    print(f'Volume "{volume_name}" does not exist in region {region}, skipping.')


