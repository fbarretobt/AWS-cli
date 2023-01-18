#!/bin/sh


infra(){
	
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
		aws ec2 describe-images --image-ids ami-022b4ada5cc036418 --query 'Images[*].{ EBS_ecryption:BlockDeviceMappings[*].Ebs.Encrypted, DeleteOnTermination:BlockDeviceMappings[*].Ebs.DeleteOnTermination, Image_Name: Name, State:State}'   --output 
	table

		echo "===== Snapshot info"
		aws ec2 describe-snapshots --owner-ids self --snapshot-ids $snap_id --output table
	done

}



rs(){
	echo"rs"
}


pra(){
	echo"PRA"
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
