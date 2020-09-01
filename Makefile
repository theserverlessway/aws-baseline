# Main Makefile

# This Makefile provides tasks to create accounts, roll out the Baseline and run security auditing tools to these
# accounts automatically. For detailed instructions on rolling out the Baseline check out docs/Rollout.md.
# To start the container including all tools run `make shell`.

# If this variable is set, run awsinfo through Docker Compose instead of directly
ifdef ComposeAwsinfo
AWSINFO=docker-compose run --rm awsinfo
else
AWSINFO=awsinfo
endif

# Prefix to run commands in the aws-baseline Docker Compose environment
BASELINE=docker-compose run --rm aws-baseline

## Account Creation

# Run with make create-account Name=ACCOUNT_NAME Email=ACCCOUNT_EMAIL
# Will wait until the Account is in Active State
create-account:
ifndef Email
	$(error Email is undefined)
endif
ifndef Name
	$(error Name is undefined)
endif
	aws organizations create-account --email $(Email) --account-name $(Name) --iam-user-access-to-billing ALLOW
	@sleep 5
	@echo "Waiting for Account creation to finish"
	@while [[ $$(aws organizations list-accounts --query "Accounts[?Name=='$(Name)'].Status" --output text) != 'ACTIVE' ]]; do (echo -n '.' && sleep 2) done
	@echo "Account $(Name) with Email $(Email) created successfully"

create-account-alias:
ifndef Alias
	$(error Alias is undefined)
endif
	aws iam create-account-alias --account-alias $(Alias)

list-accounts:
	$(AWSINFO) orgs

awsinfo:
ifndef Args
	$(error Args is undefined)
endif
	$(AWSINFO) $(Args)


## Baseline Rollout

rollout:
	cd main-account-stacks && make rollout
	cd stack-sets && make rollout

diff:
	@cd main-account-stacks && make diff
	@cd stack-sets && make diff

excluded:
	@cd main-account-stacks && make excluded -i
	@cd stack-sets && make excluded -i

## Development Tooling

test-python:
	py.test --cov-branch --cov-report html --cov-report term-missing ./

build:
	touch .bash_history
	docker-compose build --pull aws-baseline

rebuild-baseline:
	docker-compose build --pull --no-cache aws-baseline

shell: build
	$(BASELINE) bash

# For Windows users: run make targets and comnands through Docker Compose
# (Note that we cannot use the MAKE variable here as it points to make in the local environment not in the container)

compose-make: build
ifndef Args
	$(error Args is undefined)
endif
	$(BASELINE) make $(Args)

# Invoke this target before using ComposeAwsinfo=1
pull-awsinfo:
	docker-compose pull awsinfo

# Security Audit

security-audit-accounts:
ifndef Accounts
	$(error Accounts is undefined)
endif
	echo $(Accounts)
	docker-compose build aws-baseline
	$(BASELINE) ./scripts/security-audit -p $(Accounts)

clean-reports:
	rm -fr reports

security-audit-all: build clean-reports
	$(BASELINE) ./scripts/security-audit -p

security-audit-docker-with-rebuild: rebuild-baseline security-audit-all

# Delete Default VPC

delete-default-vpcs: build
	$(BASELINE) ./scripts/delete-default-vpc
