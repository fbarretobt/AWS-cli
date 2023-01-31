import boto3
import sys
import argparse
instance_id = "i-0ae4e19b44a5fbe70"

def print_ec2_tagname(instance_id):
    ec2 = boto3.resource("ec2", region_name="us-west-1")
    ec2instance = ec2.Instance(instance_id)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
    #return instancename
    print (instancename)

print_ec2_tagname(instance_id)