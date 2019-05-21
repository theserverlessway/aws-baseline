# AWS Baseline

An effective AWS Baseline (or Landing Zone) needs to provide a team with a strong security setup, but without impacting productivity negatively. To that end the account baseline sets up the following elements:

## Multi Account Setup

To use AWS effectively and in a secure way a multi-account setup is necessary. Different environments, for example development, staging and production infrastructure, should be put into separate accounts 

## User Management

User Management is handled in a centralized way through the Master account. Users are created by dedicated admins that are allowed to create them with specific limits through permissions boundaries.

To log into sub-accounts users assume into roles


# Master Account Setup

* `Baseline:` Account setup with password policies
* `Assumable Roles & Groups:` Separate roles for various use cases in every AWS Account assumable through groups in the master account
* `Auditing:` CloudTrail, Config and FlowLog Buckets in the master account to push data from subaccounts
  * Centralized AWS Config Aggregator 
* `Athena CloudTrail Search:` AWS Athena Setup to search through historic cloudTrail logs  
* `GuardDuty Master:` Guardduty Master in every region of the MasterAccount to centralize from all subaccounts
* `Disabled Regions:` AWS Config Rule to check for disabled regions
* `Budget:` Budget Alerting when costs are over a certain limit
* `Alerting and Notifications:` SNS Topics for different alerting levels
* `Service Control Policies:` Configure accessible services and actions organization wide
  * Disable Deletion of AWS Config Data
  * Disable Deletion of CloudTrail
  * Disable Deletion of GuardDuty
  * Disable Deletion of Cross Account Access Role
* `Validation of StackSet Deployments:`
  * Validates that all StackSets and StackSet instances are properly deployed into Subaccounts

# Sub Accounts
* `Roles for different use cases`:
  * `Developer Role:` ReadOnly role that only allows to work with CloudFormation
  * `CloudFormation Role`: Role to deploy any CloudFormation infrastructure
  * `Operations Role:` CloudWatch access for metrics and operations dashboard review
  * `SecurityAudit:` ReadOnly with additions for Security Auditing
  * `Admin`: Full Admin Role in the Subaccount
 * `VPC`: Template for setting up VPCs
  * Private and Public Subnets
  * Optional Network LoadBalancers
  * FlowLogs stored centrally to master account
 * `GuardDuty Membership:` Report GuardDuty findings centrally
 * `CloudTrail:` CloudTrail enabled and reporting to centralized bucket
 * `Config:` Config enabled and Centralized reporting to master account bucket
   * `Default Config Rules:` S3 Bucket not publicly writeable/readable
 
 
 https://aws.amazon.com/solutions/aws-landing-zone/
