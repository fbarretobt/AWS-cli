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


def print_ec2_tagname(instance_id, region):
    ec2 = boto3.resource("ec2", region)
    ec2instance = ec2.Instance(instance_id)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]

    return instancename



##################################################################################
### If it does not have the DR tag
def no_DR_tag(snapshotid, tags, region, instance_name):
    
    DR_not_tagged_list[region].update({snapshotid:instance_name})

    return DR_not_tagged_list



##################################################################################
### If it has the DR tag
def DR_tag(snapshotid, region, instance_name):

    
    DR_tagged_list[region].update({snapshotid:"DR-Tier"})

    return DR_tagged_list




##################################################################################
## what to do if it has no tag 
def no_tag(snapshotid, region, instance_name):

    not_tagged_list[region].update({snapshotid:"NO TAGS"})
    
    return not_tagged_list




##################################################################################
### Here we check for the tagging information if it has tags or not or a specific tag 
def snapshot_tag_info(snapshotid, region, instance_name):
    ec2 = boto3.resource('ec2', region)
    snapshot = ec2.Snapshot(snapshotid)
    

    if snapshot.tags is not None:
      
        if next(filter(lambda obj: obj.get('Key') == 'DR-Tier', snapshot.tags), None):
 
            DR_tag(snapshotid, region, instance_name)
            print(snapshotid, instance_name)
            
        else:

           
            no_DR_tag(snapshotid, snapshot.tags , region, instance_name)
            print(snapshotid, instance_name)

    else :
        no_tag(snapshotid, region, instance_name)
        print(snapshotid, instance_name)


    return



##################################################################################
### This funsction lists all snapshots older than 29 days 
def list_old_snapshots(region):


    ec2 = boto3.client('ec2', region)
    snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])

    for snapshot in snapshot_response['Snapshots']:

        days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days


        if days_old >= 29:
            try:

                volume_response = ec2.describe_volumes(VolumeIds=[snapshot['VolumeId']])
                volume = volume_response['Volumes'][0]

                for attachment in volume['Attachments']:


                    instance_name=print_ec2_tagname(attachment['InstanceId'], region)
                    print(snapshotid, instance_name)

            except botocore.exceptions.ClientError as error:

                if error.response['Error']['Code'] == 'InvalidVolume.NotFound':

                    continue

                else: # Unknown exception

                    print(error.response)
            
            snapshot_tag_info(snapshot['SnapshotId'], region, instance_name)

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


