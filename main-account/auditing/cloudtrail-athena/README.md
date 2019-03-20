# Athena Log Search

The AWS Landing Zone deployed into the HSE AWS account saves all CloudTrail logs to a central logging bucket. To
make that data searchable we're using Athena across all the log files. This allows us to search through
CloudTrail logs of all AWS accounts at once for security review and auditing.

Athena works by using metadata tables defined in the AWS Glue Data Catalog and matches them against files it finds
in the S3 buckets. On top of those metadata tables SQL queries can be run against the S3 data. Depending on the Query
it can take a few minutes to run against the full datastore as each individual file is read and queried.

## Athena and Glue

The integration between Athena and Glue allows for automated crawling of data in S3 buckets and creating
table definitions from that data. We tried Glue crawlers at first for defining the table metadata, but due
to issues with Athena and the crawled metadata we decided to create the tables directly through CloudFormation.

## Querying the data

Athena uses standard SQL to query the data stored in S3. Athena uses (Presto)[https://prestosql.io] under the
hood so for specific query details please check the Presto documentation. Following is an example that
shows you how to query the cloudtrail table in the logging database.

To run the Query go to the Athena console and either select a pre-defined query or add it in the query
editor there. On the left of the Dashboard you can see the exact table definition you can use for your query.
It combines all the data available in Cloudtrail.


```sql
SELECT *
FROM logging.cloudtrail
WHERE eventtype != 'AwsServiceEvent'
        AND useridentity.type = 'Root'
        AND eventtime > cast((now() - interval '30' day) AS varchar)
        AND useridentity.invokedby is NULL;
```

Presto supports date types, counts, limits and many other SQL features.

## Named Queries

To provide examples of queries that can be run against the data stored in S3 we provide named queries
for common use cases. Those can be run from the Athena Dashboard. Those queries are standard
SQL and deployed through CloudFormation. To add further queries check out the `queries.template.yaml` and
accompanying query sql file in the `queries` subfolder.

### Current Named queries:

* Root Login in last 30 days
