import boto3


ec2 = boto3.client('ec2')

regions_list = ec2.describe_regions()

#print(regions)
 
regions = regions_list["Regions"]

for region in regions: 
    print(region['RegionName'])

