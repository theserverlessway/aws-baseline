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


rollout:
	cd main-account-stacks && make rollout
	cd stack-sets && make rollout

diff:
	cd main-account-stacks && make diff
	cd stack-sets && make diff

list-accounts:
	awsinfo orgs

test-python:
	py.test --cov-branch --cov-report html --cov-report term-missing ./

build:
	docker-compose build --pull aws-baseline

rebuild-baseline:
	docker-compose build --pull --no-cache aws-baseline

shell: build
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

security-audit-accounts:
ifndef Accounts
	$(error Accounts is undefined)
endif
	echo $(Accounts)
	docker-compose build aws-baseline
	docker-compose run aws-baseline ./scripts/security-audit -p $(Accounts)


security-audit-all: build
	rm -fr reports
	mkdir reports
	docker-compose run aws-baseline ./scripts/security-audit -p

security-audit-docker-with-rebuild: rebuild-baseline security-audit-all

delete-default-vpcs: build
	docker-compose run aws-baseline ./scripts/delete-default-vpc
