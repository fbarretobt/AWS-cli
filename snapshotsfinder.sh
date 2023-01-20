#!/bin/sh

Snapshots=$(aws ec2 describe-snapshots --owner-id self  --query 'Snapshots[].SnapshotId' --output text )


for i in $Snapshots
do 

    
    echo "=========================================================================================================="
    echo "   "                                                                                                  
    echo "   "                                                                                                   
    echo "     AMI information based on Snapshot $i description  "                                                
    echo "   "                                                                                                  
    echo "   "                                                                                                    
    echo "=========================================================================================================="
			
    snapinfo=$(aws ec2 describe-snapshots --snapshot-ids $i)


    snap_id=$(jq -r '.[] | .[] | .SnapshotId' <<< "$snapinfo")


    echo "ID : " $snap_id
done