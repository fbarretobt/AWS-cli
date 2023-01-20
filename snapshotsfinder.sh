#!/bin/sh


for REGION in $(aws ec2 describe-regions --output text --query 'Regions[].[RegionName]')
do 

    Snapshot=$(aws ec2 describe-snapshots --owner-id self  --query 'Snapshots[].SnapshotId' --filters Name=encrypted,Values=false --output text )

    echo "=========================================================================================================="
    echo "   "                                                                                                  
    echo "   "                                                                                                   
    echo "     AMI information based on Snapshot $i description  "                                                
    echo "   "                                                                                                  
    echo "   "                                                                                                    
    echo "=========================================================================================================="
			
    snapinfo=$(aws ec2 describe-snapshots --owner-ids self --snapshot-ids $i)


    snap_id=$(jq -r '.[] | .[] | .SnapshotId' <<< "$snapinfo")
    encryption=$(jq -r '.[] | .[] | .Encrypted' <<< "$snapinfo")
    ami=$(jq -r '.[] | .[] | .Description' <<< "$snapinfo" | awk '{print $5}')
    policy=$(jq -r '.[] | .[] | .Description' <<< "$snapinfo" | awk '{print $4}')
    name=$(jq -r '.[] | .[] | .[] | .Name' <<< "$snapinfo" )

    echo "Name : " $name
done