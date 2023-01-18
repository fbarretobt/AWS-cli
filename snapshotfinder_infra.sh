#!/bin/sh


infra(){
	
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
			policy_info=$(aws dlm get-lifecycle-policy --policy-id $policy --output json )
			description=$(jq -r '.Policy.Description' <<< "$policy")
			echo "DEscription : " $description
			policy_id=$(jq -r '.Policy.PolicyId' <<< "$policy")
			echo "Policy ID : " $policy_id
			state=$(jq -r '.Policy.State' <<< "$policy")
			echo "State : " $state
			
		else
			echo "No other Info ********"
		fi

		echo "===== Snapshot info"
		aws ec2 describe-snapshots --owner-ids self --snapshot-ids $snap_id --output table

	done

}





while getopts 'ipr:' OPTION; do
  case "$OPTION" in
    i)
      infra
      ;;
    p)
      pra
      ;;
    r)
      rs
      ;;
    ?)
      echo "script usage: $(basename \$0) [-i] [-i] [-r]" >&2
      exit 1
      ;;
  esac
done
shift "$(($OPTIND -1))"
