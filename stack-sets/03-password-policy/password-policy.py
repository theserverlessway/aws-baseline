import cfnresponse
import boto3

iam = boto3.client('iam')

def is_bool(value):
    return value.lower() == 'true'

password_policy_keys = dict(
    MinimumPasswordLength=int,
    RequireSymbols=is_bool,
    RequireNumbers=is_bool,
    RequireUppercaseCharacters=is_bool,
    RequireLowercaseCharacters=is_bool,
    AllowUsersToChangePassword=is_bool,
    MaxPasswordAge=int,
    PasswordReusePrevention=int,
    HardExpiry=is_bool
)

def handler(event, context):
    print(event)
    try:
        resource_properties = event['ResourceProperties']
        request_type = event['RequestType']
        if request_type in ['Create', 'Update']:
            update_parameters = {key: cast_type(resource_properties[key]) for key, cast_type in
                                 password_policy_keys.items()}
            print(update_parameters)
            response = iam.update_account_password_policy(**update_parameters)
            print(response)
        elif request_type is 'Delete':
            iam.delete_account_password_policy()

        cfnresponse.send(event, context, cfnresponse.SUCCESS, {}, "")
    except Exception as e:
        print(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {}, "")
