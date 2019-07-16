# Stack Sets

The stack sets are deployed with [`formica`](https://theserverlessway.com/tools/formica/). To update all stacks and their deployed stack instances run `make rollout` . To manage StackSets individually go into the respective directory.

## Stack Set Summaries:

Following a short summary for each StackSet. For individual documentation on each StackSet please consult the `README.md` in each of the directories. 

* `01-stack-set-execution-role`: Role that allows Cloudformation to deploy StackSets.
* `02-assumable-roles`: Various Roles (Admin, Developer, Operations, ...) to assume from the main account.
* `03-password-policy`: Password Policy deployed into every Account
* `04-guardduty-main`: GuardDuty deployed to main account to invite SubAccounts
* `05-guardduty-member`: Guardduty deployed to member accounts accepting the invitation
* `06-auditing-configuration`: CloudTrail and Config configuration including writing to S3 Bucket in main accont
* `07-config-rules`: Default Config Rules and Rule to find Resources in unused regions
* `08-vpc`: Flexible VPC configuration


## Individual Updates
To update the template used by a StackSet run the `update` command`:

```bash
formica stack-set update -c stack-set.config.yaml
``` 

This will update all stack instances currently in use by the stack-set.

To add new instances run `add-instances`:

```bash
formica stack-set add-instances -c stack-set.config.yaml
``` 

To remove instances run `remove-instances`:

```bash
formica stack-set remove-instances -c stack-set.config.yaml
``` 

For a complete documentation of all available stack-set commands in formica check out the [`Commands Reference`](https://theserverlessway.com/tools/formica/commands/) and the [Working with Stack Sets documentation](https://theserverlessway.com/tools/formica/stack-sets/).


The Makefile in this folder also contains commands to diff and update all stack-sets and add-instances currently missing. With `make diff`, `make update` and `make add` accordingly you can go through all StackSets and deploy them. Please be careful when using these commands.

For individual documentation on each stack please consult the `README.md` in each of the stack directories.

## Execution Role

Before deploying other StackSets you need to deploy the `stack-set-execution-role` to make sure the role is available in each subaccount. Otherwise any further addition of stack instances will fail as it can't assume into the Subaccounts.

## Excluding StackSets

If you want to exclude a StackSet from the automated rollout add the directory name into the `Excluded` file. It has to be an exact match. Make sure to not add an empty line as it will interfere with grep. 

To check which directories are excluded run `make excluded`