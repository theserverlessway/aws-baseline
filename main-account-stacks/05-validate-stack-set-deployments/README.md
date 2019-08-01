# Validate Stack Set Deployments Config Rule

When using StackSets one potential issue we have to resolve is adding new Accounts to the Organization, or AWS starting new Regions. Whenever that happens we want to make sure that the StackSets that should be in every account or every region are actually deployed.

This CloudFormation Stack creates an AWS Config Rule that will compare all StackSet Instances with Tags set on the StackSet. If they match it will set the StackSet as compliant. If its missing a StackSet it will set it as not compliant.

These Validation Config Rules should be deployed in every Account that manages StackSets, e.g. your Organizations Master Account or dedicated DevOps Accounts. This will make sure that all StackSets are properly up to date and their compliance is reported to the central AWS Config setup.

## Deploying the Config Rule

The AWS Config Rules to validate StackSets are deployed as a CloudFormation Stack.
The following command will create the stack, you can update and change it like any other Stack.

```
formica new -c stack.config.yaml
formica deploy -c stack.config.yaml
```

## Validating StackSet Instances are deployed successfully

You can use the following tags on a StackSet to configure the Accounts
and Regions it should be deployed to. Some of them should only be set
as boolean, some can take a list of accounts or regions that are
split with `/` as separator. We can't use ',' as a separator as it isn't
allowed in tag values.

When using the `Excluded` tags it will compare them to an up to date
list of accounts and regions and exclude the one listed. This makes
sure that if regions or accounts are added those will be non-compliant
until you add a StackSet instance.

```
tags:
  ValidateAllAccounts: true
  ValidateAllSubAccounts: true
  ValidateAccounts: 123456789/098765432
  ValidateExcludedAccounts: 987654321

  ValidateAllRegions: true
  ValidateRegions: eu-central-1/eu-west-1
  ValidateExcludedRegions: eu-west-1/us-west-1
```

## Non Compliance of StackSet Instances

There are different ways StackSet Instances can become NON_COMPLIANT:

* A StackSet has `Accounts` and `Regions` configured but the StackSet isn't deployed to an Account/Region combination
* A StackSet has `Accounts` and `Regions` configured and the StackSet is deployed but not in `CURRENT` or `RUNNING` state
* A StackSet has `Accounts` and `Regions` configured but an Instance is deployed not matching those tag configurations
* A StackSet has no tags configured and an instance is not in `CURRENT` or `RUNNING` state

All other StackSet Instances will be added in COMPLIANT state to AWS Config.