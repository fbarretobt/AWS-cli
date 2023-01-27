import boto3


response = snapshot.describe_attribute(
    Attribute='productCodes'|'createVolumePermission',
    DryRun=False
)