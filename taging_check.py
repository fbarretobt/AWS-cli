from tracemalloc import Snapshot
import boto3
import json
import sys
from datetime import datetime, timezone
import argparse
import botocore



##################################################################################
### get instance name
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
### If it does not have the DR tag
def no_DR_tag(snapshotid, tags):

    for tag_values in tags.values():

        print("**********   ",tag_values)   

    return



##################################################################################
### If it has the DR tag
def DR_tag(snapshotid):

    #print("Snapshot ",snapshotid, "Has DR-Tier Tag")

    return




##################################################################################
## what to do if it has no tag 
def no_tag(snapshotid):

    print("Snapshot ", snapshotid, "Has no Tags")




##################################################################################
### Here we check for the tagging information if it has tags or not or a specific tag 
def snapshot_tag_info(snapshotid):
    ec2 = boto3.resource('ec2')
    snapshot = ec2.Snapshot(snapshotid)

    if snapshot.tags is not None:
      
        if 'DR-Tier' in snapshot.tags.values():
            DR_tag(snapshotid)
            
        else : 
            print("# " , snapshotid, " has no DR-tier Tag")
            no_DR_tag(snapshotid, tags)
            print("#")
            print("#")
            

    else :
        no_tag(snapshotid)

    return



##################################################################################
### This funsction lists all snapshots older than 29 days 
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
### initiates the function calls 
if __name__ == '__main__':
    list_old_snapshots()