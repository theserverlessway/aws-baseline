# User and Group Management

To be able to create new users an account needs to be in the `UserManagement` group. Then they can create new users and send developers their username and password. There are other groups for group management (which the same people will typically be part of as well).

When creating a new user make sure you don't force them to change their password on first login. The baseline setup only allows changing a users password if they have MFA enabled and thus will block access to changing a password on first login.

As the default password policy forces someone to change their password regularly and requires MFA for almost every action the security is not compromised through this setup. Make sure to validate a user has set up MFA themselves before adding them to any other groups so they can access subaccounts.

After creating a new user you should add them to the following groups so they are able to set up their own MFA and change their password:

* UserCredentialsManagement

With the `UserCredentialsManagement` group attached users are able to set up MFA, change their password and create keys for api access. Generally as an Admin you shouldn't need to set up any of this yourself, but if necessary following are commands to create keys and login profiles for a user. 

## Creating Account Keys for Users

To create an `AWS Access Key` and `Secret Access Key` for a user use the awscli in the main account (you have to be admin to do this):

```
aws iam create-access-key --user-name fmotlik
{
    "AccessKey": {
        "UserName": "fmotlik",
        "AccessKeyId": "ABCDEFGHIJKLMNOPQRS",
        "Status": "Active",
        "SecretAccessKey": "sJ7asH8+j0jasdpJE3UKA96dKO3gK7fFH3ljgyGT96Klk",
        "CreateDate": "2017-12-22T08:38:28.456Z"
    }
}
```

You can list the access key ids for a user:

```
aws iam list-access-keys --user-name fmotlik
```

or also delete a key:

```
aws iam delete-access-key --user-name fmotlik --access-key-id AKIAJIZBOEG4ZO4MZC2A
```

## Create Account Login for a User

For users to be able to log into the AWS Console you have to create a Login Profile. Use the aws cli for creating
that profile and setting the password of a user. Users can of course do this themselves as well if they want to change the password and don't want to use the Console:

```
aws iam create-login-profile --user-name fmotlik --password "ABCDEFGHIJKL"
```

## Sub Account Access Management

A separate group is created for every assumable role in every subaccount. So if we have 6 roles and 3 subaccounts 18 different groups will be created.

For a user to be able to assume a specific role in a subaccount add them to the group representing that role. The groups start with an `Assume` prefix and then list the role, the account name and account id. This should make sure that no user is accidentally put into a group and account access they shouldn't have.

