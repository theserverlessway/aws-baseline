SELECT *
FROM "${AuditingGlueDatabase}"."${CloudTrailTable}"
WHERE eventName='AssumeRoleWithSAML'
and requestparameters LIKE '%role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_AdministratorAccess%'
AND date > to_iso8601(now() - interval '30' day);