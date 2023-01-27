import boto3
import json
import sys
from pprint import pprint
from datetime import datetime, timezone

e = boto3.client('ec2')
regions_list = e.describe_regions()

#print(regions)
 
regions = regions_list["Regions"]

for region in regions: 

    regionA = print(region['RegionName'])

    ec2 = boto3.client(ec2, regionA)
    resp = ec2.describe_instances()
    resp_describe_snapshots = ec2.describe_snapshots(OwnerIds=['self'])
    snapshot =  resp_describe_snapshots['Snapshots']
    snapshots = [''];
    for snapshotIdList in resp_describe_snapshots['Snapshots']:
        snapshots.append(snapshotIdList.get('SnapshotId'))
    for id in snapshots:
        print(id)
