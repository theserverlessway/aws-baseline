# VPC Stack and StackSet

This directory contains a CloudFormation Stack that can be deployed with CloudFormation directly or as a StackSet.

You can set the number of Subnets and NAT Gateways and define exact CIDRS for your VPC. It's even possible to configure separate CIDR per Account and Region in case you want to Peer them or use a Transit Gateway.

The Stack and StackSet exports various Values to CloudFormation exports to be used in other stacks. If you want to deploy several stacks set the `ExportsPrefix` parameter so the stack can be deployed multiple times into the same region.

## Number of Subnets

The `AvailabilityZones` variable is used to set the number of of Subnets. By default it is set to 3, meaning 6 Subnets will be deployed, a private and a public one for each AZ.

## Default CIDR

The VPC Stack has uses the following parameters to configure your VPC CIDR:

`ClassA.ClassB.ClassC.ClassD/CIDRSuffix`

This allows you be specific in your CIDR Setup. To configure how the VPC is split up into Subnets it uses the `CIDRSubnetBits` parameter. It defines the number of bits used for each subnet IPs. To create the CIDR the [`FN::CIDR` function of CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-cidr.html) is used. 

Following is an example for the default VPC:

```
ClassA: 10
ClassB: 0
ClassC: 0
ClassD: 0
CIDRSuffix: 16
CIDRSubnetBits: 12
```

Which creates the following CIDR and Subnets with 4091 available IPs per Subnet:

```
VPC CIDR: 10.0.0.0/16
SubnetAPrivate: 10.0.0.0/20
SubnetAPublic: 10.0.16.0/20
SubnetBPrivate: 10.0.32.0/20
SubnetBPublic: 10.0.48.0/20
SubnetCPrivate: 10.0.64.0/20
SubnetCPublic: 10.0.80.0/20
```

This setup allows for up to 8 Availability Zones.

### Account and Region specific CIDR

If you want to set specific CIDRs per Account/Region you can set the `AccountCIDR` variable in the stack.config.yaml file:

```yaml
  AccountCIDR:
    123456789:
      "us-east-1": 11.0.0.0/16
```

This is especially helpful if you want to create different CIDRs for peered VPCs.

## NAT Gateways

By default no Nat Gateway is deployed so your instances can't access the public internet. You can set the `PrivateNatGateway` parameter to `single` or `all` to deploy a Nat Gateway into either a single AZ or all AZs you deploy Subnets into. The advantage of deploying into `all` is that in case of an outage of a region your instances still have internet access. It is quite a bit more expensive though.

## Interface and Gateway Endpoints

The `GatewayEndpoints` and `InterfaceEndpoints` variables allow you to create Endpoints for various AWS Services. You just need to add the Service name and they will be set up for you. Don't add the whole name, just the service name, e.g. `logs` instead of `com.amazonaws.us-east-1.logs`

The following example adds endpints used for running ECS Fargate and S3 workloads.:

```yaml
vars:
  GatewayEndpoints:
    - s3
  InterfaceEndpoints:
    - monitoring
    - logs
    - ecs
    - ecs-agent
    - ecs-telemetry
    - ecr.dkr
    - ecr.api
```