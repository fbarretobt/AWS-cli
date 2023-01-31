from tracemalloc import Snapshot
import boto3
import json
import sys
from pprint import pprint
from datetime import datetime, timezone
import botocore




ec2 = boto3.client('ec2')
snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])

not_found_volumes=[]

for snapshot in snapshot_response['Snapshots']:

    days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days


    if days_old >= 29:
        print ("+++++++++++++++++++++++++++")
        print ("+")
        print(snapshot['SnapshotId'])
        volumeId=snapshot['VolumeId']
        #print(volumeId)
        print("Snapshot is ", days_old, "days old")

        try:
            volume_response = ec2.describe_volumes(VolumeIds=[snapshot['VolumeId']])
            volume = volume_response['Volumes'][0]

            for attachment in volume['Attachments']:

                print("Instance ID :" + attachment['InstanceId'])
                print ("+")
                print ("+")
                print ("+++++++++++++++++++++++++++")


        except botocore.exceptions.ClientError as error:

            if error.response['Error']['Code'] == 'InvalidVolume.NotFound':

                print("Volume not found ", snapshot['VolumeId'] )
                not_found_volumes.append("snapshot['VolumeId']")

            else: # Unknown exception

                print(error.response)
    
    else :

        continue

print("List of snaps whith volumes not found :", not_found_volumes)