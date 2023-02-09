from tracemalloc import Snapshot
import boto3
import sys
from datetime import datetime, timezone
import argparse
import botocore
import printt



def list_snapshots(region):
    ec2_resource = boto3.resource('ec2', region)
    ec2 = boto3.client('ec2', region)

    snapshot_list = ec2.describe_snapshots(OwnerIds=[ 'self' ])

    for snapshot in snapshot_list["Snapshots"]:
        volumeID = snapshot['VolumeId']
        snapshotID = snapshot['SnapshotId']

        try :
            snapshot = ec2_resource.Snapshot(snapshotid)
        
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
                
                printt(name, devicename, instance)
        else :
            pass
    except:
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

            list_snapshots(region['RegionName'])
    else:

        list_snapshots(region)


##################################################################################
### initiates the function calls  and add on terminal call for functions 
if __name__ == '__main__':

    globals()[sys.argv[1]](sys.argv[2])
