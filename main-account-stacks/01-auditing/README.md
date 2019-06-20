# Main Account Auditing Setup

This stack configures the central storage for Auditing on aws including:

* CloudTrail
* Config
* Flowlogs

For each of these services a bucket is created that includes the ID if the main account so sub-accounts can easily add that bucket as target for storing audit information.

Additionally it creates an Athena CloudTrail setup with example queries to search through all CloudTrail and FlowLogs logs in all accounts. The data is partitioned by `account`, `region` and `date` with date in `yyy-mm-dd` format.

Thanks to Cloudonaut for their [Athena Query Article](https://cloudonaut.io/analyzing-cloudtrail-with-athena/) and Alex Smolen for his [Athena Partitioning Article](https://medium.com/@alsmola/partitioning-cloudtrail-logs-in-athena-29add93ee070)