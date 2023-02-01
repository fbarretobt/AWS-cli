from tracemalloc import Snapshot
import boto3
import json
import sys
from datetime import datetime, timezone
import argparse
import botocore




def ec2_tagname(instance_id):
    ec2 = boto3.resource("ec2")
    ec2instance = ec2.Instance(instance_id)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
    #return instancename
    return instancename



def snapshot_tag_info(snapshotid):
    ec2 = boto3.resource('ec2')
    snapshot = ec2.Snapshot(snapshotid)

    for tags in snapshot.tags:
        if tags["Key"] == 'DR-Tier':
            print("Snapshot ",snapshot, "Has DR-Tier Tag")
        else : 
            print("Snapshot ", snapshot, "Has no DR tag")
            print(tags)


def list_old_snapshots():

    ec2 = boto3.client('ec2')
    snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])

    for snapshot in snapshot_response['Snapshots']:

        days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days


        if days_old >= 29:
            
            print(snapshot['SnapshotId'], "is ", days_old, "days old")
        else :
            continue
    

list_old_snapshots()