#!/usr/bin/env python

import sys
from datetime import timezone 
import datetime
import time
import digitalocean


TIMEOUT = 10
ATTEMTS = 12

api_token = sys.argv[1]
region = sys.argv[2]
droplet_name = sys.argv[3] 
volume_name = sys.argv[4]

manager = digitalocean.Manager(token=api_token)

droplets = manager.get_all_droplets()
droplets = [d for d in droplets if d.name == droplet_name]

if len(droplets) == 1:
    droplet: digitalocean.Droplet = droplets[0]
    if droplet.region['slug'] != region:
        raise RuntimeError(f'Found a "{droplet_name}" droplet in the wrong region "{droplet.region["slug"]}" instead of "{region}".')
    print(f'Found "{droplet_name}" droplet in the desired region "{region}".')

    if droplet.status != 'active':
        print(f'Droplet "{droplet_name}" status: "{droplet.status}", skipping.')
    else:
        droplet.shutdown()
        
        # Await for shut down:
        for i in range(ATTEMTS):
            droplet.load()
            if droplet.status == 'off':
                break
            time.sleep(TIMEOUT)
        
        if droplet.status != 'off':
            raise RuntimeError(f'Droplet "{droplet_name}" is still running with status "{droplet.status}" after {ATTEMTS * TIMEOUT} seconds.')
        
        print(f'Droplet "{droplet_name}" is stopped.')
    
    # Detach all volumes:
    volumes: [digitalocean.Volume] = [manager.get_volume(v_id) for v_id in droplet.volume_ids]
    for v in volumes:
        v.detach(droplet_id=droplet.id, region=region)
        print(f'Volume "{v.name}" detached from the droplet "{droplet_name}".')
    time.sleep(TIMEOUT)
elif len(droplets) > 1:
    raise RuntimeError(f'Found multiple droplets of name "{droplet_name}".')
else:
    print(f'Droplet "{droplet_name}" does not exist, skipping.')