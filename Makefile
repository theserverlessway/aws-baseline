new:
	formica new -c stack.config.yaml
	formica deploy -c stack.config.yaml

create-account:
ifndef EMAIL
	$(error EMAIL is undefined)
endif

ifndef NAME
	$(error NAME is undefined)
endif
	echo aws organizations create-account --email $(EMAIL) --account-name $(NAME)

list-accounts:
	awsinfo orgs

REGIONS=$(shell aws ec2 describe-regions --query "Regions[].RegionName" --output text)

add-all-regions-to-stack-set:
ifndef STACKSET
	$(error STACKSET is undefined)
endif
ifndef ACCOUNT
	$(error ACCOUNT is undefined)
endif
	formica stack-set add-instances --accounts $(ACCOUNT) --regions $(REGIONS) -s $(STACKSET)
