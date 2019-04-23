LIST_STACK_SETS_COMMAND=@aws cloudformation list-stack-sets --status ACTIVE --query "Summaries[].StackSetName" --output text

TAG_VALUE=Tags[?Key=='$(1)'].Value|[0]||''

stack-sets:
	 $(LIST_STACK_SETS_COMMAND) | (xargs -n 1 -P 15 aws cloudformation describe-stack-set --query "StackSet.{\"1.Name\":StackSetName, \"2.Tags\":join(', ', Tags[].join('=', [Key,Value]))}" --stack-set-name) | jq -s -c 'sort_by(."1.Name")' | python3 ../scripts/json_table.py StackSets

stack-set-instances:
	$(LIST_STACK_SETS_COMMAND) | (xargs -n 1 -P 15 aws cloudformation list-stack-instances --query "Summaries.{\"1.ID\":[0].StackSetId,\"2.Current\":[?Status=='CURRENT'] | length(@), \"3.Other\":[?Status!='CURRENT'] | length(@)}" --stack-set-name) | sed 's/:[a-z0-9][a-z0-9-]*//g' | jq -s -c 'sort_by(."1.ID")' | python3 ../scripts/json_table.py StackSetInstances


diff-stack-sets:
	@ls -d */ | xargs -n 1 -I {} bash -c "echo '{} ----------------------------------' && cd {} && formica stack-set diff -c stack-set.config.yaml && echo -e '\n\n'"

add-stack-set-instances:
	@ls -d */ | xargs -n 1 -I {} bash -c "echo '{} ----------------------------------' && cd {} && formica stack-set add-instances -c stack-set.config.yaml && echo -e '\n\n'"

update-stack-sets:
	@ls -d */ | xargs -n 1 -I {} bash -c "echo '{} ----------------------------------' && cd {} && formica stack-set add-instances -c stack-set.config.yaml && echo -e '\n\n'"