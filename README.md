# AWS Account Baseline

This repository contains configuration to roll out your AWS Baseline (also known as a Landing Zone). The result will be a flexible setup to give you a basis to build your specific infrastructure on. The Baseline is implemented through a mix of CloudFormation Stacks and StackSets with individual parts being optional so you can decide the
setup of your infrastructure.

The `main-account-stacks` folder contains CloudFormation Stacks that should be deployed first into your main account. It
will set up roles and groups automatically for your existing accounts.

The `stack-sets` folder contains various StackSets that should be created in your main account and then deployed
into your member accounts. For more information on the StackSets check out the README in the `stack-sets` folder.

Various stacks are based on or derived from the wonderful [Widdix Templates](http://templates.cloudonaut.io/en/stable/). Check them out they do an amazing job!

## Note on Security

The account assume setup does its best to make sure escalating rights isn't possible. From providing various roles
to assume to providing [Permission Boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html) by default and MFA support. Those measures are only effective though if your team follows best practices by using MFA and not creating workarounds for Admin access in various accounts.

The stack also creates groups for user management so you can enable only the specific rights your users need, without having to resort to admin access for everyone. Make sure to limit the rights of each user and only add more in instances where thats necessary and for a short time.

### Service control policies

To really lock down your AWS Organization you should take a look at the available service control policies in the `scp` subfolder of `main-account-stacks`. SCPs can limit specific actions organization wide so even if someone is able to escalate rights in a specific account they won't be able to delete CloudTrail for example.

This is another important step in securing your account even in cases of rights escalation.

### Auditing

The Stacks and StackSets deployed to both the main and sub accounts set up a best practice auditing solution. That
includes CloudTrail, Config and GuardDuty across all accounts and regions.

Make sure to familiarize yourself with the specific services so you have a good understanding of the auditing setup and understand how to detect issues in your Organization. 

## User and Access Management

In the main account we're creating several `assume-role` groups which allow users to assume roles in subaccounts.
They are created automatically for any account found in the current organization. When you add new accounts you
have to redeploy the stack so it picks up the new accounts and creates groups accordingly. For more information on assuming roles in another account check out the [Assume Role Documentation](./docs/ASSUME.md)

The stacks in the main account also create various groups for User Management. This allows you to add new users to
groups to for example create new users or manage group membership. For more information on User Management check out the [User Managemend Documentation](./docs/USER_MANAGEMENT.md)

Check out the [main-account-stacks README](./main-account-stacks/README.md) for more detail on each stack that gets deployed to the main AWS account.

## Necessary Tools

* Formica: [https://theserverlessway.com/tools/formica/](https://theserverlessway.com/tools/formica/)
* Awsie: [https://theserverlessway.com/tools/awsie/](https://theserverlessway.com/tools/awsie/)

## Recommended Tools:
* AWSInfo: [https://theserverlessway.com/tools/awsinfo/](https://theserverlessway.com/tools/awsinfo/)


## Security Audit

The Makefile in the root of the repository has a `security-audit` task that will run a full audit on all of your accounts. It uses [Prowler](https://github.com/toniblyx/prowler) and [ScoutSuite](https://github.com/nccgroup/ScoutSuite) to audit the accounts. Make sure those tools are installed on your system.

When you run the audit make sure that your current credentials are MFA signed, so use `awsinfo assume token -md 8` and export the given variables before calling the command.

If you only want to run the audit against a specific account, you can run the script directly with `./scripts/security-audit ACCOUNT_ID`.

By default the `AssumableSecurityAuditRole` is assumed and used. If you want to use a different role, set it with the `-r` parameter. If you want to run the audits in parallel use the `-p` option. [Gnu Parallel](https://www.gnu.org/software/parallel/) needs to be installed on your system in that case. For the Prowler reports you also need [`ansi2html`](https://pypi.org/project/ansi2html/) and `sed` installed on your System.

The reports are stored in the reports folder, with separate folders for each audit tool.

The Audit will take quite a long time (even if run in parallel mode).