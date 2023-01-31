#!/bin/sh

total="0"
for REGION in $(aws ec2 describe-regions --output text --query 'Regions[].[RegionName]')
do
	echo $REGION

	Snapshot=$(aws ec2 describe-snapshots --owner-id self  --query "Snapshots[?(StartTime<='$(date --date='-2 month' '+%Y-%m-%d')')].SnapshotId"  --output text --region $REGION )

	count="0"
	for i in $Snapshot
	do
		((count++))

		echo "=========================================================================================================="
		echo "                                                                                                     "
		echo "                                                                                                      "
		echo "     AMI information based on Snapshot $i description                                                 "
		echo "                                                                                                      "
		echo "                                                                                                      "
		echo "=========================================================================================================="


		snapinfo=$(aws ec2 describe-snapshots --owner-ids self --snapshot-ids $i --region $REGION)


		snap_id=$(jq -r '.[] | .[] | .SnapshotId' <<< "$snapinfo")
		encryption=$(jq -r '.[] | .[] | .Encrypted' <<< "$snapinfo")
		ami=$(jq -r '.[] | .[] | .Description' <<< "$snapinfo" | awk '{print $5}')
		policy=$(jq -r '.[] | .[] | .Description' <<< "$snapinfo" | awk '{print $4}')


		if [[ "$policy" =~ .*"policy-".* ]]; then
				echo "===== Policy Info"
				policy_info=$(aws dlm get-lifecycle-policy --policy-id $policy --output json --region $REGION)


				description=$(jq -r '.Policy.Description' <<< "$policy_info")
				echo "DEscription : " $description
				policy_id=$(jq -r '.Policy.PolicyId' <<< "$policy_info")
				echo "Policy ID : " $policy_id
				state=$(jq -r '.Policy.State' <<< "$policy_info")
				echo "State : " $state

				echo "Total snaps = " $count
		fi																																	


	done

	echo "Total Snapshots older than 30 days in $REGION = "$count 

	total=$(($total + $count))

done
echo "++ "
echo "++ "
echo "++ "
echo "++ "
echo "++ "
echo "++ "
echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "++      Total across regions = " $total
echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"