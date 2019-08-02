update-all-scps:
	python deploy-policies.py

policies:
	aws organizations list-policies --filter SERVICE_CONTROL_POLICY

policy-attachments:
	@aws organizations list-policies --filter SERVICE_CONTROL_POLICY --output text --query 'Policies[].[Name, Id]' |	xargs -n 2 bash -c 'echo -e "\nPolicy Attachments for: $$0" && aws organizations list-targets-for-policy --policy-id $$1 --output table --query "sort_by(Targets,&Name)[].{Name:Name,TargetId:TargetId,Type:Type}"'

STACK_NAMES=aws cloudformation describe-stacks --query "Stacks[].[StackName,StackId]" --output text

enable-termination-protection:
ifndef Stack
	$(error Stack to enable termination protection on has to be set)
endif
	aws cloudformation update-termination-protection --enable-termination-protection --stack-name $(Stack)

disable-termination-protection:
ifndef Stack
	$(error Stack to enable termination protection on has to be set)
endif
	aws cloudformation update-termination-protection --no-enable-termination-protection --stack-name $(Stack)

enable-all-termination-protections:
	@$(STACK_NAMES) | xargs -n 2 bash -c 'echo Enabling Termination Protection for $$0 && aws cloudformation update-termination-protection --enable-termination-protection --stack-name $$1 && echo Update Successful'

disable-all-termination-protections:
	@$(STACK_NAMES) | xargs -n 2 bash -c 'echo Disabling Termination Protection for $$0 && aws cloudformation update-termination-protection --no-enable-termination-protection --stack-name $$1 && echo Update Successful'

termination-protections:
	@aws cloudformation describe-stacks --query "Stacks[].[StackName]" --output text | xargs -n 1 -I {} bash -c 'aws cloudformation describe-stacks --stack-name {} --output text --query "Stacks[].[StackName, EnableTerminationProtection]"'

set-stack-policy:
ifndef Stack
	$(error Stack for setting the Policy needs to be set)
endif
ifndef Policy
	$(error Policy needs to be set)
endif
	aws cloudformation set-stack-policy --stack-name $(Stack) --stack-policy-body file://$(Policy)

stack-policy:
ifndef Stack
	$(error Stack for setting the Policy needs to be set)
endif
	aws cloudformation get-stack-policy --stack-name $(Stack) --query StackPolicyBody --output text

set-all-stack-policies:
ifndef Policy
	$(error Policy needs to be set)
endif
	@$(STACK_NAMES) | xargs -n 2 bash -c 'echo Setting Stack Policy for $$0 && aws cloudformation set-stack-policy --stack-name  $$1 --stack-policy-body file://$(Policy)'
