# Cross Account Access

AWS 조직의 모범 사례는 개발자가 하위 계정에서 수행하려는 모든 작업에 대해 수임 할 수있는 하위 계정의 역할을 사용하는 것입니다. 이 문서에서는 교차 계정 역할 액세스가 작동하는 방식과 AWS Console 과 CLI 로 교차 계정에 엑세스 하는 방법을 소개합니다.

## Cross Account Role Setup in the AWS Baseline

이 AWS Baseline은 Admin, Developer, ReadOnly 또는 Operations를 포함하여 수임 할 다양한 역할을 롤아웃합니다. 사용자가 Sub 계정에서 특정 Role이 필요하면 해당 Role에 대한 임시 자격 증명(Temporary Credentials)을 받아서 해당 자격 증명을 작업PC에 환경변수로 설정 후 사용할 수 있습니다.  터미널의 현재 환경으로 내보내고 언어 별 aws-sdk에서 사용할 수 있습니다. ( 최대 12시간 )

기본적으로 Sub 계정에서 Role을 Assume 하기 위해서 IAM 유저는 MFA 인증을 활성화하여 인증을 받아야 합니다.


### AWS Console 에서 Role 전환

AWS 콘솔에서 역할을 맡아 다른 계정의 리소스를 보거나 편집하려면 전환하려는 계정의 AccountId와 맡을 역할의 이름 만 있으면됩니다.

아래 IAM 유저를 클릭한 후, Switch Role 버튼을 클릭합니다. ( Sub 계정에서 전환할 Role의 종류에 대해서는 ../stak-sets/02-assumable-roles을 참조하세요)

![Switch Role Menu](./images/switch-role-menu.png)

