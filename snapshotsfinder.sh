#!/bin/sh

for REGION in $(aws ec2 describe-regions --output text --query 'Regions[].[RegionName]') ; 
    do

    Snapshots=$(aws ec2 describe-snapshots --owner-id self  --query "Snapshots[?(StartTime<='$(date --date='-1 month' '+%Y-%m-%d')')].{ID:SnapshotId}" --output text --region $REGION)
    #Snapshots="snap-0366f4adb11b16dd3"
    #Snapshots="snap-0ca1c5480c699e314"

    for i in $Snapshots
    do


        echo "=========================================================================================================="
        echo "||"                                                                                                  
        echo "||"                                                                                                   
        echo "     AMI information based on Snapshot $i description  in --region $REGION"                                               
        echo "   "                                                                                                  
        echo "   "                                                                                                    


        snapinfo=$(aws ec2 describe-snapshots --snapshot-ids $i --region $REGION)
        

        snap_id=$(jq -r '.[] | .[] | .SnapshotId' <<< "$snapinfo")
        encryption=$(jq -r '.[] | .[] | .Encrypted' <<< "$snapinfo")
        ami=$(jq -r '.[] | .[] | .Description' <<< "$snapinfo" | awk '{print $5}')
        policy=$(jq -r '.[] | .[] | .Description' <<< "$snapinfo" | awk '{print $4}')
        name=$(jq -r '.[] | .[] | .Tags[] | select(.Key=="Name").Value' <<< "$snapinfo")
        date=$(jq -r '.[] | .[] | .StartTime' <<< "$snapinfo")
        volume=$(jq -r '.[] | .[] | .VolumeId' <<< "$snapinfo")
        


        volumeinfo=$(aws ec2 describe-volumes --volume-ids $volume --region $REGION)

        instance=$(jq -r '.[] | .[] | .Attachments[] | .InstanceId' <<< "$volumeinfo")
        VolumeState=$(jq -r '.[] | .[] | .State' <<< "$volumeinfo")

        policyinfo=$(aws dlm get-lifecycle-policy --policy-id $policy --region $REGION)

        instancestatus=$(aws ec2 describe-instances --instance-ids  $instance --query "Reservations[*].Instances[*].{Status:State.Name}" --region $REGION)

        if [ $? == 0 ]; then
            echo ""

            policy_name=$(jq -r '.[] | .Description' <<< "$policyinfo")

            echo "Snap ID : " $snap_id
            echo "Encryption : " $encryption
            echo "Policy Name : " $policy_name
            echo "Snapshot Name : " $name
            echo "Creation Date : " $date
            echo "Volume : " $volume
            echo "Volume State : " $VolumeState
            echo "Instance Status : " $instancestatus
        else    

            echo ""
            
        fi


        echo "||"
        echo "||"
        echo "||"
        echo "||"
        echo "=========================================================================================================="

    done
done