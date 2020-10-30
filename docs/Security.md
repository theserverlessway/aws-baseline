# Note on Security

The account assume setup does its best to make sure escalating rights isn't possible. From providing various roles
to assume to providing [Permission Boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html) by default and MFA support. Those measures are only effective though if your team follows best practices by using MFA and not creating workarounds for Admin access in various accounts.

IAM은 직무 혹은 필요에 따라 사전에 제공되는 역할을 가진 그룹으로 관리되며 IAM 유저에 권한을 직접 부여하지 않고, Role을 위임(Assume) 받는 형태로 구성됩니다. IAM 유저와 그룹은 Master 계정에서 관리되고, 기본적으로는 ReadOnly 권한만 부여됩니다. 
리소스를 배포하는 인프라 담당자와 같이 권한이 필요한 IAM 유저는 작업할 Sub 계정에 대한 적절한 작업 권한을 가진 그룹에 추가가되면 해당 계정의 신청한 권한을 위임받을 수가 있습니다. 

## Region Limitation

각 Sub 계정에 배포 된 일부 Role은 특정 지역으로 제한됩니다. Admin Role 및 ReadOnly Role은 특정 지역으로 제한되지 않습니다. 특정 지역에 대해서만 Assumable Role을 생성하고 싶은 경우, Sub 계정에 배포될 StackSet 설정에서 AllowedRegions 파라미터에 설정을 원하는 지역을 설정하면 됩니다. 
```
# stack-set.config.yaml

parameters:
  AllowedRegions: ap-northeast-2,us-east-1
```

## Permissions Boundaries

Sub 계정에서 생성 된 모든 Role은 Permission Boundary로 특정 리소스 및 서비스에 대한 액세스가 제한됩니다.  ( 예 : IAM 관련, Region 제한 Boundary ) 뿐만 아니라 StackSet을 통해 생성된 CloudFormation 스택에 대한 모든 액세스가 거부됩니다. 자세한 내용은 StackSet 문서를 확인하세요.

설정되는 중요한 Boundary 중 하나는 Sub 계정에서 Developer가 만든 Role에 대한 것입니다. 기준 역할을 통해 생성 된 모든 역할 또는 사용자는 특정 경계로 설정된 권한 경계를 가져야합니다. 이렇게하면 권한 승격이 불가능합니다. 

This PermissionsBoundary limits access to iam and other services for these roles and enforces the same Boundaries as the DeveloperRole has. For CloudFormation you could do the following:

이 PermissionsBoundary는 이러한 Role에 대한 iam 및 기타 서비스에 대한 액세스를 제한하고 DeveloperRole과 동일한 경계를 적용합니다. CloudFormation의 경우 다음을 수행 할 수 있습니다.

```yaml
!Sub arn:aws:iam::${AWS::AccountId}:policy/CreatedIdentitiesPermissionsBoundary
```

이 PermissionsBoundary가 설정되면 새 Role 또는 IAM 유저를 생성 할 수 없습니다. 이 동작을 비활성화하려면 ʻassumable-roles` StackSet에서 ʻIAMPermissionBoundaryLimitation`을`false`로 설정할 수 있습니다. 그러나 이것은 매우 위험 할 수 있으며 어떤 이유로 든 자격 증명이 유출되면 권한이 상승 할 수 있습니다.

동일한 StackSet에서`DisabledIdentitiesServices` 변수를 설정하여 계정에서 생성 된 모든 역할에 대해 특정 AWS 서비스를 비활성화 할 수 있습니다. 해당 서비스의 모든 작업에 대한 액세스를 비활성화합니다. ʻIAM` 및`CloudTrail`과 같은 몇 가지 서비스가 기본 목록에 있습니다. 병합되지 않으므로 자신의 목록을 구성하려면 해당 목록을 포함해야합니다. 배포 후 정책을 확인하여 원하는 제한 사항을 준수하십시오.