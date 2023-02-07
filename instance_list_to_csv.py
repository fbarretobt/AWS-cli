from tracemalloc import Snapshot
import boto3
import json
import sys
from datetime import datetime, timezone
import argparse
import botocore


snapshot_dict = {}

##################################################################################
### Get all spanshots in the given region 
def get_snapshot(region):
    ec2 = boto3.client('ec2', region)

    snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])
    count = 0
    snapshot_count=len(snapshot_response['Snapshots'])
    for snapshot in snapshot_response['Snapshots']:

        count +=1

        print("Working on ", count, "of ", snapshot_count, "in ", region)
        days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days
        seconds = (datetime.now(timezone.utc) - snapshot['StartTime']).total_seconds()
        hours = int(seconds // 3600)
        minutes = int((seconds//60)%60)

        hours_old = str(hours),str(minutes), "Hours"
        print(hours_old)
        #print(snapshot)
        snapshot_tag_info(snapshot['SnapshotId'], region, days_old, snapshot["Encrypted"], hours_old)
        
        if count == 10:
           break



##################################################################################
### Get all spanshots Tag info in the given region 
def snapshot_tag_info(snapshotid, region, days_old, encryption, hours_old):
    ec2 = boto3.resource('ec2', region)
    snapshot = ec2.Snapshot(snapshotid)
    
    if snapshot.tags is not None:
      
        if next(filter(lambda obj: obj.get('Key') == 'DR-Tier', snapshot.tags), None):
            try :
                instance_info = next(filter(lambda obj: obj.get('Key') == 'instance-id', snapshot.tags), None)
                instance = instance_info["Value"]
            except:
                instance = "No Instance ID Tag"
            try :
                name_info=next(filter(lambda obj: obj.get('Key') == 'Name', snapshot.tags), None)
                name=name_info["Value"]
            except:
                name ="No Name Tag"
            try :
                device_info=next(filter(lambda obj: obj.get('Key') == 'DeviceName', snapshot.tags), None)
                devicename=device_info["Value"]
            except:
                name ="No device Name"


            create_snapshot_dict(instance, name, region, days_old, snapshotid, encryption, devicename, hours_old)
    else :
        pass

    return 


def create_snapshot_dict(instance, name, region, days_old, snapshotid, encryption, devicename, hours_old):
    try: 
        snapshot_count = snapshot_dict[name]['Snapshots'] + 1
        snapshot_dict[name].update({"Snapshots":snapshot_count, devicename:hours_old})
    except:
        snapshot_dict[name] = {"Snapshots":1, "Region":region, "Days Old":days_old, "Encryption":encryption, devicename:hours_old}

##################################################################################
### convert output to csv  
def convert_csv(snapshotid, volume, region):
    pass


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
            print("Working on region", count, "of ", region_count, "(", region['RegionName'], ")")

            get_snapshot(region['RegionName'])
    else:

        get_snapshot(region)


##################################################################################
### initiates the function calls  and add on terminal call for functions 
if __name__ == '__main__':

    globals()[sys.argv[1]](sys.argv[2])


print(snapshot_dict)