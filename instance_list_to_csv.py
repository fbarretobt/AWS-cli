from tracemalloc import Snapshot
import boto3
import json
import sys
from datetime import datetime, timezone
import argparse
import botocore

##################################################################################
### Get all spanshots in the given region 
def get_snapshot(region):
    ec2 = boto3.client('ec2', region)

    snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])

    for snapshot in snapshot_response['Snapshots']:
        print(snapshot['SnapshotId'])
    pass



def convert_csv():
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
            print("Working on region", count, "of ", region_count, "(", region, ")")

            get_snapshot(region['RegionName'])
    else:

        get_snapshot(region)


##################################################################################
### initiates the function calls  and add on terminal call for functions 
if __name__ == '__main__':

    globals()[sys.argv[1]](sys.argv[2])


