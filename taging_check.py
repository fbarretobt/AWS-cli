from tracemalloc import Snapshot
import boto3
import json
import sys
from datetime import datetime, timezone
import argparse
import botocore



##################################################################################
def ec2_tagname(instance_id):

    ec2 = boto3.resource("ec2")

    ec2instance = ec2.Instance(instance_id)

    instancename = ''

    for tags in ec2instance.tags:

        if tags["Key"] == 'Name':
            
            instancename = tags["Value"]

    #return instancename
    return instancename


##################################################################################
def no_DR_tag(snapshotid, tags):

    print("Snapshot ", snapshotid, "Has no DR tag")

    for tag_values in tags.values():

        print("**********   ",tag_values)   

    return



##################################################################################
def DR_tag(snapshotid):

    print("Snapshot ",snapshotid, "Has DR-Tier Tag")

    return

##################################################################################
def no_tag(snapshotid):

    print("Snapshot ", snapshotid, "Has no Tags")



##################################################################################
def snapshot_tag_info(snapshotid):
    ec2 = boto3.resource('ec2')
    snapshot = ec2.Snapshot(snapshotid)

    if snapshot.tags is not None:
        for tags in snapshot.tags:
            
            if tags["Key"] == 'DR-Tier':
                DR_tag(snapshotid)
                continue
            else : 
                no_DR_tag(snapshot, tags)
                continue
    else :
        no_tag(snapshotid)

    return

##################################################################################
def list_old_snapshots():

    ec2 = boto3.client('ec2')
    snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])

    for snapshot in snapshot_response['Snapshots']:

        days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days


        if days_old >= 29:
            
            print(snapshot['SnapshotId'], "is ", days_old, "days old")
            snapshot_tag_info(snapshot['SnapshotId'])
            continue
        else :
            continue
    return
    

##################################################################################
if __name__ == '__main__':
#    globals()[sys.argv[1]](sys.argv[2])

    list_old_snapshots()