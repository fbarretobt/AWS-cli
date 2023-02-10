
import boto3
import sys
from datetime import datetime, timezone
import argparse
import botocore



client = boto3.client("sts")
account_id = client.get_caller_identity()["Account"]

print("Running on ", account_id)

print("#")
print("#")
print("#")



data_dict={}

def list_snapshots(region):
    ec2 = boto3.client('ec2', region)
    ec2_resource = boto3.resource('ec2', region)

    snapshot_list = ec2.describe_snapshots(OwnerIds=[ 'self' ])

    count = 0
    snap_count = len(snapshot_list["Snapshots"])

    for snapshot in snapshot_list["Snapshots"]:

        print("Working on ", count, "of ", snap_count, " in ", region)
        volumeID = snapshot['VolumeId']
        snapshotID = snapshot['SnapshotId']

        days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days
        seconds = (datetime.now(timezone.utc) - snapshot['StartTime']).total_seconds()
        hours = int(seconds // 3600)
        minutes = int((seconds//60)%60)


        if hours < 8 :
            get_snapshot_info(snapshotID, region, ec2_resource)

        count +=1

    convert_csv(data_dict,region)



def get_instance_info(instanceID, region, ec2_resource):

    instance = ec2_resource.Instance(instanceID)

    if instance.tags is not None:
        try :
            instance_info = next(filter(lambda obj: obj.get('Key') == 'Product', instance.tags), None)
            product = instance_info["Value"]
        except:
            product = "No product"
        try :
            instance_info = next(filter(lambda obj: obj.get('Key') == 'Version', instance.tags), None)
            version = instance_info["Value"]
        except:
            product = "No version"


    return {"Product":product, "Version":version}


def get_snapshot_info(snapshotID, region, ec2_resource):

    try :

        snapshot = ec2_resource.Snapshot(snapshotID)
        
        if snapshot.tags is not None:
        
            if next(filter(lambda obj: obj.get('Key') == 'DR-Tier', snapshot.tags), None):

                instance_info = next(filter(lambda obj: obj.get('Key') == 'instance-id', snapshot.tags), None)
                instanceID = instance_info["Value"]

                name_info=next(filter(lambda obj: obj.get('Key') == 'Name', snapshot.tags), None)
                name=name_info["Value"]

                device_info=next(filter(lambda obj: obj.get('Key') == 'DeviceName', snapshot.tags), None)
                devicename=device_info["Value"]
                instanceinfo = get_instance_info(instanceID, region, ec2_resource)

            

                root=next(filter(lambda obj: obj.get('Key') == 'Root', snapshot.tags), None)

            

                if name in data_dict.keys():
                    print(name,"already added ")
                else:
                    data_dict[name] = {"Name":name, "Product":instanceinfo['Product'], "Version":instanceinfo['Version'], "Instance Id": instanceID, "Region":region, "Root Snapshot":" ", "Root Encryption":"", "Non Root Snapshot":" ", "Non Root Encryption":""}

                if root["Value"] == "0":
                    rootdevice = snapshotID
                    rootEncrypted = snapshot.encrypted
                    data_dict[name].update({"Root Snapshot":rootdevice, "Root Encryption":rootEncrypted })
                else:
                    nonrootdevice = snapshotID
                    nonrootEncrypted = snapshot.encrypted
                    data_dict[name].update({"Non Root Snapshot":nonrootdevice, "Non Root Encryption":nonrootEncrypted})




            

        else :
            pass

    except:
        pass

    return 



##################################################################################
### convert output to csv  
def convert_csv(items_dict, region):
    file_name = region+".csv"
    header = "Hostname, Product, Version, Instance Id, Region,Root Snapshot,Root Encryption, Non Root Snapshot,Non Root Encryption"
    opened_file = open(file_name, 'a')
    opened_file.write(header)
    opened_file.close()

    for item in items_dict.values():
        opened_file = open(file_name, 'a')
        key_list= list(item)
        devicename = key_list[5]
        line = "\n "+item['Name']+","+item['Product']+","+item['Version']+","+item['Instance Id']+","+item['Region']+","+item['Root Snapshot']+","+str(item['Root Encryption'])+","+item['Non Root Snapshot'] +","+str(item['Non Root Encryption'])
        #print(line)
        opened_file.write(line)
        opened_file.close()
    

##################################################################################
### define whihch region to use or loop all the regions 
def region(region):

    if region == "all":
        regions = [ "ap-south-1",
                    "eu-north-1",
                    "eu-west-3" ,
                    "eu-west-2" ,
                    "eu-west-1" ,
                    "ap-northeast-3",
                    "ap-northeast-2",
                    "ap-northeast-1" ,
                    "ca-central-1" ,
                    "sa-east-1"  ,
                    "ap-southeast-1" ,
                    "ap-southeast-2" ,
                    "eu-central-1" ,
                    "us-east-1",
                    "us-east-2" ,
                    "us-west-1" ,
                    "us-west-2" ,
                  ]
        count=0 
        for region in regions:
            region_count=len(regions)
 
            count +=1 
            print("Working on region", count, "of ", region_count, "(", region, ")")

            list_snapshots(region)
    else:

        list_snapshots(region)


##################################################################################
### initiates the function calls  and add on terminal call for functions 
if __name__ == '__main__':

    globals()[sys.argv[1]](sys.argv[2])
