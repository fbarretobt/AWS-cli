from tracemalloc import Snapshot
import boto3
import sys
from datetime import datetime, timezone
import argparse
import botocore



def list_snapshots(region):
    ec2_resource = boto3.resource('ec2', region)
    ec2 = boto3.client('ec2', region)

    snapshot_list = ec2.describe_snapshots(OwnerIds=[ 'string' ])
    instaces_list = ec2_resource.Instance.all()
    volume_list = ec2_resource.Volume.all()


    for instance in snapshot_list["SnapshotId"]:
        print(instance)



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
