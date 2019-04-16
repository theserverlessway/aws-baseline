# Assumable Roles in Sub Accounts

This StackSet deploys a set of Roles that can be assume from the main account

* `AssumableAdminRole` that has full admin access in the member account
* `AssumableDeveloperRole` that has read-only on all services except cloudformation where it has write access. It can also pass the `cloudformation` role when creating or updating a stack
* `cloudformation` has full admin access, but can't be directly assumed. It has to be used to pass it to CloudFormation when creating or changing a stack so a `user` can actually create resources. This makes sure changes are only done through CloudFormation.
