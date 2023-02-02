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
def no_DR_tag(snapshotid, tags, region):
    
    print(tags)

    try :
        instance_info = next(filter(lambda obj: obj.get('Key') == 'instance-id', tags), None)
        instance = instance_info["Value"]
    except:
        instance = "No Instance ID Tag"
    try :
        name_info=next(filter(lambda obj: obj.get('Key') == 'Name', tags), None)
        name=name_info["Value"]
    except:
        name ="No Name Tag"

    DR_not_tagged_list[region].update({snapshotid:{ "Instance":instance, "Name":name}})

    return DR_not_tagged_list



##################################################################################
### If it has the DR tag
def DR_tag(snapshotid,tags, region):

    try :
        instance_info = next(filter(lambda obj: obj.get('Key') == 'instance-id', tags), None)
        instance = instance_info["Value"]
    except:
        instance = "No Instance ID Tag"
    try :
        name_info=next(filter(lambda obj: obj.get('Key') == 'Name', tags), None)
        name=name_info["Value"]
    except:
        name ="No Name Tag"
    DR_tagged_list[region].update({snapshotid:"DR-Tier", "Instance":instance, "Name":name})

    return DR_tagged_list




##################################################################################
## what to do if it has no tag 
def no_tag(snapshotid, region):

    not_tagged_list[region].update({snapshotid:"NO TAGS"})
    
    return not_tagged_list




##################################################################################
### Here we check for the tagging information if it has tags or not or a specific tag 
def snapshot_tag_info(snapshotid, region):
    ec2 = boto3.resource('ec2', region)
    snapshot = ec2.Snapshot(snapshotid)
    

    if snapshot.tags is not None:
      
        if next(filter(lambda obj: obj.get('Key') == 'DR-Tier', snapshot.tags), None):


            DR_tag(snapshotid, snapshot.tags, region)
            #print(region,snapshotid, "DR-tier Tagged")
            
        else:

            no_DR_tag(snapshotid, snapshot.tags , region)
            #print(region,snapshotid, "not DR-tier tag")

    else :
        no_tag(snapshotid, region)
        #print(region, snapshotid, "No Tags" )


    return



##################################################################################
### This funsction lists all snapshots older than 29 days 
def list_old_snapshots(region):


    ec2 = boto3.client('ec2', region)
    snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])

    snapshot_count=len(snapshot_response['Snapshots'])
    count = 0

    for snapshot in snapshot_response['Snapshots']:

        count +=1

        print("Working on ", count, "of ", snapshot_count, "in ", region)

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
        region_count=len(regions)
        count=0 
        for region in regions:
            count +=1 
            print("Working on region", count, "of ", region_count)
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
    

    with open("DR_tagged_list.json","w") as file:
        json.dump(DR_tagged_list,file, indent=4, default=str)

    with open("DR_not_tagged_list.json","w") as file:
        json.dump(DR_not_tagged_list,file, indent=4, default=str)

    with open("not_tagged_list.json","w") as file:
        json.dump(not_tagged_list,file, indent=4, default=str)