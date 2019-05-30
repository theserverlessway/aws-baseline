ACCOUNT_ID=$(shell aws sts get-caller-identity --output text --query Account)

accounts-config:
	aws organizations list-accounts --output json --query "Accounts[?Id!='$(ACCOUNT_ID)'].{Id: Id, Email: Email}" | jq '{"vars": {"Accounts": .}}' > accounts.config.json
