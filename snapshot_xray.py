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
    print ("+")
    print ("+")
    print ("+")
    print ("++++++++++++++++++++++++++++++++++++++++")
    regionA = print(region['RegionName'])
    print ("++++++++++++++++++++++++++++++++++++++++")
    print ("+")

    ec2 = boto3.client('ec2', regionA)
    snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])

    for snapshot in snapshot_response['Snapshots']:
        print("Snapshot Id : " + snapshot['SnapshotId'])
        print("Volume Id :" +snapshot['VolumeId'])
        print("Volume Size :", snapshot['VolumeSize'])
        print("Creation date :" + snapshot['StartTime'])
        days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days
        print("Snapshot is " + days_old + "days old")

        volume_response = ec2.describe_volumes(VolumeIds=[snapshot['VolumeId']])
        volume = volume_response['Volumes'][0]
        print("Volume Type :" +volume['VolumeType'])
        for attachment in volume['Attachments']:
            print("Instance ID :" + attachment['InstanceId'])