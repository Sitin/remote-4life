#!/usr/bin/env python

import sys
import digitalocean


api_token = sys.argv[1]
region = sys.argv[2]
volume_name = sys.argv[3]
volume_size = int(sys.argv[4])
filesystem = sys.argv[5]

manager = digitalocean.Manager(token=api_token)

volumes = manager.get_all_volumes(region=region)
volumes = [v for v in volumes if v.name == volume_name]

if len(volumes) == 1:
    volume = volumes[0]
    assert volume.filesystem_type == filesystem, f'Volume "{volume_name}" filesystem "{volume.filesystem_type}" does not match provided "{filesystem}"'
    assert volume.size_gigabytes == volume_size, f'Volume "{volume_name}" size {volume.size_gigabytes} does not match provided {volume_size}'
    print(f'Volume "{volume_name}" already exists in region "{region}", skipping.')
elif len(volumes) > 1:
    raise RuntimeError(f'Found multiple volumes of name "{volume_name}"" in region "{region}".')
else:
    snapshots = manager.get_all_snapshots()
    snapshots = [s for s in snapshots if s.name.startswith(volume_name) and region in s.regions and s.resource_type == 'volume']
    snapshots = sorted(snapshots, key=lambda x: x.created_at, reverse=True)
    if len(snapshots) > 0:
        snapshot = snapshots[0]
        snapshot_id = snapshot.id
        print(f'Found snapshot "{snapshot.name}" for "{volume_name}" created at {snapshot.created_at}.')
    else:
        snapshot_id = None

    volume = digitalocean.Volume(
        name=volume_name,
        filesystem_type=filesystem,
        filesystem_label=volume_name,
        size_gigabytes=volume_size,
        region=region,
        token=api_token,
        snapshot_id=snapshot_id,
    )
    volume.create()
    print(f'Volume "{volume_name}" has been created in region "{region}" with ID={volume.id}.')