다음 페이지에서 역할 전환을 선택하면 ʻAccount`,`Role` 및`DisplayName` 필드가있는 양식이 표시됩니다. 이에 따라 내용을 입력하고 'Switch Role'버튼을 클릭합니다. `DisplayName`을 생략하면 AccountId 또는 Alias와 역할 이름 만 사용하여 더 길지만 이해하기 쉽습니다.
![Switch Role Form](./images/switch-role-form.png)

계정에 적절한 액세스 권한이 있으면 이제 새 계정에 로그인 할 수 있습니다. 오른쪽 상단 메뉴를 열면 방금 입력 한 AccountId와 기본 계정으로 돌아갈 수있는 링크가 표시됩니다. 이전에 입력 한 구성은 브라우저에 저장되므로 다시 전환하려는 경우 (또는 여러 구성이있는 경우 (예 : dev 및 prod 계정)) 빠르게 전환 할 수 있습니다.

참조: [AWS Switch Role Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html)

## Switching Roles in the AWS CLI

AWS CLI에는 Profile 또는 자격 증명을 직접 획득하여 환경변수를 설정하는 두 가지 방법이 있습니다. Profile의 장점은 사용이 빠르고 AWS CLI가 자격 증명을 처리한다는 것입니다. 단점은 일반적으로 한 시간 동안 만 지속되므로 MFA를 사용하는 경우 정기적으로 입력해야한다는 것입니다. 또한 모든 도구가 Profile을 사용할 때 자격 증명 캐싱을 구현하는 것은 아니므로 도구를 실행할 때마다 MFA 세부 정보를 입력해야 할 수 있습니다.

이러한 경우에는 더 긴 기간을 설정할 수 있으므로 자격 증명을 직접 가져와 환경 변수로 등록하는 것이 더 나은 방법입니다.

### Getting credentials with the cli

After getting your own keys and [configuring the aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) you can run the following command to verify who your current credentials belong to:

자체 키를 받고, 환경변수에 Key를 설정 후에 [cinfugring the aws cli] (https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) 후 다음 명령을 실행하여 현재 Credentials에 대한 사용자를 확인할 수 있습니다.

```bash
aws sts get-caller-identity
{
    "UserId": "AIDA41PGWXOK5F4BT4BP",
    "Account": "814916968542",
    "Arn": "arn:aws:iam::814916968542:user/fmotlik"
}
```

올바른 사용자로 인증이 되면 AWS 보안 토큰 서비스 인 'STS'를 사용할 수 있습니다.

We're going to use the [`aws sts assume-role`](https://docs.aws.amazon.com/cli/latest/reference/sts/assume-role.html) command to assume into a specific account. As we've enabled MFA on our account we need to set the `serial-number` and `token-code` parameter.

특정 Sub 계정의 Role을 위임받기 위해[aws sts assume-role] (https://docs.aws.amazon.com/cli/latest/reference/sts/assume-role.html) 명령을 사용합니다. 계정에서 위임 조건으로 MFA를 활성화 했으므로`serial-number` 및`token-code` 매개 변수를 설정해야합니다.

실행하면 출력이 다음과 유사하게 표시됩니다 (다음 예제에서 실제 값은 변수로 대체 됨):

```bash
aws sts assume-role --role-arn arn:aws:iam::SUBACCOUNT_ID:role/ROLE_NAME --serial-number arn:aws:iam::MAIN_ACCOUNT_ID:mfa/fmotlik --token-code 273976 --role-session-name SOME_RANDOM_SESSION_NAME
{
    "Credentials": {
        "AccessKeyId": "AWS_ACCESS_KEY_ID",
        "SecretAccessKey": "AWS_SECRET_ACCESS_KEY",
        "SessionToken": "SESSION_TOKEN",
        "Expiration": "2019-04-05T11:41:31Z"
    },
    "AssumedRoleUser": {
        "AssumedRoleId": "AROAJEILVX4PFJ5KI7I4L6:SOME_RANDOM_SESSION_NAME",
        "Arn": "arn:aws:sts::SUBACCOUNT_ID:assumed-role/ROLE_NAME/SOME_RANDOM_SESSION_NAME"
    }
}
```

그런 다음 AccessKeyId,SecretAccessKey 및 SessionToken의 값을 환경으로 아래와 같이 설정합니다.

```bash
export AWS_ACCESS_KEY_ID=VALUE_OF_AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=VALUE_OF_AWS_SECRET_ACCESS_KEY
export AWS_SESSION_TOKEN=VALUE_OF_SESSION_TOKEN
```

환경 변수를 설정 후`get-caller-identity`를 다시 실행하면 다음과 같은 내용이 표시됩니다:

```bash
aws sts get-caller-identity
{
    "UserId": "AROAJEILVX4PFJ5KI7I4L6:SOME_RANDOM_SESSION_NAME",
    "Account": "SUBACCOUNT_ID",
    "Arn": "arn:aws:sts::SUBACCOUNT_ID:assumed-role/ROLE_NAME/SOME_RANDOM_SESSION_NAME"
}
```

즉, 해당 역할의 자격 증명을 성공적으로 맡았으며 이제 해당 계정에서 작업 할 수 있습니다.

As this process is rather complex there are tools that make this easier. AWSInfo for example has an [assume command](https://github.com/theserverlessway/awsinfo/blob/master/scripts/commands/assume/index.md) to get credentials:

이 프로세스는 다소 복잡하기 때문에이를 쉽게 만드는 도구가 있습니다. 예를 들어 AWSInfo에는 자격 증명을 얻기위한 [assume command] (https://github.com/theserverlessway/awsinfo/blob/master/scripts/commands/assume/index.md)가 있습니다.




다음 명령은 먼저 조직의 모든 계정을 나열하고`dev`를 포함하는 첫 번째 계정을 선택하고`--` 구분 기호 뒤에 지정된 역할을 맡습니다. 또한`-m` 매개 변수로 MFA를 구성하고`-d` 옵션을 통해 자격 증명 기간을 8 시간으로 설정합니다.

터미널에 복사하여 붙여넣고 실행할 수있는 export 이하를 복사합니다. 

```bash
awsinfo assume -md 8 dev -- AssumableAdminRole
Selected Account 735985379897
MFA TOKEN: 957382
export AWS_ACCESS_KEY_ID=VALUE_OF_AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=VALUE_OF_AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN=VALUE_OF_SESSION_TOKEN
```

[AWSInfo 도구 참조] (https://theserverlessway.com/tools/awsinfo/)에서 모든 availabe 명령을 확인하십시오.

### Profiles
AWS CLI를 사용하여 교차 계정 액세스를 위한 Profile을 설정하려면`~ / .aws / config`에 다음을 추가하십시오. 사용자 MFA 디바이스와 역할, 특히 AccountID와 일치하도록 역할 ARN을 일치 시키도록 MFA 디바이스를 편집해야합니다.

```##### COMPANY
[profile company]
region=us-east-1

[profile company-dev]
role_arn = arn:aws:iam::1234567891011:role/AssumableAdminRole
source_profile = company
region = us-east-1
mfa_serial = arn:aws:iam::1011987654321:mfa/YOUR_USER_NAME

[profile company-prod]
role_arn = arn:aws:iam::8573615396827:role/AssumableAdminRole
source_profile = company
region = us-east-1
mfa_serial = arn:aws:iam::1011987654321:mfa/YOUR_USER_NAME
```

The `company` profile in this case has credentials from the main account (set up either through `aws configure` or by editing the credentials file directly). If you run `aws sts get-caller-identity --profile company-dev` you should see the dev account id in the output:

이 경우`company` Profile에는 기본 계정의 Credentials이 있습니다 (`aws configure`를 통해 설정하거나 자격 증명 파일을 직접 편집하여 설정). ʻaws sts get-caller-identity --profile company-dev`를 실행하면 출력에 dev 계정 ID가 표시되어야합니다.

```{
    "UserId": "AROAJ7ZDAUEM44NIIIF4Q:botocore-session-1552422118",
    "Account": "1234567891011",
    "Arn": "arn:aws:sts::488242777082:assumed-role/AssumableAdminRole/botocore-session-1552422118"
}
```

## 참조 
* [Role documentation in AWS IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html) 
