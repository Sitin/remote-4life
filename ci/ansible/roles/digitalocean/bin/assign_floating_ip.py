#!/usr/bin/env python

import sys
import digitalocean


api_token = sys.argv[1]
ip_address = sys.argv[2]
droplet_id = sys.argv[3]

manager = digitalocean.Manager(token=api_token)

print(manager.get_floating_ip(ip=ip_address))
