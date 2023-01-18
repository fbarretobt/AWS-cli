#!/bin/sh

AMI=$(aws ec2 describe-snapshots --owner-id self --filters Name=encrypted,Values=false --output text | awk '{print $6}')

for i in AMI
do 
	echo $i;
done 

