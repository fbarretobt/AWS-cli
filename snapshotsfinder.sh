#!/bin/sh



find_policy(){
#Snapshots=$(aws ec2 describe-snapshots --owner-id self  --query "Snapshots[?(StartTime<='$(date --date='-2 month' '+%Y-%m-%d')')].{ID:SnapshotId}" --output text )
#Snapshots="snap-0366f4adb11b16dd3"
#Snapshots="snap-0ca1c5480c699e314"

for i in $Snapshots
do


    echo "=========================================================================================================="
    echo "||"                                                                                                  
    echo "||"                                                                                                   
    echo "     AMI information based on Snapshot $i description  "                                                
    echo "   "                                                                                                  
    echo "   "                                                                                                    


    snapinfo=$(aws ec2 describe-snapshots --snapshot-ids $i)


    snap_id=$(jq -r '.[] | .[] | .SnapshotId' <<< "$snapinfo")
    encryption=$(jq -r '.[] | .[] | .Encrypted' <<< "$snapinfo")
    ami=$(jq -r '.[] | .[] | .Description' <<< "$snapinfo" | awk '{print $5}')
    policy=$(jq -r '.[] | .[] | .Description' <<< "$snapinfo" | awk '{print $4}')
    name=$(jq -r '.[] | .[] | .Tags[9].Value' <<< "$snapinfo")


    policyinfo=$(aws dlm get-lifecycle-policy --policy-id $policy)

    if [ $? == 0 ]; then
        echo ""

        policy_name=$(jq -r '.[] | .Description' <<< "$policyinfo")

        echo "Snap ID : " $snap_id
        echo "Encryption : " $encryption
        echo "Policy Name : " $policy_name
        echo "Snapshot Name : " $name
    else    

        echo ""
        
    fi


    echo "||"
    echo "||"
    echo "||"
    echo "||"
    echo "=========================================================================================================="

done

}


while getopts s:p:i: flag
do
    case "${flag}" in
        s) s=${OPTARG};;
        p) p=${OPTARG};;
        i) i=${OPTARG};;
    esac
done



echo "Snap = $s "
echo "Policy = $p"
echo "Image = $i