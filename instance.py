from tracemalloc import Snapshot
import boto3
import json
import sys
from pprint import pprint
from datetime import datetime, timezone
import botocore




ec2 = boto3.client('ec2')

instance_response = ec2.describe_instances(InstanceIds=[attachment['i-0ae4e19b44a5fbe70']])

print(instance_response)