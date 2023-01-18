#!/bin/sh

Snapshot=$(aws ec2 describe-snapshots --owner-id self --filters Name=encrypted,Values=false --output text | awk '{print $10}')



for i in $Snapshot
do 


	echo "=========================================================================================================="
	echo "                                                                                                     "
	echo "                                                                                                      "
	echo "     AMI information based on Snapshot $i description                                                 "
	echo "                                                                                                      "
	echo "                                                                                                      "
	echo "=========================================================================================================="
	

	snapinfo=$(aws ec2 describe-snapshots --owner-ids self --snapshot-ids $i)


	snap_id=$(jq -r '.[] | .[] | .SnapshotId' <<< "$snapinfo")
	encryption=$(jq -r '.[] | .[] | .Encrypted' <<< "$snapinfo")
	ami=$(jq -r '.[] | .[] | .Description' <<< "$snapinfo" | awk '{print $5}')

	
	echo "===== AMI info"
	aws ec2 describe-images --image-ids $ami  --query 'Images[*].{Image_Name: Name, State:State}'   --output table 

	echo "===== Snapshot info"
	aws ec2 describe-snapshots --owner-ids self --snapshot-ids $snap_id --output table
done 
