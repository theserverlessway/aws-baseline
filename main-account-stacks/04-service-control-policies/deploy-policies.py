import boto3
import cfnresponse
import time
import random
import re

organizations = boto3.client("organizations")

CREATE = 'Create'
UPDATE = 'Update'
DELETE = 'Delete'


def root():
    return organizations.list_roots()['Roots'][0]


def root_id():
    return root()['Id']


def scp_enabled():
    enabled_policies = root()['PolicyTypes']
    print('Enabled Policy Types: {}'.format(enabled_policies))
    return {"Type": "SERVICE_CONTROL_POLICY", "Status": "ENABLED"} in enabled_policies


def exception_handling(function):
    def catch(event, context):
        try:
            function(event, context)
        except Exception as e:
            print(e)
            print(event)
            if event["RequestType"] == DELETE:
                cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
            else:
                cfnresponse.send(event, context, cfnresponse.FAILED, {})

    return catch


@exception_handling
def enable_service_control_policies(event, context):
    RequestType = event["RequestType"]
    if RequestType == CREATE and not scp_enabled():
        r_id = root_id()
        print('Enable SCP for root: {}'.format(r_id))
        organizations.enable_policy_type(RootId=r_id, PolicyType='SERVICE_CONTROL_POLICY')
    cfnresponse.send(event, context, cfnresponse.SUCCESS, {}, 'SCP')


def with_retry(function, **kwargs):
    for i in [0, 3, 9, 15, 30]:
        # Random sleep to not run into concurrency problems when adding or attaching multiple SCPs
        # They have to be added, updated or deleted one after the other
        sleeptime = i + random.randint(0, 5)
        print('Running {} with Sleep of {}'.format(function.__name__, sleeptime))
        time.sleep(sleeptime)
        try:
            response = function(**kwargs)
            print("Response for {}: {}".format(function.__name__, response))
            return response
        except organizations.exceptions.ConcurrentModificationException as e:
            print('Exception: {}'.format(e))
    raise Exception


@exception_handling
def handler(event, context):
    RequestType = event["RequestType"]
    Properties = event["ResourceProperties"]
    LogicalResourceId = event["LogicalResourceId"]
    PhysicalResourceId = event.get("PhysicalResourceId")
    Policy = Properties["Policy"]
    Attach = Properties["Attach"] == 'true'

    print('RequestType: {}'.format(RequestType))
    print('PhysicalResourceId: {}'.format(PhysicalResourceId))
    print('LogicalResourceId: {}'.format(LogicalResourceId))
    print('Attach: {}'.format(Attach))

    parameters = dict(
        Content=Policy,
        Description="Baseline Policy - {}".format(LogicalResourceId),
        Name=LogicalResourceId,
    )

    policy_id = PhysicalResourceId
    if RequestType == CREATE:
        print('Creating Policy: {}'.format(LogicalResourceId))
        response = with_retry(organizations.create_policy,
                              **parameters, Type="SERVICE_CONTROL_POLICY"
                              )
        policy_id = response["Policy"]["PolicySummary"]["Id"]
        if Attach:
            with_retry(organizations.attach_policy, PolicyId=policy_id, TargetId=root_id())
    elif RequestType == UPDATE:
        print('Updating Policy: {}'.format(LogicalResourceId))
        with_retry(organizations.update_policy, PolicyId=policy_id, **parameters)
    elif RequestType == DELETE:
        print('Deleting Policy: {}'.format(LogicalResourceId))
        # Same as above
        if re.match('p-[0-9a-z]+', policy_id):
            if Attach:
                with_retry(organizations.detach_policy, PolicyId=policy_id, TargetId=root_id())
            with_retry(organizations.delete_policy, PolicyId=policy_id)
        else:
            print('PhysicalResourceId {} is not a valid PolicyId'.format(policy_id))
    else:
        cfnresponse.send(event, context, cfnresponse.FAILED, {}, policy_id)
    cfnresponse.send(event, context, cfnresponse.SUCCESS, {}, policy_id)
