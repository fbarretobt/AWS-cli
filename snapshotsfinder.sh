#!/bin/sh

#Snapshots=$(aws ec2 describe-snapshots --owner-id self  --query "Snapshots[?(StartTime<='$(date --date='-2 month' '+%Y-%m-%d')')].{ID:SnapshotId}" --output text )
Snapshots="snap-0a92a41b03a8e33b7"

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
    encryption=$(jq -r '.[] | .[] | .Encrypted' <<< "$snapinfo")
    ami=$(jq -r '.[] | .[] | .Description' <<< "$snapinfo" | awk '{print $5}')
    policy=$(jq -r '.[] | .[] | .Description' <<< "$snapinfo" | awk '{print $4}')
    name=$(jq -r '.[] | .[] | .Tags[9].Value' <<< "$snapinfo")


    policyinfo=$(aws dlm get-lifecycle-policy --policy-id $policy )

    policy_name=$(jq -r '.[] | .[] | .Description' <<< "$policyinfo")

    echo "Snap ID : " $snap_id
    echo "Encryption : " $encryption
    echo "Policy Name : " $policy_name
    echo "Name : " $name

done
