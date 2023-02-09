from tracemalloc import Snapshot
import boto3
import sys
from datetime import datetime, timezone
import argparse
import botocore



def list_snapshots(region):
    ec2_resource = boto3.resource('ec2', region)
    ec2 = boto3.client('ec2', region)

    instaces_list = ec2_resource.Instance.all()
    volume_list = ec2_resource.Volume.all()
    snapshot_list = ec2_resource.Snapshot.all()

    for instance in instaces_list:
        print(instance.volumes.all())