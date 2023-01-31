from tracemalloc import Snapshot
import boto3
import json
import sys
from pprint import pprint
from datetime import datetime, timezone
import botocore




ec2 = boto3.client('ec2')
snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])

for snapshot in snapshot_response['Snapshots']:

    days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days


    if days_old >= 29:
        print ("+++++++++++++++++++++++++++")
        print ("+")
        print(snapshot['SnapshotId'])
        volumeId=snapshot['VolumeId']
        #print(volumeId)
        print("Snapshot is ", days_old, "days old")

    
    else :

        continue