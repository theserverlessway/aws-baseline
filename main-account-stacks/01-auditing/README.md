# Main Account Auditing Setup

This stack configures the central storage for Auditing on aws including:

* CloudTrail
* Config
* Flowlogs

For each of these services a bucket is created that includes the ID if the main account so sub-accounts can easily
add that bucket as target for storing audit information.

Additionally it creates an Athena CloudTrail setup with example queries to search through all CloudTrail logs
in all accounts.