#!/bin/sh

Snapshot=$(aws ec2 describe-snapshots --owner-id self --filters Name=encrypted,Values=false --output text)

for i in $Snapshot
do 

	AMI=$($i| awk '{print $6}')
	snap_ID=$($i| awk '{print $10}')
	echo "=========================================================================================================="
	echo "||                                                                                                      ||"
	echo "||                                                                                                      ||"
	echo "||     AMI information based on Snapshot description                                                    ||"
	echo "||                                                                                                      ||"
	echo "||                                                                                                      ||"
	echo "=========================================================================================================="
	aws ec2 describe-images --image-ids $ami  --query 'Images[*].{Image_Name: Name, State:State}'   --output table 
	aws ec2 describe-snapshots --snapshot-ids $snap_ID  --output table
done 

