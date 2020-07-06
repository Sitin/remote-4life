#!/usr/bin/env python

import sys
import digitalocean


api_token = sys.argv[1]
ip_address = sys.argv[2]
droplet_id = int(sys.argv[3])

manager = digitalocean.Manager(token=api_token)

floating_ip = manager.get_floating_ip(ip=ip_address)

if floating_ip.droplet is None:
    print(f'Assigning free IP {floating_ip} to droplet {droplet_id}...')
    floating_ip.assign(droplet_id=droplet_id)
else:
    if floating_ip.droplet['id'] != droplet_id:
        print(f'Unassigning IP {floating_ip} from droplet {floating_ip.droplet["id"]}...')
        floating_ip.unassign()
        print(f'Reassigning released IP {floating_ip} to droplet {droplet_id}...')
        floating_ip.assign(droplet_id=droplet_id)
    else:
        print(f'Floating IP {floating_ip} is already assigned to droplet {droplet_id}.')
