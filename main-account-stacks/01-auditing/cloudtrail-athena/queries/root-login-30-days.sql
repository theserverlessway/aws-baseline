SELECT *
FROM "${AuditingGlueDatabase}"."${CloudTrailTable}"
WHERE eventtype != 'AwsServiceEvent'
        AND useridentity.type = 'Root'
        AND date > to_iso8601((now() - interval '30' day))
        AND useridentity.invokedby is NULL;
