# Rolling Out the AWS Baseline

Rolling out the Baseline into AWS can be done fully automated through the `make rollout` command. Before running the Rollout there are a few things to consider.

## Storing your customisations

It is highly recommended that you fork this repository and commit all chagnes you're doing to the infrastructure to your own repository. This will make sure that you can redeploy your infrastructure easily anytime and selectively update the Baseline from upstream.

## Single Main Account or Split Management Accounts

When deciding on your Account Setup one thing to consider is if you want to have a single Main Account managing all others or if you want to split up your Accounts into separate Logging, Security or other Management Accounts.

The advantage of a single Main Account is that it makes the whole infrastructure easier to understand and use. All configuration and deployment metadata is stored in one account, so tight security over that one Account is easier to implement and understand for most teams. As the Main Account in the Org is also the only one that can access the list of Sub Accounts it's easier to automate various deployments as AccountIDs don't have to be hardcoded.

The downsides in this approach are the limits in scale this provides as any sufficiently large organization with dozens of accounts will potentially run into issues with one main account. Different teams will want to be able to have more control over their Accounts, e.g. the Security team might want to be able to have more control over a dedicated Security Account which is organizationally harder to do with one Main Account. Service Control Policies also don't work in the Main Account of an Organization so limiting access thoroughly is harder to achieve.

For most organizations, especially those that only need a handful of accounts going with one central Account should be the best option as it limits complexity and needs no customization in this baseline. For companies that require (or already have) a more complex setup having multiple accounts dealing with the Baseline might be a good option.

In the end because the whole setup is fully automated switching from one mode to another can always be done, although with a varying amount of effort.

## Configuration to change when setting up multiple Management Accounts

In case you want to split your Main Account configuration to multiple accounts you need to make sure to set the appropriate configuration values in each StackSet to point to those Management accounts.

For example if you deploy the `auditing` stack into a separate logging account any CloudTrail, Config or VPC Flowlogs will need the `MainAccount` parameter in their respective StackSets to be set to the ID of the respective Management Account. You can find all those StackSets by searching for `main-account-parameter` and setting that parameter directly in the `stack.config.yaml` file. 

By default the `MainAccount` parameter in those StackSets will be set to the MainAccounId of the Organization which automates the process if you use a single Main Account.


## Configuring the Regions

The configuration files for each Stack and StackSet have us-east-1 hardcoded as the region to deploy into. This is done so that no individual stack can accidentally be deployed into the wrong region. If you do not want your Stacks or StackSets to be deployed into us-east-1 please change those values accordingly in each configuration file. While this is a manual effort and might be more automated in the future it removes some future problems with inconsistent configuration.

## Excluding Stacks or StackSets

If you want to exclude a Stack or StackSet from the automated rollout add the directory name into the `Excluded` file in the `main-account-stacks` or `stack-sets` directories. It has to be an exact match. Make sure to not add an empty line as it will interfere with grep. 

To check which directories are excluded run `make excluded` either in the main directory or the `main-account-stacks` or `stack-sets` directories.

## Required Tools

When using the toolbox all required tools are already installed. In case you do not want to or can't use the Docker container you need to install Formica with `pip install formica-cli` and make sure you have `make` installed on your System.

## Rolling out the Baseline

Now finally after we've made all the adjustments we need we can roll out the Baseline. Make sure you have local credentials that have Admin Access into your Main Account. If you're in the Toolbox Docker Container (start it with `make shell`) or have [`awsinfo`](https://theserverlessway.com/tools/awsinfo/) installed you can run `awsinfo me` and `awsinfo credentials` to see which User you're logged into and what the currently used credentials and region are.

After that run `make rollout` in the root folder of the repository. That task will switch into the `main-account-stacks` folder first and run `make rollout` there and deploy all stacks. After that it will switch into the `stack-sets` folder and deploy the StackSets. In case any issues come up during the deployment you can rerun `make rollout` again as it will update existing stacks in case they already exist.

## Updating the Baseline and Debugging issues

Whenever you want to update the baseline either by customising it or adding features from the upstream repository run `make rollout` again after updating repository.

In case there are ever errors when rolling out the Baseline open an issue (in case it's a bug) and look into [`Formica`](https://theserverlessway.com/tools/formica/) the underlying tool deploying all Stacks and StackSets of the Baseline.