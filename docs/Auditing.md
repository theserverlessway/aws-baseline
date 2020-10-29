# Auditing and Reviews

Audit은 모든 AWS Baseline에서 중요한 부분입니다. AWS는 계정 Audit를위한 다양한 서비스를 제공합니다. Baseline에는 GuardDuty, AWS Config 및 Cloudtrail Storage에 대한 설정과 계정 감사를위한 기타 도구가 포함됩니다.

## Guard Duty and Config

기본적으로 모든 계정의 모든 지역에는 GuardDuty 및 Config Enabled가 있습니다.

* [`GuardDuty`](https://aws.amazon.com/guardduty/): 머신러닝을 통해 CloudTrail, FlowLogs에서 의심되는 패턴을 찾고, 리포팅해주는 머신러닝 기반 AWS 침입 탐지 서비스   예 : 이전에 API 상호 작용이 없었던 국가의 IP 주소 또는 퍼블릭 인스턴스에서 포트 Probe
* [`Config`](https://aws.amazon.com/config/): Config는 리소스 상태 (예 : EC2 인스턴스 또는 VPC의 모든 구성)를 저장하고, 이를 해당 리소스에 대해 정의 된 규칙 세트와 비교합니다. 해당 리소스가 준수하지 않는 경우 비준수로 표시됩니다.
* [`CloudTrail`](https://aws.amazon.com/cloudtrail/): CloudTrail은 모든 AWS API 상호 작용을 기록하고 나중에 평가할 수 있도록 저장합니다. 이는 보안 분석을위한 것이거나 특정 리소스의 권한을 제한하기위한 액세스 패턴을 결정하기 위한 것일 수 있습니다. 
* [`VPC FlowLogs`](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html): Flowlogs는 VPC의 네트워크 인터페이스에서 들어오고 나가는 IP 트래픽에 대한 정보를 캡처합니다. 연결된 IP, 연결이 통과 한 포트, 시간 프레임에 전송 된 바이트 수 등을 기록합니다. 이는 문제를 분석하고 인프라에 대한 공격을 결정 및 분석하는 데 유용합니다.

### GuardDuty

GuardDuty는 Region 서비스이므로 각 지역에서 활성화해야하며 Master 계정에는 모든 Region의 모든 Sub 계정에 대해 설정된 초대가 있어야합니다. 이를 달성하기 위해 하나는 기본 계정에 다른 하나는 하위 계정에 두 개의 개별 StackSet으로 배포합니다.

이것이 롤아웃되면 해당 지역의 기본 계정 GuardDuty 콘솔에서 특정 지역에 대한 모든 결과를 볼 수 있습니다.

### Config 

Config allows to aggregate evaluations across regions and accounts into a central location. The `auditing` stack in the main-account stacks sets up an aggregator accross all accounts, so depending into which region you deploy that stack, there you'll find the Aggregator.   

Config를 사용하면 지역 및 계정에 대한 평가를 중앙 위치로 집계 할 수 있습니다. Master 계정 Stack의 'Audit'Stack은 모든 계정에 대해 Aggregator를 설정하므로 해당 Stack을 배포하는 지역에 따라 집계자를 찾을 수 있습니다

Some AWS Resources are considered [global resources](https://docs.aws.amazon.com/config/latest/developerguide/select-resources.html) and can therefore show up in any region. To prevent this duplication the Baseline uses a StackSet parameter `GlobalConfigRegion` in the `auditing` StackSet which allows you to set that global region which records these global resources.

## CloudTrail

CloudTrail은 계정 전체에 설정되며 각 계정 및 리전의 CloudWatch LogGroup과 모든 계정의 중앙 버킷에 기록합니다. 이를 통해 특정 계정 및 지역에 로그인했을 때 문제를 분석 할 수있을뿐만 아니라 전체 계정에서의 문제를 찾고 분석 할 수도 있습니다.

### Analyzing with Athena

Athena is a Service in AWS that lets you query data in S3 Buckets through SQL queries. This simplifies analytics across all API events in all accounts drastically, especially in high pressure moments like a potential attack on your infrastructure. It also partitionas your data anytime a new CloudTrail file gets written to the bucket, so you can use the `date` field to query against. For example the following query will create vastly different numbers:

Athena는 SQL 쿼리를 통해 S3 버킷의 데이터를 쿼리 할 수있는 AWS의 서비스입니다. 이를 통해 모든 계정의 모든 API 이벤트에 대한 분석이 대폭 간소화됩니다. 특히 인프라에 대한 잠재적 인 공격과 같은 압력이 높은 순간에 더욱 그렇습니다. 또한 새 CloudTrail 파일이 버킷에 기록 될 때마다 데이터를 분할하므로`date` 필드를 사용하여 쿼리 할 수 ​​있습니다.

* `Select count(*) from auditing.cloudtrail where date > '2020'`
* `Select count(*) from auditing.cloudtrail where date > '2020-10'`
* `Select count(*) from auditing.cloudtrail where date > '2020-10-23'`

날짜 형식은`YYY-MM-DD`이며 간단한 문자열 비교이므로`>`또는`<`또는 둘 다와 비교할 수 있습니다. 따라서 대용량 데이터에서도 쿼리가 정말 빨라집니다.

Baseline은 CloudTrail 버킷 용 Athena를 설정하고 계정을 분석하고 더 복잡한 분석을 시작할 수 있도록 몇 가지 쿼리를 추가합니다. 'Athena 대시 보드'로 이동하여 '저장된 쿼리'로 이동하면 'RootLogin30Days'쿼리가 표시됩니다. 그것을 클릭하면 쿼리를보고 실행할 수있는 쿼리 편집기로 이동합니다.

쿼리를 실행하면 지난 30 일 동안 누군가가 루트 계정에 로그인 한 횟수에 대한 모든 세부 정보를 얻을 수 있습니다.



## FlowLogs
VPC StackSet을 사용하거나 CloudFormation 스택으로 직접 배포하면 FlowLog가 해당 계정 및 리전의 CloudWatch Log Group에 저장되고 기본 계정의 중앙 flowlogs 버킷으로 전달됩니다. 여러 계정의 트래픽을 빠르게 분석하려면 위에 설명 된대로 'Athena'를 사용할 수도 있습니다.

## Tool Based Security Audit

The Makefile in the root of the repository has a `security-audit-all` task that will run a full audit on all of your accounts. It uses [Prowler](https://github.com/toniblyx/prowler) and [ScoutSuite](https://github.com/nccgroup/ScoutSuite) to audit the accounts. The make commands will use Docker to create the container with all required tools and run the audit inside of that container. If you want to run the script directly on your system make sure those tools are installed on your system.


When you run the audit make sure that your current credentials are MFA signed, so use `awsinfo assume token -md 8` and export the given variables before calling the command. This limits the time credentials are valid to 1 hour because of chain assuming (assume token then assume role), so in case an audit of a single account takes longer and you need MFA you can use the `-m` and `-d` options. `-m` will ask for an MFA token when assuming a role which allows the limit to be increased with the `-d` option. Make sure you don't use credentials obtained through `awsinfo assume token` when using the `-d` option though, as it would be a chain assume and limit the max duration to 1 hour. 

If you only want to run the audit against a specific account, you can run the single account make command with `make security-audit-accounts Accounts=1234567898765` ir the script directly with `./scripts/security-audit ACCOUNT_ID`.

By default the `AssumableSecurityAuditRole` is assumed and used. If you want to use a different role, set it with the `-r` parameter. If you want to run the audits in parallel use the `-p` option. [Xargs] needs to be installed on your system in that case. For the Prowler reports you also need [`ansi2html`](https://pypi.org/project/ansi2html/) and `sed` installed on your System. For assuming the roles [`awsinfo`](https://theserverlessway.com/tools/awsinfo/) is used, make sure to install it.

The reports are stored in the reports folder, with separate folders for each audit tool. You can check the progress of the Audit in the reports files as logs are written into the reports folder. As it runs through all your accounts and collects a lot of data the Audit will take quite a long time (even if run in parallel mode).
