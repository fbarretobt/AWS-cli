from tracemalloc import Snapshot 
import boto3
import json
import sys
from datetime import datetime, timezone
import argparse
import botocore


def list_instances(region):
    ec2 = boto3.client('ec2', region)
    Instance_list = ec2.describe_instances()

    count = 0

    for reservation in Instance_list['Reservations']:
        for instance in x['Instances']:
	        print(instance['InstanceId'])

        count +=1
        
        if count == 1:
            break        

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

            list_instances(region['RegionName'])
    else:

        list_instances(region)


##################################################################################
### initiates the function calls  and add on terminal call for functions 
if __name__ == '__main__':

    globals()[sys.argv[1]](sys.argv[2])