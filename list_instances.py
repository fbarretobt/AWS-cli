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
    data_dict = {}
    for reservation in Instance_list['Reservations']:

        for instance in reservation['Instances']:
            instanceID = (instance['InstanceId'])
            rootdevice = (instance["RootDeviceName"])

            for device in instance['BlockDeviceMappings']:
                devicename = (device['DeviceName'])
                volumeID = (device.get('Ebs', {}).get("VolumeId"))


                if devicename != rootdevice :
                    nonrootdevice = devicename

                volume = ec2.describe_volumes(VolumeIds = [volumeID])

                for volumeinfo in volume['Volumes']:
                    encryption = volumeinfo['Encrypted']
                    snapshot = volumeinfo['SnapshotId']
                    for device in volumeinfo['Attachments']:
                        device=(device['Device'])
                        if device == rootdevice:
                            rootsnapshot = snapshot
                        else:
                            nonrootsnapshot=snapshot

            for tag in instance['Tags']:

               if tag['Key'] == "Name":
                    name = tag['Value']
               elif tag['Key'] == "Product":
                    product = tag['Value']
               elif tag['Key'] == "Version":
                    version = tag['Value']


            data_dict.update({"Hostname":name, "Product":product,"Version":version, "Instance ID":instanceID, "Root Device":rootdevice, "Non root Device": nonrootdevice, "Root Snapshot": rootsnapshot, "Non Root Snapshot": nonrootsnapshot, "Region":region, "Encryption":encryption})


        count +=1
        
        if count == 10:
            break        

    #create_csv(data_dict)

    print(data_dict)

    return 

def create_csv(data):
    file_name = "list.csv"
    header = "Hostname, Product,Version, Instance ID, Root Snapshot, Non Root Snapshot, Region, Encryption"
    opened_file = open(file_name, 'a')
    opened_file.write(header)
    opened_file.close()

    for item in data.values():
        opened_file = open(file_name, 'a')
        key_list= list(item)
        devicename = key_list[5]
        line = "\n" + item["Hostname"] + "," + item['version'] + "," + item['Product'] + "," + item["Instance ID"] + "," + item["Root Snapshot"] + "," + item["Non Root Snapshot"] + "," + item["Region"] + ","+ str(item["Encryption"])
        print(line)
        opened_file.write(line)
        opened_file.close()


    
    
    

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