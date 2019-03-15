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


LIST_STACK_SETS_COMMAND=@aws cloudformation list-stack-sets --status ACTIVE --query "Summaries[].StackSetName" --output text

stack-sets:
	 $(LIST_STACK_SETS_COMMAND) | (xargs -n 1 -P 15 aws cloudformation describe-stack-set --query "StackSet.{\"1.Name\":StackSetName, \"2.Accounts\":$(call TAG_VALUE,Accounts), \"3.Regions\":$(call TAG_VALUE,Regions), \"4.CommitId\":$(call TAG_VALUE,CommitId), \"5.CommitCount\":$(call TAG_VALUE,CommitCount), \"6.LastUpdated\":$(call TAG_VALUE,LastUpdated), \"7.ComparisonAccount\":$(call TAG_VALUE,ComparisonAccount), \"8.ComparisonStackSetName\":$(call TAG_VALUE,ComparisonStackSetName), \"9.GracePeriod\":$(call TAG_VALUE,GracePeriod)}" --stack-set-name) | jq -s -c 'sort_by(."1.Name")' | python3 json_table.py StackSets

stack-set-instances:
	$(LIST_STACK_SETS_COMMAND) | (xargs -n 1 -P 15 aws cloudformation list-stack-instances --query "Summaries.{\"1.ID\":[0].StackSetId,\"2.Current\":join(', ', [?Status=='CURRENT'].join('/', [Account, Region])), \"3.Other\":join(', ', [?Status!='CURRENT'].join('/', [Account, Region]))}" --stack-set-name) | sed 's/:[a-z0-9][a-z0-9-]*//g' | jq -s -c 'sort_by(."1.ID")' | python3 json_table.py StackSetInstances


test:
	py.test --cov-branch --cov-report html --cov-report term-missing ./

shell:
	docker-compose build aws-baseline
	docker-compose run aws-baseline bash