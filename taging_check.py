from tracemalloc import Snapshot
import boto3
import json
import sys
from datetime import datetime, timezone
import argparse
import botocore



DR_tagged_list={}
DR_not_tagged_list={}
not_tagged_list={}

##################################################################################
### If it does not have the DR tag
def no_DR_tag(snapshotid, tags, region):
    
    not_tagged_list[region].update({"Snap":snapshotid})

    return



##################################################################################
### If it has the DR tag
def DR_tag(snapshotid, region):

    
    DR_tagged_list[region].update({"Snap":snapshotid})

    return




##################################################################################
## what to do if it has no tag 
def no_tag(snapshotid, region):
    
    not_tagged_list[region].update({"Snap":snapshotid})




##################################################################################
### Here we check for the tagging information if it has tags or not or a specific tag 
def snapshot_tag_info(snapshotid, region):
    ec2 = boto3.resource('ec2', region)
    snapshot = ec2.Snapshot(snapshotid)
    

    if snapshot.tags is not None:
      
        if next(filter(lambda obj: obj.get('Key') == 'DR-Tier', snapshot.tags), None):
 
            DR_tag(snapshotid, region)
        else:

           
            no_DR_tag(snapshotid, snapshot.tags , region)

    else :
        no_tag(snapshotid, region)

    return



##################################################################################
### This funsction lists all snapshots older than 29 days 
def list_old_snapshots(region):

    print(DR_not_tagged_list)
    print(DR_not_tagged_list)
    print(not_tagged_list)

    ec2 = boto3.client('ec2', region)
    snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])

    for snapshot in snapshot_response['Snapshots']:

        days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days


        if days_old >= 29:

            snapshot_tag_info(snapshot['SnapshotId'], region)

            continue
        else :
            continue

    return


##################################################################################
### define whihch region to use or loop all the regions 
def region(region):

    if region == "all":
        e = boto3.client('ec2')
        regions_list = e.describe_regions()
        regions = regions_list["Regions"]
        for region in regions:
            DR_tagged_list[region['RegionName']]={}
            DR_not_tagged_list[region['RegionName']]={}
            not_tagged_list[region['RegionName']]={}

            list_old_snapshots(region['RegionName'])
    else:

        DR_tagged_list[region]={}
        DR_not_tagged_list[region]={}
        not_tagged_list[region]={}    
            
        list_old_snapshots(region)

##################################################################################
### initiates the function calls 
if __name__ == '__main__':

    globals()[sys.argv[1]](sys.argv[2])
    

    print("snapshots with DR tag: ")
    print(DR_tagged_list)
    print("#")
    print("#")
    print("#")
    print("snapshots with no DR tag: ")
    print(DR_not_tagged_list)
    print("#")
    print("#")
    print("#")
    print("snapshots with no tag: ")
    print(not_tagged_list)


