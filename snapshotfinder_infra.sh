#!/bin/sh


single_region(){
	
	Snapshot=$(aws ec2 describe-snapshots --owner-id self  --query 'Snapshots[].SnapshotId' --filters Name=encrypted,Values=false --output text )


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
		policy=$(jq -r '.[] | .[] | .Description' <<< "$snapinfo" | awk '{print $4}')


		if [[ "$ami" =~ .*"ami-".* ]]; then
			echo "===== AMI info"
			aws ec2 describe-images --image-ids $ami --query 'Images[*].{ EBS_ecryption:BlockDeviceMappings[*].Ebs.Encrypted, DeleteOnTermination:BlockDeviceMappings[*].Ebs.DeleteOnTermination, Image_Name: Name, State:State}'   --output table
		elif [[ "$policy" =~ .*"policy-".* ]]; then
			echo "===== Policy Info"
			policy_info=$(aws dlm get-lifecycle-policy --policy-id $policy --output json) 
			
			
			description=$(jq -r '.Policy.Description' <<< "$policy_info")
			echo "DEscription : " $description
			policy_id=$(jq -r '.Policy.PolicyId' <<< "$policy_info")
			echo "Policy ID : " $policy_id
			state=$(jq -r '.Policy.State' <<< "$policy_info")
			echo "State : " $state
			
		else
			echo "No other Info ********"
		fi

		echo "===== Snapshot info"
		aws ec2 describe-snapshots --owner-ids self --snapshot-ids $snap_id --output table

	done

}


multi_region(){
	for REGION in $(aws ec2 describe-regions --output text --query 'Regions[].[RegionName]')
	do 
		echo $REGION

		Snapshot=$(aws ec2 describe-snapshots --owner-id self  --query 'Snapshots[].SnapshotId' --filters Name=encrypted,Values=false --output text --region $REGION )


		for i in $Snapshot
		do 


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


			if [[ "$ami" =~ .*"ami-".* ]]; then
				echo "===== AMI info"
				aws ec2 describe-images --image-ids $ami --query 'Images[*].{ EBS_ecryption:BlockDeviceMappings[*].Ebs.Encrypted, DeleteOnTermination:BlockDeviceMappings[*].Ebs.DeleteOnTermination, Image_Name: Name, State:State}'   --output table --region $REGION
			elif [[ "$policy" =~ .*"policy-".* ]]; then
				echo "===== Policy Info"
				policy_info=$(aws dlm get-lifecycle-policy --policy-id $policy --output json --region $REGION) 
				
				
				description=$(jq -r '.Policy.Description' <<< "$policy_info")
				echo "DEscription : " $description
				policy_id=$(jq -r '.Policy.PolicyId' <<< "$policy_info")
				echo "Policy ID : " $policy_id
				state=$(jq -r '.Policy.State' <<< "$policy_info")
				echo "State : " $state
				
			else
				echo "No other Info ********"
			fi

			echo "===== Snapshot info"
			aws ec2 describe-snapshots --owner-ids self --snapshot-ids $snap_id --output table --region $REGION

		done


	done

}



for arg in "$@"; do
  case $arg in
    -s | --single)
      single_region
      ;;
    -m | --multi)
      multi_region
      ;;
	-v | --version)
	  Echo "Version 1.0"
    ?)
      echo "script usage:  [-s] [-m] " >&2
	  echo "Use -m / --multi for multi region "
	  echo "Use -s / --single for single region active region"
      exit 1
      ;;
  esac
done
shift "$(($OPTIND -1))"
