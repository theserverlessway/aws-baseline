# User and Group Management

To be able to create new users an account needs to be in the `UserManagement` group. Then they can create new users and send developers their username and password. There is a `GroupManagement` group that gives an account the rights to add and remove people from specific groups (which the same people will typically be part of as well).

When creating a new user make sure you don't force them to change their password on first login. The baseline setup only allows changing a users password if they have MFA enabled and thus will block access to changing a password on first login.

As the default password policy forces someone to change their password regularly and requires MFA for almost every action the security is not compromised through this setup. Make sure to validate a user has set up MFA themselves before adding them to any other groups so they can access other accounts.

After creating a new user you should add them to the following groups so they are able to set up their own MFA and change their password:

* UserCredentialsManagement

With the `UserCredentialsManagement` group attached users are able to set up MFA, change their password and create keys for api access. Generally as an Admin you shouldn't need to set up any of this yourself, but if necessary following are commands to create keys and login profiles for a user. 

Once a user has set up MFA make sure they log out and back into their account again. Otherwise their current credentials aren't MFA secured and they won't be allowed to perform any actions.

## Sub Account Access Management

A separate group is created for every assumable role in every account. So if we have 6 roles and 3 subaccounts 18 different groups will be created.

For a user to be able to assume a specific role in a subaccount add them to the group representing that role. The groups start with an `Assume` prefix and then list the role, the account name and account id. This should make sure that no user is accidentally put into a group and account access they shouldn't have. After adding them to the Group the users will have the right to `sts:AssumeRole` a specific role in the subaccounts.

As an IAM User can only be part of 10 Groups you might want to remove and add users to specific groups in situations where thats necessary if you ecceed that limit.
