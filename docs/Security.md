# Note on Security

The account assume setup does its best to make sure escalating rights isn't possible. From providing various roles
to assume to providing [Permission Boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html) by default and MFA support. Those measures are only effective though if your team follows best practices by using MFA and not creating workarounds for Admin access in various accounts.

The stack also creates groups for user management so you can enable only the specific rights your users need, without having to resort to admin access for everyone. Make sure to limit the rights of each user and only add more in instances where that's necessary. Once a production issue for example is resolved you can remove the user again from Developer or Admin Access and give them ReadOnly. This ensures that nobody can even accidentally delete or impact resources in production.

## Region Limitation

Some of the Roles deployed into each sub-account are limited to specific regions. The Admin role and ReadOnly Roles are not limited to specific regions. You can use the `AllowedRegions` parameter in the `assumable-roles` StackSet to set the allowed regions. It's a comma separated list of regions that.

## Permissions Boundaries

All Roles created in sub-accounts are configured with a Permissions Boundary to limit access to specific resources and services. All access to CloudFormation stacks created through a StackSet is denied. Specific other services are denied as well, please check the StackSet documentation for more details.

One important Boundary that is set up is for roles created by developers in the sub-accounts. Any Role or user that gets created through a Baseline Role needs to have a Permissions Boundary set to a specific Boundary. This ensures that no rights escalation is possible, for example consider the following:

1. Attacker gets acces to sub-account credentials that are able to create new Roles or Users
2. She creates a new Role and sets the Permissions to Admin access
3. She switches into that new Role and has now escalated rights from the DeveloperRole she had, for example she can now work around the region limitation set up before.

To make sure this isn't possible every Role created needs to have its `PermissionsBoundary` set to the following(with appropriate AccountId):

```
arn:aws:iam::1234569789:policy/CreatedIdentitiesPermissionsBoundary
```

This PermissionsBoundary limits access to iam and other services for these roles and enforces the same Boundaries as the DeveloperRole has. For CloudFormation you could do the following:

```yaml
!Sub arn:aws:iam::${AWS::AccountId}:policy/CreatedIdentitiesPermissionsBoundary
```

Without this PermissionsBoundary set you can't create any new Roles or Users. If you want to disable this behaviour you can set `IAMPermissionBoundaryLimitation` to `false` in the `assumable-roles` StackSet. But be aware that this can be very dangerous and if credentials leak for any reason this can escalate rights. 

You can set the `DisabledIdentitiesServices` variable in the same StackSet to disable specific AWS services for any role created in the accounts. It will disable access to all actions of those services. A few services like `IAM` and `CloudTrail` are in the default list. Make sure to include those if you want to configure your own list as those don't get merged. After deployment check the policy to conform to the limitations you want to have in place.

## Service control policies

To really lock down your AWS Organization you should take a look at the available service control policies in the `service-control-policies` Stack in `main-account-stacks`. SCPs can limit specific actions organization wide so even if someone is able to escalate rights in a specific account they won't be able to delete CloudTrail for example.

This is another important step in securing your account even in cases of rights escalation. There are a number of default Policies being deployed and attached to the root of your Organization, but you can add your own custom policies easily. Those will not be automatically attached to make sure you're attaching them exactly where required.