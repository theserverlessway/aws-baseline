# Service Control Policies

Service control policies can deny actions across the whole organization, specific Organizational Units or accounts in the Organization. Actions in the Main Account are not impacted by any SCPs though.

The Custom CloudFormation Resource in this folder has tasks to deploy and update service control policies. Formica lists all files in the `global-policies` and `custom-policies` folder that end in `.scp.json` and deploys them as a custom resource. The part before `.scp.json` will be used as the name of the Policy.



## Global Policies  

All policy files in the `global-policies` file are created deployed and attached to the Root of the Organization. This makes sure there is no additional management and no possibility of forgetting any stepo in default policies.

Those Service Control Policies deny access to resources created throught StackSets and limit dangerous actions across all subaccounts.

## Custom Policies

All policies in the `custom-policies` folder are deployed as well, but not attached to anything in the Organization. They have to be manually attached afterwards. This makes it easy to create and deploy these policies without having
to manage the process yourself.

## Working with Policies

To get a list of currently deployed policies and where they are attached run the following commands:

```bash
make policies
make policy-attachments
```

SCPs are implemented following AWS Control Tower and other ideas and requirements. You can see all the Control Tower GuardRails in their [documentation](https://docs.aws.amazon.com/controltower/latest/userguide/guardrails.html)

# API Resource Access Management

To make sure specific resources can't be removed by accident or through an attack we need to limit the availability of certain actions. Beyond implementing Termination Protection for CloudFormation stacks we're adding Stack Policies to Stacks and Service Control Policies Organization wide.

## Termination Protection 

Termination protection on AWS makes sure that we can't accidentally remove a stack. The termination protection would have to be removed first before the stack can be deleted. As normal developers don't have access to the Action to update the termination protection this adds an additional security check that Admins need to do.

The Makefile in this folder has tasks to manage termination protection:

```bash
make enable-termination-protection STACK=somestack
make disable-termination-protection STACK=somestack
make enable-all-termination-protections
make disable-all-termination-protections
```

To list all current termination protections per stack there is an additional task:

```bash
make termination-protections
```


## Stack Policies

With Stack Policies you can configure which resources in a stack can be updated or replaced or which actions are denied. This is especially important for any datastores, for example denying any replacements of a DBInstance or DBCluster. The stack policy, like the termination protection, can only be set by admins and not updated by a developer. This adds an additional layer to make sure no data can be removed accidentally.

If a stack doesn't have a stack policy set there is an implicit AllowAll policy in place. Once set a stack policy can't be removed, it can just be updated (for example to AllowAll).

The Makefile in this folder has tasks to manage stack policies:

```bash
make set-stack-policy Stack=SomeStack Policy=stack-policies/allow-all.policy.json
make set-all-stack-policies Stack=SomeStack Policy=stack-policies/allow-all.policy.json
```

To get the current stack policy there is a command as well:

```bash
make stack-policy Stack=toolbox-service
aws cloudformation get-stack-policy --stack-name toolbox-service --query StackPolicyBody --output text
{
  "Statement" : [
    {
      "Effect" : "Allow",
      "Action" : "Update:*",
      "Principal": "*",
      "Resource" : "*"
    }
  ]
}
```