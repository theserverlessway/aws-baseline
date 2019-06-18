SELECT *
FROM "${AuditingGlueDatabase}"."${CloudTrailTable}"
WHERE eventName='AssumeRoleWithSAML'
and requestparameters LIKE '%role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_AdministratorAccess%'
AND eventtime > cast((now() - interval '30' day) AS varchar);