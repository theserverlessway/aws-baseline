SELECT *
FROM "${CloudTrailDatabase}"."${CloudTrailTable}"
WHERE eventtype != 'AwsServiceEvent'
        AND useridentity.type = 'Root'
        AND eventtime > cast((now() - interval '30' day) AS varchar)
        AND useridentity.invokedby is NULL;
