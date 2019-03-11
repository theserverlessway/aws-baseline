# AWS Account Baseline

This repository contains configuration to roll out your AWS Baseline (also known as a Landing Zone). The result will be a flexible setup to give you a basis to build your specific infrastructure on. 

The baseline is implemented through a mix of CloudFormation Stacks and StackSets. This leads to a flexible setup allowing you to choose specific StackSets to be rolled out across accounts, or not. 

The `main-account` folder contains a CloudFormation stack that should be deployed first into your main account. It
will set up roles and groups automatically for your existing accounts.

The `stack-sets` folder contains various stack-sets that should be created in your main account and then deployed
into your member accounts. For more information check out the README in the `stack-sets` folder.

Various stacks (e.g. basic and vpc) are based on the wonderful [Widdix Templates](http://templates.cloudonaut.io/en/stable/). Check them out they do an amazing job!

## Note on Security

The account assume setup is not considered to be a completely secure setup to shield your users from being able to escalate rights.
A user that doesn't have admin access could still create new IAM users or groups that allow them to escalate rights. This should
be considered as a setup for non-malicious users where you simply want to make sure proper procedures are followed with CloudFormation.

AWS also provides [Permission Boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html) to
completely limit what users are able to do, even if they can create new IAM entities. If you want to completely shield access you can either user Organisation Policies or edit the `cloudformation` role to not allow IAM access for example or introduce Permissions Boundaries.

## Main Account

In the main account we're creating several `assume-role` groups which allow users to assume the admin role in another account. Additionally we're creating an admin group for the main account and all users for this specific account.

### User and Group Configuration

You can start from the `stack.config.example.yaml` and copy it over to for example `stack.config.yaml`. This makes it easier
to later pull updates from this repository into your own without merge issues.

In the `stack.config.yaml` file in the `main-account` repo you can define the users and groups you want to create
through CloudFormation. Following is an example setup:

```
stack: assume-role-users-groups
capabilities:
  - CAPABILITY_NAMED_IAM
vars:
  assume:
    development: 123456789
  users:
    fmotlik:
      - admin
      - development-admin
    gwashington:
      - development-admin
    htruman:
      - development
```


We're defining the development account with its account id. From that definition the stack will have 3 groups:

* `development` allows to assume the `user` role in the development account
* `development-admin` allows to assume the `admin` and `user` role in the development account
* `admin` allows for admin access in the main account we're deploying this stack into


The next configuration are the users and which groups they belong to. It will create the users and their group memberships
through CloudFormation as well. In the above example `fmotlik` is admin on the main account and the development account,
`gwashington` is admin in the development account and `htruman` has only read and cloudformation access in the `development`
account.

To remove a user just remove them from the stack config file and redeploy the stack.

### Creating Account Keys for Users

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

### Create Account Login for a User

For users to be able to log into the AWS Console you have to create a Login Profile. Use the aws cli for creating
that profile and setting the password of a user:

```
aws iam create-login-profile --user-name fmotlik --password "ABCDEFGHIJKL"
```

## Member Accounts

Deploy a CloudFormation Stack that creates roles that can be assumed from the main account. The Member Account stack has a MFA Parameter that is set to true by default and will require MFA on every account that wants to assume the role.

The member account creates two roles:

* `admin` that has full admin access in the member account
* `user` that has read-only on all services except cloudformation where it has write access. It can also pass the `cloudformation` role when creating or updating a stack
* `cloudformation` has full admin access, but can't be directly assumed. It has to be used to pass it to CloudFormation when creating or changing a stack so a `user` can
actually create resources. This makes sure changes are only done through CloudFormation.

The Makefile also contains commands to remove the Role created automatically by AWS so you can only assume a role in the member account that was created by your stack.

## VPC

Deploy a VPC with a private and public subnet to a region in your account.

## Necessary Tools

* Formica
