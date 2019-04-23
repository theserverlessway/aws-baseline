GET_VPC_ID=aws ec2 describe-vpcs --query "Vpcs[?IsDefault].VpcId" --output text --region {}
LIST_REGIONS=aws ec2 describe-regions --query Regions[].RegionName --output text

list-default-vpcs:
	@$(LIST_REGIONS) | xargs -n 1 -I {} bash -c "$(GET_VPC_ID) | xargs echo Region: {} VPCID: "

remove-default-vpc-from-all-regions:
	@$(LIST_REGIONS) | xargs -n 1 -I {} bash -c "$(GET_VPC_ID) | xargs aws ec2 delete-vpc --region {} --vpc-id"