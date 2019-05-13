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
	aws organizations create-account --email $(Email) --account-name $(Name)
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

test-python:
	py.test --cov-branch --cov-report html --cov-report term-missing ./

shell:
	docker-compose build aws-baseline
	docker-compose run aws-baseline bash

RSYNC=rsync -vlar --delete --exclude .git .idea ./ $(Target)

sync-dry-run:
ifndef Target
	$(error Target is undefined)
endif
	$(RSYNC) -n

sync:
ifndef Target
	$(error Target is undefined)
endif
	$(RSYNC)

security-audit:
	./scripts/security-audit -p

security-audit-docker:
	docker-compose run --detach aws-baseline ./scripts/security-audit -p