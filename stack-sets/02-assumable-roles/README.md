# Assumable Roles in Sub Accounts

This StackSet deploys a set of Roles that can be assumed from the main account if the user is part of the group that has the rights to assume this role.

* `AssumableAdminRole` that has full admin access in the member account.
* `AssumableDeveloperRole` that has read-only on all services except cloudformation where it has write access. It can also pass the `cloudformation` role when creating or updating a stack. It is limited by a PermissionsBoundary to the `AllowedRegions`.
* `AssumableCloudformationDeveloperRole` A Role that is only allowed to deploy Cloudformation stacks and pass the CloudformationRole. It is limited by a PermissionsBoundary to the `AllowedRegions`.
* `AssumableReadOnlyRole` has the AWS ReadOnly Managed Policy attached and provides ReadOnly Access to all regions.
* `AssumableSecurityAuditRole` has the AWS Security Audit Managed Policy attached in addition to a few extra rights that allow Security Audits with tools like Prowler and Scout.
* `AssumableOperationsRole` has access to CloudWatch Metrics and Logs in the `AllowedRegions`.

## Allowed Regions

Through the `AllowedRegions` parameter you can set the Regions that are accessible in the account. The parameter has to be a list of comma separated region names. 

## Permissions Boundary

The Admin and Developer Roles are limited by Permissions Boundaries to not be able to alter the basic Role Setup. Access to Stacks created through StackSets and Roles created by the StackSets are Denied.

## CloudFormation Role

`CloudformationRole` has full admin access, but can't be directly assumed. It has to be used to pass it to CloudFormation when creating or changing a stack so a `user` can actually create resources. This makes sure changes are only done through CloudFormation.
