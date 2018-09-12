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
