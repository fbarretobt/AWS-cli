#!/bin/sh


for REGION in $(aws ec2 describe-regions --output text --query 'Regions[].[RegionName]')
	do 
		echo $REGION

		Snapshot=$(aws ec2 describe-snapshots --owner-id self  --query 'Snapshots[].SnapshotId' --filters Name=encrypted,Values=false --output text --region $REGION )

		count="0"
		for i in $Snapshot
		do 
			$count=+1

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
            fi


		done

		echo "Total Snapshots older than 30 days in all regions = "$count 
	done