# Main Account Stacks

기본 계정 스택은 [`formica`] (https://theserverlessway.com/tools/formica/)로 배포됩니다. 'make rollout'으로 모든 스택을 업데이트하거나 해당 디렉토리로 이동하여 'formica change -c stack.config.yaml'을 실행하여 개별적으로 스택을 업데이트 할 수 있습니다. 그러면`formica deploy -c stack.config.yaml`로 배포 할 수있는 변경 세트가 생성됩니다.

스택을 배포하기 전에 'make diff'를 실행하여 모든 스택에 대한 차이를 가져 오거나 스택 디렉토리에서 'formica diff -c stack.config.yaml'을 실행하여 배포 될 변경 사항의 전체 차이를 가져와야합니다. ChangeSet과 Diff를 함께 사용하면 변경 사항을 배포하기 전에 변경 될 내용을 안전하게 파악할 수 있습니다.

## Stack Summaries:

각 스택에 대한 간략한 요약을 따릅니다. 각 스택에 대한 개별 문서는 각 스택 디렉토리의`README.md`를 참조하십시오.

* `01-auditing`: S3 Buckets and configuration to store CloudTrail, Config and FlowLogs data
* `02-budget`: Account Budget with MaxBudget set and alerts sent to Account Email by default
* `03-iam-groups`: IAM groups to manage Users and give access to Sub Accounts
* `04-service-control-policies`: Service Control Policies deployed as a StackSet
* `05-validate-stack-set-deployments`: Validates deployed StackSet instances against the tags set on the StackSets. Records AWS Config Evaluations to see missing StackSet Instances.

## Excluding Stacks

자동 롤아웃에서 스택을 제외하려면 ʻExcluded` 파일에 디렉토리 이름을 추가하십시오.
정확히 일치해야합니다. grep을 방해하므로 빈 줄을 추가하지 마십시오

제외 된 디렉토리를 확인하려면`make exclude '를 실행하십시오.