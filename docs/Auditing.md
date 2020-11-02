# Auditing and Reviews

Auditing is an important part of every AWS Baseline. AWS provides various Services to Audit your Accounts. The Baseline includes setup for GuardDuty, AWS Config and Cloudtrail Storage as well as other tools to Audit your Account.

## Guard Duty and Config

By default every region of every Account has GuardDuty and Config Enabled.

* [`GuardDuty`](https://aws.amazon.com/guardduty/): Machine Learning on top of AWS CloudTrail and Flowlogs (among other future sources) that looks for suspicious patterns and reports them. E.g. IP Addresses from countries that haven't had API interactions before or port probes on public instances.
* [`Config`](https://aws.amazon.com/config/): Config stores Resource state (e.g. all configuration of an EC2 Instance or VPC) and compares them to a set of Rules defined for those Resources. In case those Resources don't conform it is marked as Non-Compliant. 
* [`CloudTrail`](https://aws.amazon.com/cloudtrail/): CloudTrail records all AWS API interactions and stores them for later evaluation. This can either be for security analysis or determining access patterns for limiting rights of specific resources. 
* [`VPC FlowLogs`](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html): Flowlogs captures information about the IP traffic going into and from your network interfaces in your VPC. It records which IP connected, which ports the connection went over, how many bytes were sent in a timeframe and more. This is helpful for both analysing issues and determining and analysing attacks on your infrastructure.  

### GuardDuty

As GuardDuty is a regional service it has to be enabled in each Region and in the main account there have to be invitations set up for all sub-accounts for every region. To achieve this we're deploying it as two separate StackSets, one into the main account and the other into sub-accounts.

Once this is rolled out you can see all the findings for a particular region in the main account GuardDuty console of that region.

### Config 

Config allows to aggregate evaluations across regions and accounts into a central location. The `auditing` stack in the main-account stacks sets up an aggregator accross all accounts, so depending into which region you deploy that stack, there you'll find the Aggregator.   

Some AWS Resources are considered [global resources](https://docs.aws.amazon.com/config/latest/developerguide/select-resources.html) and can therefore show up in any region. To prevent this duplication the Baseline uses a StackSet parameter `GlobalConfigRegion` in the `auditing` StackSet which allows you to set that global region which records these global resources.

## CloudTrail

CloudTrail is set up across your Organization and writes into a CloudWatch LogGroup in each account and region and into a central bucket for all accounts. This lets you analyse issues when logged into a specific account and region, but also lets you find and analyse issues across your whole Organization.

### Analyzing with Athena

Athena is a Service in AWS that lets you query data in S3 Buckets through SQL queries. This simplifies analytics across all API events in all accounts drastically, especially in high pressure moments like a potential attack on your infrastructure. It also partitionas your data anytime a new CloudTrail file gets written to the bucket, so you can use the `date` field to query against. For example the following query will create vastly different numbers:

* `Select count(*) from auditing.cloudtrail where date > '2019'`
* `Select count(*) from auditing.cloudtrail where date > '2019-07'`
* `Select count(*) from auditing.cloudtrail where date > '2019-07-23'`

The date format is `YYY-MM-DD` and its a simple string comparison so comparing with `>` or `<` or both is totally possible. This makes queries really fast, even over large data. 

The Baseline sets up Athena for the CloudTrail Bucket and adds a few queries for you to analyse your account and get started with more complex analysis. When you go to the `Athena Dashboard` and there to `Saved Queries` you will see the `RootLogin30Days` query. Click that and you'll be taken to the Query Editor where you can see and run the query.

Once you ran the query you'll get all details on the number of times someone logged into a root account in the last 30 days.

## FlowLogs

When you use the VPC StackSet (or deployed it as a CloudFormation stack directly) the FlowLogs are stored into a CloudWatch Log Group in that account and region and delivered into a central flowlogs bucket in the main account. To quickly analyse traffic across multiple accounts you can also use `Athena` as described above.

## Tool Based Security Audit

The Makefile in the root of the repository has a `security-audit-all` task that will run a full audit on all of your accounts. It uses [Prowler](https://github.com/toniblyx/prowler) and [ScoutSuite](https://github.com/nccgroup/ScoutSuite) to audit the accounts. The make commands will use Docker to create the container with all required tools and run the audit inside of that container. If you want to run the script directly on your system make sure those tools are installed on your system.

When you run the audit make sure that your current credentials are MFA signed, so use `awsinfo assume token -md 8` and export the given variables before calling the command. This limits the time credentials are valid to 1 hour because of chain assuming (assume token then assume role), so in case an audit of a single account takes longer and you need MFA you can use the `-m` and `-d` options. `-m` will ask for an MFA token when assuming a role which allows the limit to be increased with the `-d` option. Make sure you don't use credentials obtained through `awsinfo assume token` when using the `-d` option though, as it would be a chain assume and limit the max duration to 1 hour. 

If you only want to run the audit against a specific account, you can run the single account make command with `make security-audit-accounts Accounts=1234567898765` ir the script directly with `./scripts/security-audit ACCOUNT_ID`.

By default the `AssumableSecurityAuditRole` is assumed and used. If you want to use a different role, set it with the `-r` parameter. If you want to run the audits in parallel use the `-p` option. [Xargs] needs to be installed on your system in that case. For the Prowler reports you also need [`ansi2html`](https://pypi.org/project/ansi2html/) and `sed` installed on your System. For assuming the roles [`awsinfo`](https://theserverlessway.com/tools/awsinfo/) is used, make sure to install it.

The reports are stored in the reports folder, with separate folders for each audit tool. You can check the progress of the Audit in the reports files as logs are written into the reports folder. As it runs through all your accounts and collects a lot of data the Audit will take quite a long time (even if run in parallel mode).
