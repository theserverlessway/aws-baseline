# Account Iteration Macro

CloudFormation has the ability to create Macros that allow you to run your template
through a Lambda function and return a new template. This allows for more dynamic
interaction when deploying a template.

This CloudFormation Stack provides a Macro to create specified Resources for
all SubAccounts in the Organization or all Accounts.

You can use the Macro through the `Transform` Keyword in your CloudFormation Template.

```
Transform: AccountIteration
```

If you want to Resources for the Master account as well add `WithMaster` at the end:

```
Transform: AccountIterationWithMaster
```

# Defining Resources

To define a resource that should be created for every Account Make sure to add
the term `ACCOUNT_ID` to your Resource LogicalId. The Macro will then create
a resource for every account and replace `ACCOUNT_ID`. The following Example
creates an S3 Bucket for every Account:

```
Transform: AccountIteration
Resources:
  SomeBucketACCOUNT_ID:
    Type: AWS::S3::Bucket
```

will transform into something like:

```
Transform: AccountIteration
Resources:
  SomeBucket123456789:
    Type: AWS::S3::Bucket
  SomeBucket987654321:
    Type: AWS::S3::Bucket
.....
```

If a Resource doesn't have `ACCOUNT_ID` in the name it will be simply copied over
to the resulting template.

You can also use the the following parameters anywhere in your resource

* ACCOUNT_ID
* ACCOUNT_NAME
* ACCOUNT_EMAIL

In the following example we're creating a role for every Account that can
only be assumed from that Account:

```
Transform: AccountIteration
Resources:
  VPCPeeringRoleACCOUNT_ID:
    Properties:
      RoleName: VPCPeeringRoleACCOUNT_ID
      AssumeRolePolicyDocument:
        Statement:
          - Action:
              - 'sts:AssumeRole'
            Effect: Allow
            Principal:
              AWS: ACCOUNT_ID
      Path: /
    Type: 'AWS::IAM::Role'
```
