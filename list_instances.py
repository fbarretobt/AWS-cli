import boto3
import sys
from datetime import datetime, timezone
import argparse
import botocore


def list_instances(region):
    ec2 = boto3.client('ec2', region)
    ec2_resource = boto3.resource('ec2', region)
    Instance_list = ec2.describe_instances()

    count = 0

    for reservation in Instance_list['Reservations']:
        for instance in reservation['Instances']:
            instanceID = (instance['InstanceId'])
            rootdevice = (instance["RootDeviceName"])

            for device in instance['BlockDeviceMappings']:
                devicename = (device['DeviceName'])
                volumeID = (device.get('Ebs', {}).get("VolumeId"))

                volume = ec2.describe_volumes(VolumeId = volumeID)

                print(volume)
                
                print(devicename, volumeID)

                if devicename != rootdevice :
                    nonrootdevice = devicename

            for tag in instance['Tags']:

               if tag['Key'] == "Name":
                    name = tag['Value']
               elif tag['Key'] == "Product":
                    product = tag['Value']
               elif tag['Key'] == "Version":
                    version = tag['Value']


            #print(name, product, instanceID, version, rootdevice, nonrootdevice, volumeID)

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