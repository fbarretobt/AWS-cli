import boto3


ec2 = boto3.client('ec2')

regions = ec2.describe_regions()

print( "Regionws = " + regions)


