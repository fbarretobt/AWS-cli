from tracemalloc import Snapshot
import boto3
import json
import sys
from pprint import pprint
from datetime import datetime, timezone
import argparse
import botocore




def print_ec2_tagname(instance_id, RegionName):
    ec2 = boto3.resource("ec2")
    ec2instance = ec2.Instance(instance_id, region_name=RegionName)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
    #return instancename
    return instancename



e = boto3.client('ec2')
regions_list = e.describe_regions()

regions = regions_list["Regions"]

for region in regions: 
    ec2 = boto3.client('ec2', region['RegionName'])
    snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])

    not_found_volumes={}
    instances_attached={}

    for snapshot in snapshot_response['Snapshots']:

        days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days


        if days_old >= 29:

            try:

                volume_response = ec2.describe_volumes(VolumeIds=[snapshot['VolumeId']])
                volume = volume_response['Volumes'][0]

                for attachment in volume['Attachments']:


                    instance_name=print_ec2_tagname(attachment['InstanceId'], region['RegionName'])
                    instances_attached.update({snapshot['SnapshotId']:instance_name})


            except botocore.exceptions.ClientError as error:

                if error.response['Error']['Code'] == 'InvalidVolume.NotFound':


                    not_found_volumes.update({snapshot['SnapshotId']:snapshot['VolumeId']})

                else: # Unknown exception

                    print(error.response)
        
        else :

            continue


    Print("++++++++++++++++++++", region['RegionName'], "+++++++++++++++++++++++++++++++++")

    sorted_not_found_by_volume=sorted(not_found_volumes.items(), key=lambda x:x[1])
    convert_not_fount=dict(sorted_not_found_by_volume)
    print("||  Snaps with non running instances: ")
    print("||")
    print("||")
    for key, value in convert_not_fount.items():

        print("Snapshot:", key, ' = ',"Volume:", value)

    print("||")
    print("||")
    print ("Total of ", len(convert_not_fount), " Snapshots with non running instances in", region['RegionName'])
    print("||")
    print("||")
    print("||")
    print("===============================================================================")
    print("||  Snaps with  running instances:")  
    print("||")
    print("||")
    sorted_running=sorted(instances_attached.items(), key=lambda x:x[1])
    convert_running=dict(sorted_running)
    for key, value in convert_running.items():

        print(key, ' = ',"Instance:", value)

    print ("Total of ", len(convert_running), " Snapshots with  running instances in ", region['RegionName'])