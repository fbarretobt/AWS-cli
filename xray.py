from tracemalloc import Snapshot
import boto3
import json
import sys
from pprint import pprint
from datetime import datetime, timezone
import argparse
import botocore




def print_ec2_tagname(instance_id):
    ec2 = boto3.resource("ec2")
    ec2instance = ec2.Instance(instance_id)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
    #return instancename
    return instancename




ec2 = boto3.client('ec2')
snapshot_response = ec2.describe_snapshots(OwnerIds=['self'])

not_found_volumes={}
instances_attached={}

for snapshot in snapshot_response['Snapshots']:

    days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days


    if days_old >= 29:

        try:

            volume_response = ec2.describe_volumes(VolumeIds=[snapshot['VolumeId']])
            volume = volume_response['Volumes'][0]

            for attachment in volume['Attachments']:


                #print ("+++++++++++++++++++++++++++")
                #print ("+")
                #print(snapshot['SnapshotId'])
                #print("Snapshot is ", days_old, "days old") 
                #print("Instance ID :" + attachment['InstanceId'])
                #print ("+")
                #print ("+")
                #print ("+++++++++++++++++++++++++++")


                instance_name=print_ec2_tagname(attachment['InstanceId'])
                instances_attached.update({snapshot['SnapshotId']:instance_name})

                #print("Name: ",instance_name)


        except botocore.exceptions.ClientError as error:

            if error.response['Error']['Code'] == 'InvalidVolume.NotFound':

                #print("Volume not found ", snapshot['VolumeId'] )
                not_found_volumes.update({snapshot['SnapshotId']:snapshot['VolumeId']})

            else: # Unknown exception

                print(error.response)
    
    else :

        continue

#print("List of snaps whith volumes not found :", not_found_volumes)
#print(" ")

#print("List of instances attached to snaps :" , instances_attached)


sorted_not_found_by_volume=sorted(not_found_volumes.items(), key=lambda x:x[1])
convert_not_fount=dict(sorted_not_found_by_volume)
print("||  Snaps with non running instances: ")
print("||")
print("||")
for key, value in convert_not_fount.items():

    print("Snapshot:", key, ' = ',"Volume:", value)

print("||")
print("||")
print ("Total of ", len(convert_not_fount), " Snapshots with non running instances")
print("||")
print("||")
print("||")
print("===============================================================================")
print("||  Snaps with  running instances:")  

sorted_running=sorted(instances_attached.items(), key=lambda x:x[1])
convert_running=dict(sorted_running)
for key, value in convert_running.items():

    print(key, ' = ',"Instance:", value)