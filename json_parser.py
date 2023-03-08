import json
import boto3
import botocore
import sys
import os
from datetime import datetime, timezone

Instance_Not_Found = {}
Instance_Found = {}
Image_info = {}

### load json file and return the data from the file
def load_file():
    files = {}
    count = 0
    for x in os.listdir():
        if x.endswith(".json"):
            count += 1
            # Prints only text file present in My Folder
            files.update({count: x})
    for file in files:
        print(str(file) + " : " + files[file])

    user_input = input("Chose the number from the list above: ")

    with open(files[int(user_input)]) as file:
        data = json.load(file)

    return data


## get the data loaded and parses it
def parse_data():
    data = load_file()

    for region in data.keys():

        count = 0

        for snapshot in data[region]:
            if instance := data[region][snapshot].get("Instance"):
                check_instance(region, data[region][snapshot]["Instance"], snapshot, data[region][snapshot]["Name"])
            elif data[region][snapshot]["Tags"] == "NO TAGS":
                check_snapshot_notags(region, snapshot)
            else:
                check_snapshot(region, data[region][snapshot]["Instance"], snapshot, data[region][snapshot]["Name"])



def check_snapshot_notags(region, snapshot):
    client = boto3.client('ec2', region)
    resource = boto3.resource('ec2', region)


    try:
        snapshot_response = client.describe_snapshots(SnapshotIds=[snapshot])

        for snap in snapshot_response["Snapshots"]:
            #print(snap["Description"])
            description =  snap["Description"].split()

            #ami = [x for x in description if x.startswith("ami")]

            for ami in description:
                if ami.startswith("ami"):

                    check_ami(region, ami, snapshot)

    except botocore.exceptions.ClientError as error:
        snapshot_status = error.response['Error']['Code']
        pass


def check_ami(region, ami, snapshot):
    client = boto3.client('ec2', region)
    resource = boto3.resource('ec2', region)

    try :
        print("checking ", ami)
        ami_response = client.describe_images(ImageIds=[ami])
        for image in ami_response["Images"]:

            if "Description" in image.keys():
                image_info = image["Description"]
                ami_status = image["State"]
            if "Name" in image.keys():
                image_info = image["Name"]
                ami_status = image["State"]



    except botocore.exceptions.ClientError as error:
        ami_status = error.response['Error']['Code']
        image_info = "No info"

    if ami_status == "available":

        print("Checking snapshot for ami:  ",ami, snapshot, region)
        image_info_list(region, snapshot, image_info, ami_status, ami)
    else:
        pass


def image_info_list(region, snapshot, image_info, ami_status, ami):
    if ami not in Image_info:
        Image_info[ami] = {"Region": region,"Snapshots":[snapshot], "Image":image_info, "Status":ami_status}
    else :

        Image_info[ami]["Snapshots"].append(snapshot)

    create_file(Image_info, "Image_information")

def check_instance(region, instanceID, snapshot, instanceName):
    client = boto3.client('ec2', region)
    resource = boto3.resource('ec2', region)

    print("Checking instance :", instanceID)

    try:
        instance_response = client.describe_instances(InstanceIds=[instanceID])
        for instance in instance_response["Reservations"]:
            for node in instance["Instances"]:
                instance_status = node['State']['Name']
                # print("Instance Found and running, Checking the snapshots : ")
                check_snapshot(region, instanceID, instance_status, snapshot, instanceName)


    except botocore.exceptions.ClientError as error:
        instance_status = error.response['Error']['Code']
        instance_not_found(region, snapshot, instanceID, instance_status)



def check_snapshot(region, instanceID, instance_status, snapshotID, instanceName):
    client = boto3.client('ec2', region)
    resource = boto3.resource('ec2', region)
    print("Checking snapshot:  ", snapshotID)

    try:
        snapshot_response = client.describe_snapshots(Filters=[{'Name': 'tag:Name', 'Values': [instanceName]}])

        old_count = 0
        current_count = 0

        for snapshot in snapshot_response['Snapshots']:
            days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days

            if days_old > 29:
                old_count = old_count + 1

            else:
                current_count = current_count + 1

            for tags in snapshot["Tags"]:
                if tags["Key"] == "DR-Tier":
                    drtier = tags["Key"] + " " + tags["Value"]
                    print(drtier)


            instance_found(region, instanceID, snapshot["SnapshotId"], instance_status, instanceName, old_count, current_count, days_old, drtier)

    except botocore.exceptions.ClientError as error:
        snapshot_status = error.response['Error']['Code']
        pass

    # print("Json dump")
    # print(json.dumps(Instance_Found, indent=4))


def instance_not_found(region, snapshot, instance, instance_status):

    if instance not in Instance_Not_Found:
        Instance_Not_Found[instance] = {"Region": region, "Instance Status": instance_status, "Snapshots": [snapshot]}
    else:
        Instance_Not_Found[instance]["Snapshots"].append(snapshot)

    create_file(Instance_Not_Found, "instances_not_found")


def instance_found(region, instance, snapshot, instance_status, instanceName, old_count, current_count, days_old,
                   drtier):

    if instance not in Instance_Found:

        Instance_Found[instance] = {"Region": region, "Instance Status": instance_status, "Name": instanceName,
                        "Snapshots": [{snapshot: str(days_old) + "Days Old"}], "Old snapshots": old_count,
                        "Current Snapshots": current_count, "Tags": [drtier]}
    else:
        Instance_Found[instance]["Snapshots"].append({snapshot: str(days_old) + " Days Old"})
        Instance_Found[instance].update({"Old snapshots": old_count,
                        "Current Snapshots": current_count})


    create_file(Instance_Found, "instances_found")

def create_file(data, filename):
    with open(filename + '.json', "w") as file:
        json.dump(data, file, indent=4, default=str)


def run():
    parse_data()


    run = input("re-run parser? y/n : ")

    return run


##################################################################################
### initiates the function calls  and add on terminal call for functions
if __name__ == '__main__':

    while run() == "y":
        run()
