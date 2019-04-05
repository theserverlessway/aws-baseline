.PHONY: stack-sets


new:
	formica new -c stack.config.yaml
	formica deploy -c stack.config.yaml

create-account:
ifndef Email
	$(error Email is undefined)
endif

ifndef Name
	$(error Name is undefined)
endif
#	aws organizations create-account --email $(Email) --account-name $(Name)
	@echo "Waiting for Account creation to finish"
	@while [[ $$(aws organizations list-accounts --query "Accounts[?Name=='$(Name)'].Status" --output text) != 'ACTIVE' ]]; do (echo -n '.' && sleep 2) done
	@echo "Account $(Name) with Email $(Email) created successfully"


create-account-alias:
ifndef Alias
	$(error Alias is undefined)
endif
	aws iam create-account-alias --account-alias $(Alias)



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

TAG_VALUE=Tags[?Key=='$(1)'].Value|[0]||''

stack-sets:
	 $(LIST_STACK_SETS_COMMAND) | (xargs -n 1 -P 15 aws cloudformation describe-stack-set --query "StackSet.{\"1.Name\":StackSetName, \"2.Tags\":join(', ', Tags[].join('=', [Key,Value]))}" --stack-set-name) | jq -s -c 'sort_by(."1.Name")' | python3 json_table.py StackSets

stack-set-instances:
	$(LIST_STACK_SETS_COMMAND) | (xargs -n 1 -P 15 aws cloudformation list-stack-instances --query "Summaries.{\"1.ID\":[0].StackSetId,\"2.Current\":[?Status=='CURRENT'] | length(@), \"3.Other\":[?Status!='CURRENT'] | length(@)}" --stack-set-name) | sed 's/:[a-z0-9][a-z0-9-]*//g' | jq -s -c 'sort_by(."1.ID")' | python3 json_table.py StackSetInstances


test-python:
	py.test --cov-branch --cov-report html --cov-report term-missing ./

shell:
	docker-compose build aws-baseline
	docker-compose run aws-baseline bash

diff-stack-sets:
	@ls stack-sets | xargs -n 1 -I {} bash -c "echo '{} ----------------------------------' && cd stack-sets/{} && formica stack-set diff -c stack-set.config.yaml && echo -e '\n\n'"

diff-stacks:
	@ls main-account-stacks | xargs -n 1 -I {} bash -c "echo '{} ----------------------------------' && cd main-account-stacks/{} && formica diff -c stack.config.yaml && echo -e '\n\n'"