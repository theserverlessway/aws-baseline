# AWS Baseline 적용

소스코드 루트 위치에서 `make rollout` 커맨드를 실행하면 자동으로 aws baseline이 Sub 계정에 적용됩니다. 그러나 명령을 실행하기 전에 몇가지 고려해야 할 사항이 있습니다.   

## Storing your customisations
이 Repository를 fork하고 인프라에 수행중인 모든 변경사항을 자신의 Repository에 커밋하는 것이 좋습니다. 이렇게하면 언제든지 인프라를 쉽게 재배포하고 업스트림에서 baseline을 선택적으로 업데이트 할 수 있습니다.

## Single Main Account or Split Management Accounts

계정 설정을 결정할 때 고려해야 할 사항은 하나의 Master 계정으로 다른 모든 계정을 관리하거나 AWS LandingZone 솔루션처럼 기능에 따라 계정을 별도의 Logging, Security 또는 기타 Management 계정으로 분할하려는 경우입니다.

단일 Master 계정의 장점은 전체 인프라를 보다 쉽게 관리할 수 있습니다. 모든 구성 및 배포 메타 데이터가 하나의 계정에 저장되므로 다양한 부서 혹은 팀에 대해 단일 계정에서 엄격한 보안 준수를 보다 쉽게 관리할 수 있습니다. Master 계정은 Sub 계정 목록에 액세스 할 수있는 유일한 계정이므로 AccountID를 하드 코딩 할 필요가 없으므로 다양한 배포를 자동화하는 것이 더 쉽습니다.

## Configuration to change when setting up multiple Management Accounts

기본 계정 구성을 여러 계정으로 분할하려는 경우 각 StackSet에서 해당 관리 계정을 가리 키도록 적절한 구성 값을 설정해야합니다.

예를 들어 'Audit'Stack을 별도의 Logging 계정에 배포하는 경우, CloudTrail, Config 또는 VPC Flowlog는 해당 StackSet의 'MainAccount'파라미터를 각 관리 계정의 ID로 설정해야합니다. `main-account-parameter`를 검색하고`stack.config.yaml` 파일에서 직접 해당 매개 변수를 설정하여 모든 StackSet을 찾을 수 있습니다.

기본적으로 이러한 StackSet의`MainAccount` 매개 변수는 단일 기본 계정을 사용하는 경우 baseline 작업을 수행하는 AccountId로 설정됩니다.


## Configuring the Regions

The configuration files for each Stack and StackSet have us-east-1 hardcoded as the region to deploy into. This is done so that no individual stack can accidentally be deployed into the wrong region. If you do not want your Stacks or StackSets to be deployed into us-east-1 please change those values accordingly in each configuration file. While this is a manual effort and might be more automated in the future it removes some future problems with inconsistent configuration.

각 Stack 및 StackSet의 구성 파일에는 배포 할 지역으로 ap-northeast-2로 하드 코딩되어 있습니다. 이는 개별 스택이 실수로 잘못된 지역에 배포되지 않도록 하기위한 것입니다. 스택 또는 StackSet이 ap-northeast-2에 배포되는 것을 원하지 않는 경우 각 구성 파일에서 해당 값을 적절히 변경하십시오. 이는 수동 작업이며 앞으로 더 자동화 될 수 있지만 일관성없는 구성으로 인해 발생하는 몇 가지 향후 문제를 제거합니다.

## Excluding Stacks or StackSets

baseline 적용시에 계정에 Stack 또는 StackSet 적용을 제외하려면`main-account-stacks` 또는`stack-sets` 디렉토리의 'Excluded'파일에 디렉토리 이름을 추가합니다. 정확히 일치해야합니다.

제외 된 디렉토리를 확인하려면 기본 디렉토리 나`main-account-stacks` 또는`stack-sets` 디렉토리에서`make exclude`를 실행하십시오.

## Rolling out the Baseline

이제 마지막으로 필요한 모든 조정을 마친 후 baseline을  적용할 수 있습니다. Master 계정에 대한 관리자 액세스 권한이있는 로컬 자격 증명이 있는지 확인하십시오. Toolbox Docker Container (`make shell`로 시작)에 있거나 [ʻawsinfo`] (https://theserverlessway.com/tools/awsinfo/)가 설치되어있는 경우 ʻawsinfo me` 및 ʻawsinfo를 실행할 수 있습니다. 로그인 한 사용자와 현재 사용 된 자격 증명 및 리전을 확인합니다.

그 후 저장소의 루트 폴더에서`make rollout`을 실행합니다. 이 작업은 먼저`main-account-stacks` 폴더로 전환하고 거기에서`make rollout`을 실행하고 모든 스택을 배포합니다. 그 후`stack-sets` 폴더로 전환하고 StackSets를 배포합니다. 배포 중에 문제가 발생하는 경우 이미 존재하는 경우 기존 스택을 업데이트하므로`make rollout`을 다시 실행할 수 있습니다.

## Adding new Accounts

새로운 계정에 추가되면 각각의 Sub 계정 리스트에 추가된 AccountId 를 추가하고 `make rollout` 을 수행하면 새로 추가된 계정에 baseline이 적용됩니다. 

추가된 AccountId를 설정이 필요한 항목에 추가하고, 저장소의 Root 폴더에서 먼저`make diff`를 실행하여 수행 될 모든 변경 사항을 확인합니다. 그런 다음 'make rollout'을 실행하여 Baseline이 'main-account-stacks'및 'stack-sets'폴더를 통과하고 모든 스택 및 StackSet를 롤아웃합니다. `main-account-stacks` 및`stack-sets` 하위 폴더에서`make diff` 또는`make rollout`을 실행하여 독립적으로 배포 할 수도 있습니다.

## Updating the Baseline and Debugging issues

Whenever you want to update the baseline either by customising it or adding features from the upstream repository run `make rollout` again after updating repository.

저장소에서 기능을 추가하여 기준을 업데이트하려면 저장소를 업데이트 한 후 'make rollout'을 다시 실행하면 이미 배포된 Stack과 StackSet의 ChangeSet에 변경된 부분만 업데이트 됩니다. 

baseline 배포시 오류가 발생하면 AWS Console의 CloudFormation 에서 에러가 발생한 Stack의 이벤트에서 에러 원인을 확인하고 수정합니다. 
