# AWS Baseline

An effective AWS Baseline (or Landing Zone) needs to provide a team with a strong security setup, but without impacting productivity negatively. To that end the account baseline sets up the following elements:

효과적인 AWS Baseline (또는 Landing Zone)은 팀에 강력한 보안 설정을 제공해야하지만 생산성에 부정적인 영향을주지 않아야합니다. 이를 위해 AWS Baseline 은 다음 요소를 설정합니다.

## Multi Account Setup

To use AWS effectively and in a secure way a multi-account setup is necessary. Different environments, for example development, staging and production infrastructure, should be put into separate accounts 

AWS를 효과적이고 안전한 방식으로 사용하려면 다중 계정 설정이 필요합니다. 개발, 스테이징 및 프로덕션 인프라와 같은 다양한 환경은 별도의 계정에 넣어야합니다.

## User Management

User Management is handled in a centralized way through the Master account. Users are created by dedicated admins that are allowed to create them with specific limits through permissions boundaries.

사용자 관리는 마스터 계정을 통해 중앙 집중식으로 처리됩니다. 사용자는 Permission Boundary 통해 특정 제한으로 만들 수있는 전담 관리자에 의해 생성됩니다.

To log into sub-accounts users assume into roles
사용자가 역할을 맡은 하위 계정에 로그인하려면 AWS Console에서는 역할 전환 메뉴에서 Account, Role 입력을 통해 위임받은 역할을 수행할 수 있고, AWS CLI 에서는 역할이 설정된 Profile 설정을 통해 임시 Credentials 을 얻을 수 있습니다. 


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
