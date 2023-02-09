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
    instance_count = len(Instance_list['Reservations'])
    data_dict = {}
    for reservation in Instance_list['Reservations']:

        count +=1
        print("Working on ", count, "of ", instance_count, "Instances")

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
                            rootencryption = snapshot['Encrypted']



                snapshots = ec2.describe_snapshots(Filters=[{'Name':'volume-id', 'Values': [ volumeID] }])

                for snapshot in snapshots["Snapshots"]:

                    days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days
                    seconds = (datetime.now(timezone.utc) - snapshot['StartTime']).total_seconds()
                    hours = int(seconds // 3600)
                    minutes = int((seconds//60)%60)



                    if hours < 4 :
                        
                        if rootsnapshot != snapshot['SnapshotId']:

                            nonrootsnapshot=snapshot['SnapshotId']
                            nonrootencryption = encryption



            for tag in instance['Tags']:

               if tag['Key'] == "Name":
                    name = tag['Value']
               elif tag['Key'] == "Product":
                    product = tag['Value']
               elif tag['Key'] == "Version":
                    version = tag['Value']


            data_dict[name] = {"Hostname":name, "Product":product,"Version":version, "Instance ID":instanceID, "Root Device":rootdevice, "Non root Device": nonrootdevice, "Root Snapshot": rootsnapshot, "Non Root Snapshot": nonrootsnapshot, "Region":region, "Encryption":encryption}



        
        #if count == 20:
        #    break        

    create_csv(data_dict, region)



    return 

def create_csv(data, region):
    file_name = region+".csv"
    header = "Hostname, Product,Version, Instance ID, Root Snapshot, Non Root Snapshot, Region, Encryption"
    opened_file = open(file_name, 'a')
    opened_file.write(header)
    opened_file.close()

    for item in data.values():
        opened_file = open(file_name, 'a')
        line = "\n" + item["Hostname"] + "," + item['Product'] + "," + item['Version'] + "," + item["Instance ID"] + "," + item["Root Snapshot"] + "," + item["Non Root Snapshot"] + "," + item["Region"] + "," + str(item["Encryption"])
        #print(line)
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