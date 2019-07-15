# Main Account Auditing Setup

This stack configures the central storage for Auditing on aws including:

* CloudTrail
* Config
* Flowlogs

For each of these services a bucket is created that includes the ID if the main account so sub-accounts can easily add that bucket as target for storing audit information.

Additionally it creates an Athena CloudTrail setup with example queries to search through all CloudTrail and FlowLogs logs in all accounts. The data is partitioned by `account`, `region` and `date` with date in `yyy-mm-dd` format.

Thanks to Cloudonaut for their [Athena Query Article](https://cloudonaut.io/analyzing-cloudtrail-with-athena/) and Alex Smolen for his [Athena Partitioning Article](https://medium.com/@alsmola/partitioning-cloudtrail-logs-in-athena-29add93ee070)


## Limiting Access to Specific Accounts

At the moment the buckets for CloudTrail, Config and FlowLogs are only limited to those services, but not to a specific account list or Organization. When your Organization has many accounts limiting the bucket policy to those specific accounts can increase the policy size beyond the max limit. Sometimes the time between deploying the policy and it becoming active has been seen as taking a few minutes.

Both those cases make it hard to limit access. In the future a fix has to be found, especially around `aws:PrincipalOrgID` in the condition section. At the time of this writing it is not yet clear if its possible to use the attribute in bucket policy conditions when allowing access to external AWS services.