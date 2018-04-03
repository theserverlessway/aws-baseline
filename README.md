# Account Setup

This repository contains the general Account Setup for the Organisation.
It contains several folders with CloudFormation stacks for different part of the Org.

* main-account: CloudFormation stack to set up the main organisation account
* basic: PasswordPolicy, CloudTrail and Config setup based on [Widdix Templates](http://templates.cloudonaut.io/en/stable/)
* sub-accounts: CloudFormation stack to deploy into sub-accounts to enable users in the main account to log into sub-accounts
* vpc: VPC stack that has to be deployed into every sub-account region that should be used

## Main Account

In the main account we're creating several `assume-role` groups which allow users to assume the admin role in another account.
Additionally we're creating an admin group for the main account and all users for this specific account.

### Adding Users

To add a new user go into the `main-account` folder and open the `stack.config.yaml` file. There you can add new users together
with the groups they are part of (and therefore can access specific accounts). Afterwards redeploy the stack with Formica.

To remove a user just remove them from the stack config file and redeploy the stack.

### Creating Account Keys for Users

To create an `AWS Access Key` and `Secret Access Key` for a user use the awscli:

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
aws iam delete-access-key --user-name fmotlik --access-key-id AKIAJIZBOEG4ZO4MZC2A --profile tellzme
```

### Create Account Login for a User

For users to be able to log into the AWS Console you have to create a Login Profile. Use the aws cli for creating
that profile and setting the password of a user:

```
aws iam create-login-profile --user-name fmotlik --password "ABCDEFGHIJKL"
```

## Sub Accounts

Deploy a CloudFormation Stack that creates a role that can be assumed from the main account. The Sub Account stack has a MFA Parameter
that is set to true by default and will require MFA on every account that wants to assume the role.

The Makefile also contains commands to remove the Role created automatically by AWS.

## VPC

Deploy a VPC with a private and public subnet to a region in your account.

## Deployment

```
formica new/change -c stack.config.yaml --profile tellzme
```

```
formica deploy -c stack.config.yaml --profile tellzme
```

## Necessary Tools

* Formica
