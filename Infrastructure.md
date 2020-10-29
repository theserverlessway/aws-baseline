# AWS Baseline
효과적인 AWS Baseline (또는 Landing Zone)은 팀에 강력한 보안 설정을 제공해야하지만 생산성에 부정적인 영향을주지 않아야합니다. 이를 위해 AWS Baseline 은 다음 요소를 설정합니다.

## Multi Account Setup
AWS를 효과적이고 안전한 방식으로 사용하려면 다중 계정 설정이 필요합니다. 개발, 스테이징 및 프로덕션 인프라와 같은 다양한 환경은 별도의 계정에 넣어야합니다.

## User Management
사용자 관리는 마스터 계정을 통해 중앙 집중식으로 처리됩니다. 사용자는 Permission Boundary 통해 특정 제한으로 만들 수있는 전담 관리자에 의해 생성됩니다.

## To log into sub-accounts users assume into roles
사용자가 역할을 맡은 하위 계정에 로그인하려면 AWS Console에서는 역할 전환 메뉴에서 Account, Role 입력을 통해 위임받은 역할을 수행할 수 있고, AWS CLI 에서는 역할이 설정된 Profile 설정을 통해 임시 Credentials 을 얻을 수 있습니다. 

# Master Account Setup

* `Baseline:` Account setup with password policies
* `Assumable Roles & Groups:` 마스터 계정에서 IAM Group을 통해 위임받을 수 있는 다양한 Role을 UseCase에 따라 분리함 
* `Auditing:` Sub Account의 CloudTrail, Config, FlowLog를 마스터 계정에서 통합 로깅하기 위해 S3 Bucket 생성 
* `Athena CloudTrail Search:` CloudTrail과 FlowLog를 마스터 계정에서 빠르게 검색하기 위한 Athena 설정
* `GuardDuty Master:` 모든 Sub 계정의 GuardDuty 모니터링을 Master 계정에서 통합 모니터링 하기 위한 GuardDuty Master 설정
* `Disabled Regions:` 비활성화 Region에서 발생할 수 있는 보안상황을 체크하기 위한 AWS Config Rule 
* `Budget:` 예산 범위를 초과하는 경우, 알람을 통해 경고를 받을 수 있도록 설정 (CloudZ Portal 기능 이용 )
* `Alerting and Notifications:`  알람 레벨에 따라 SNS Topic으로 Noti 수신
* `Service Control Policies:` CloudZ Portal 제약으로 SCP 설정은 불가
  * Disable Deletion of AWS Config Data
  * Disable Deletion of CloudTrail
  * Disable Deletion of GuardDuty
  * Disable Deletion of Cross Account Access Role
* `Validation of StackSet Deployments:`
  * Sub계정에 StackSet이 적절하게 배포되었는지 검증 

# Sub Accounts
* `다양한 유즈케이스에 따라 Role을 생성하고 마스터 계정의 IAM User가 위임받을 수 있도록 Assumable Role 생성`:
  * `Developer Role:` CloudFormation 관련 작업 이외에는 ReadOnly 조회만 가능한 Role
  * `CloudFormation Role`: CloudFormation Stack 배포가 가능한 Role
  * `Operations Role:`  운영을 위해 CloudWatch 메트릭 및 대시보드 조회 Role
  * `SecurityAudit:` Security & Audit 관련 조회만 가능한 Role 
  * `Admin`: IAM을 제외한 Sub 계정의 Full Administrator 가능한 Role 
 * `VPC`: Template for setting up VPCs
  * Private and Public Subnets
  * Optional Network LoadBalancers
  * FlowLogs stored centrally to master account
 * `GuardDuty Membership:` GuardDuty를 Master계정에서 통합 관리하기 위해 멤버로 조인
 * `CloudTrail:` Master계정의 S3에 CloudTrail 로그를 통합 수집하기 위한 Audit 설정 
 * `Config:` Sub 게정의 Config 변경 이력을 Master 계정에서 통합 관리하기 위한 설정 
 * `Default Config Rules:` Config Rules 결과를 저장하는 S3 버킷을 수정하지 못하도록 버킷 설정
 
 
 https://aws.amazon.com/solutions/aws-landing-zone/
