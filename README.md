# AWS Account Baseline

이 리포지토리에는 AWS Baseline (a.k.a landing zone)을 롤아웃하기위한 구성이 포함되어 있습니다. AWS로의 본격적인 전환을 고려하는 조직 부합한 유연한 Landing Zone 을 구축할 수 있습니다. 

Baseline은 CloudFormation Stacks와 StackSet의 혼합을 통해 구현되며 개별 부분은 선택 사항이므로 인프라 설정을 결정할 수 있습니다.

Baseline에서 제공되는 기능은 다음과 같습니다     

* 모든 Sub계정에 대한 Role을 위임받을 수 있는 Group을 통한 Identity and Access Control
* Auditing with CloudTrail, GuardDuty and Config
* 오픈소스 기반 보안 및 컴플라이언스 Report Tool [Prowler](https://github.com/toniblyx/prowler) and [ScoutSuite](https://github.com/nccgroup/ScoutSuite) 
* Flexible VPC Configuration 
* Sub 계정의 FlowLog, CloudTrail 로그를 빠른 검색을 위한 AWS Athena 설정
* and more ...

## Customisations and Consulting

특별한 기능 추가가 필요한 고객사의 경우 SK C&C Cloud Tranformation 그룹의 AWS TF에 이메일 부탁드립니다. ( jingood2@sk.com )
여기서 사용되는 Tool에 대한 상세 정보는 https://theserverlessway.com 에서 확인할 수 있습니다.

## Comparison to AWS Control Tower and Landing Zone

기존 생성된 AWS Account의 경우, AWS Landing Zone 혹은 AWS Control Tower 관리체계 하에 두기가 어렵습니다.( 수동으로 소스코드를 수정하여 Baseline을 기존 계정에 추가)

그리고 다양한 고객의 환경과 요구사항을 선택적용하거나 커스터마이징 하기가 어렵습니다. 그러나 이 레포지토리에서 제공하는 Landing Zone은 고객이 원하는 기능만 선택 적용가능하고, 커스터마이징도 가능합니다. 

향후에는 AWS Control Tower와 호환가능한 Baseline 기능을 제공한 계획입니다. 


## General Baseline Info

`main-account-stacks` 폴더에는 먼저 중앙에서 Sub계정을 관리하는 Master 계정에 배포해야하는 CloudFormation 스택이 포함되어 있습니다. 기존 계정에 대한 역할과 그룹을 설정하고 다양한 감사 데이터를 저장하도록 S3 버킷을 구성합니다.

The `stack-sets` folder contains StackSets that should be created in your main account and then deployed
into your member accounts. For more information on the StackSets check out the README in the `stack-sets` folder.

`stack-sets` 폴더에는 Sub 계정에서 배포되어야 하는 CloudFormation 스택을 Master 계정에서 StackSet을 이용하여 원격으로 Sub계정에 작업합니다. StackSets에 대한 자세한 내용은`stack-sets` 폴더의 README를 확인하세요.

Various stacks are based on or derived from the wonderful [Widdix Templates](http://templates.cloudonaut.io/en/stable/). Check them out they do an amazing job!

## AWS Baseline Toolbox

As the AWS Baseline needs a few different tools and dependencies to be set up the easiest way to get started is the toolbox that comes built-in. With `make shell` you can start a Docker Container that includes all necessary tools. It forwards all AWS Environment Variables you've set and make the `~/.aws` folder accessible in the toolbox. This means you can use all your AWS credentials the same way as outside of the container.

AWS Baseline을 설정하기 위해서는 몇 가지 다른 Tool이 설치가 필요한데 작업 환경을 구성하는 가장 쉬운 방법은 기본 제공되는 Docker 환경을 이용하는 방법입니다.  `make shell`을 사용하면 필요한 모든 도구가 포함 된 Docker 컨테이너를 시작할 수 있습니다. 설정 한 모든 AWS 환경 변수를 전달하고 도구 상자에서`~ / .aws` 폴더에 액세스 할 수 있도록합니다. 즉, 컨테이너 외부와 동일한 방식으로 모든 AWS 자격 증명을 사용할 수 있습니다.

이 Docker 컨테이너를 이용하여 작업을 보다 빠르게 진행할 수 있기 때문에 가급적 제공되는 컨테이너를 이용합니다. 

## Rolling out the Baseline

Baseline을 계정에 롤아웃하고, 업데이트하는 것은 `make rollout` 커맨드를 실행하여 수행 할 수 있습니다. 이 작업을 수행하기 전에 전체 [`AWS Baseline 적용`] (docs / Rollout.md) 설명서를 읽고 필요한 모든 구성 값을 올바르게 설정하십시오.

Baseline 적용 후, AWS 서비스에 대한 API 연동을 위해 MFA 인증 및 작업PC에 Credentials 설정이 필요합니다. 'scripts'하위 폴더의 'assume-token'스크립트를 사용하여 mfa 보안 자격 증명을 가져옵니다. 일반적으로 './scripts/assume-token -m -d 8 -p my-profile'과 같은 것을 실행하여 'my-profile'프로필에 대해 8 시간 동안 지속되는 MFA 서명 자격 증명을 얻습니다. ( 이 Tool은 시스템에 JQ 설치 필요 ) 
용
스크립에서 제공하는 옵션은 다음과 같습니다. 

* -p: For setting the AWS Profile to use
* -m: For using an MFA device and asking for the token
* -d: For setting the expiration of the token
* -t: For directly setting the MFA token code (will be asked for if not set)
* -s: For setting the MFA device serial number directly 


### Auditing and Security

Master 및 Sub 계정 모두에 배포 된 Stacks 및 StackSets는 모범 사례 감사 및 보안 솔루션을 설정합니다. 여기에는 모든 계정 및 리전에서 CloudTrail, Config 및 GuardDuty가 포함됩니다. 계정의 현재 상태를 쉽게 감사 할 수 있도록 하나의`make` 명령으로 실행할 수있는 다양한 AWS 보안 감사 도구도 포함되어 있습니다.

Audit 및 Security에 대한 보다 상세한 설명은 [Auditing Documentation](docs/Auditing.md) and the [Security Documentation](docs/Security.md).

Audit 설정을 잘 이해하고, 조직에서 문제를 감지하는 방법을 이해할 수 있도록 AWS Native 보안 서비스에 익숙해 져야합니다.

## User and Access Management

Master 계정에서는 사용자가 Sub 계정에서 Role을 맡을 수있는(Assumable) 여러 'assume-role' 그룹을 생성합니다. 현재 Sub 계정이 추가될 때마다 계정 추가, 적용하는 최소한의 수작업이 필요합니다. 새 계정을 추가 할 때 스택을 다시 배포하여 새 계정을 선택하고 그에 따라 그룹을 만들어야합니다. Cross 계정에서 Role을 전환하는 방법에 대한 세부 내용은[Assume Role Documentation](docs/Assume.md) 참조하세요 

Master 계정의 스택은 사용자 관리를위한 다양한 그룹도 생성합니다. 이렇게하면 새 사용자를 그룹에 추가하여 새 사용자를 만들거나 그룹 구성원을 관리 할 수 ​​있습니다. 사용자 관리에 대한 세부 내용은 
[User Management Documentation](docs/UserManagement.md) 를 참조하세요. 

Master 계정에 배포되는 각 스택에 대한 자세한 내용은 [main-account-stacks README](./ main-account-stacks/README.md)를 확인하세요.

## Tooling

이 소스에서는 필요한 패키지가 설치된 Docker 기반의 컨테이너로 `make shell`로 시작할 수 있도록 작업 환경을 제공합니다. 여기에는 기준을 관리하고 AWS API와 상호 작용하는 다양한 도구가 포함되어 있습니다. 설치된 모든 도구를 보려면 도구 상자 폴더의 파일을 확인하십시오.

The only required tool to roll out your infrastructure is [`Formica`](https://theserverlessway.com/tools/formica/). If you do not want to or can't use the Docker based toolbox you need to install this tool.

CloudFormation 스택을 배포하는데 사용되는 cli 도구는 [`Formica`] (https://theserverlessway.com/tools/formica/)입니다. Docker 기반 도구 상자를 사용하지 않거나 사용할 수없는 경우이 도구를 설치해야합니다.


## Deleting default VPCs

계정에서 모든 기본 VPC를 삭제하는 것은 가장 먼저 수행해야하는 보안 정책중 하나 입니다 `delete-default-vpcs`는 현재 내 Crednetial이 설정된 모든 리전에서 default VPC를 제거합니다. 따라서 [environment variables] (https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)를 통해 자격 증명 또는 프로필을 설정하고 명령을 시작합니다. 기본 Docker 컨테이너 내부에서 실행되므로 시스템에 도구를 설치할 필요가 없습니다.

## License
The AWS Baseline is published under the Apache License Version 2.0.
