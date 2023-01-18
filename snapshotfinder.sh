#!/bin/sh

AMI=$(aws ec2 describe-snapshots --owner-id self --filters Name=encrypted,Values=false --output text | awk '{print $6}')

for i in $AMI
do 
	aws ec2 describe-images --image-ids $i  --query 'Images[*].{Image_Name: Name, State:State}'   --output table 
	echo "=========================================================================================================="
	echo "||                                                                                                      ||"
	echo "||                                                                                                      ||"
	echo "||     AMI information based on Snapshot description                                                    ||"
	echo "||                                                                                                      ||"
	echo "||                                                                                                      ||"
	echo "=========================================================================================================="
	aws ec2 describe-images --image-ids $i  --query 'Images[*].{Image_Name: Name, State:State}'   --output table 
done 

