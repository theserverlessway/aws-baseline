import pytest
import fail_all_resources
import os


@pytest.fixture
def config(mocker):
    return mocker.patch('fail_all_resources.config')


@pytest.fixture
def context(mocker):
    os.environ['StackName'] = STACK_NAME
    mock = mocker.Mock()
    mock.function_name = LAMBDA_FUNCTION
    return mock


OVERSIZED_EVENT = {
    "invokingEvent": "{\"configurationItemSummary\": {\"changeType\": \"UPDATE\",\"configurationItemVersion\": \"1.2\",\"configurationItemCaptureTime\":\"2016-10-06T16:46:16.261Z\",\"configurationStateId\": 0,\"awsAccountId\":\"123456789012\",\"configurationItemStatus\": \"OK\",\"resourceType\": \"AWS::EC2::Instance\",\"resourceId\":\"i-00000000\",\"resourceName\":null,\"ARN\":\"arn:aws:ec2:us-west-2:123456789012:instance/i-00000000\",\"awsRegion\": \"us-west-2\",\"availabilityZone\":\"us-west-2a\",\"configurationStateMd5Hash\":\"8f1ee69b287895a0f8bc5753eca68e96\",\"resourceCreationTime\":\"2016-10-06T16:46:10.489Z\"},\"messageType\":\"OversizedConfigurationItemChangeNotification\"}",  # noqa
    "ruleParameters": "{\"myParameterKey\":\"myParameterValue\"}",
    "resultToken": "myResultToken",
    "eventLeftScope": False,
    "executionRoleArn": "arn:aws:iam::123456789012:role/config-role",
    "configRuleArn": "arn:aws:config:us-east-2:123456789012:config-rule/config-rule-ec2-managed-instance-inventory",
    "configRuleName": "change-triggered-config-rule",
    "configRuleId": "config-rule-0123456",
    "accountId": "123456789012",
    "version": "1.0"
}

EVENT = {
    "invokingEvent": "{\"configurationItem\":{\"configurationItemCaptureTime\":\"2016-02-17T01:36:34.043Z\",\"awsAccountId\":\"123456789012\",\"configurationItemStatus\":\"OK\",\"resourceId\":\"i-00000000\",\"ARN\":\"arn:aws:ec2:us-east-2:123456789012:instance/i-00000000\",\"awsRegion\":\"us-east-2\",\"availabilityZone\":\"us-east-2a\",\"resourceType\":\"AWS::EC2::Instance\",\"tags\":{\"Foo\":\"Bar\"},\"relationships\":[{\"resourceId\":\"eipalloc-00000000\",\"resourceType\":\"AWS::EC2::EIP\",\"name\":\"Is attached to ElasticIp\"}],\"configuration\":{\"foo\":\"bar\"}},\"messageType\":\"ConfigurationItemChangeNotification\"}",  # noqa
    "ruleParameters": "{\"myParameterKey\":\"myParameterValue\"}",
    "resultToken": "myResultToken",
    "eventLeftScope": False,
    "executionRoleArn": "arn:aws:iam::123456789012:role/config-role",
    "configRuleArn": "arn:aws:config:us-east-2:123456789012:config-rule/config-rule-0123456",
    "configRuleName": "change-triggered-config-rule",
    "configRuleId": "config-rule-0123456",
    "accountId": "123456789012",
    "version": "1.0"
}

STACK_NAME = 'TestStack'
STACK_EVENT = {
    "invokingEvent": "{\"configurationItem\":{\"configurationItemCaptureTime\":\"2016-02-17T01:36:34.043Z\",\"resourceId\":\"TestStack\",\"resourceType\":\"AWS::CloudFormation::Stack\"}}",  # noqa
    "resultToken": "myResultToken"
}

LAMBDA_FUNCTION = 'LambdaFunction'
LAMBDA_FUNCTION_EVENT = {
    "invokingEvent": "{\"configurationItem\":{\"configurationItemCaptureTime\":\"2016-02-17T01:36:34.043Z\",\"resourceId\":\"LambdaFunction\",\"resourceType\":\"AWS::Lambda::Function\"}}",  # noqa
    "resultToken": "myResultToken"
}

AUDIT_STACK_SET_EVENT = {
    "invokingEvent": "{\"configurationItem\":{\"configurationItemCaptureTime\":\"2016-02-17T01:36:34.043Z\",\"resourceId\":\"StackSet-audit-test-something\",\"resourceType\":\"AWS::CloudFormation::Stack\"}}",  # noqa
    "resultToken": "myResultToken"
}


def test_all_resources_with_event(config, context):
    fail_all_resources.handler(EVENT, context)
    config.put_evaluations.assert_called_with(
        Evaluations=[
            {
                'ComplianceResourceType': 'AWS::EC2::Instance',
                'ComplianceResourceId': 'i-00000000',
                'ComplianceType': 'NON_COMPLIANT',
                'Annotation': 'No Resources should be deployed in this Region',
                'OrderingTimestamp': '2016-02-17T01:36:34.043Z'
            }
        ],
        ResultToken='myResultToken'
    )


def test_all_resources_with_oversized_event(config, context):
    fail_all_resources.handler(OVERSIZED_EVENT, context)
    config.put_evaluations.assert_called_with(
        Evaluations=[
            {
                'ComplianceResourceType': 'AWS::EC2::Instance',
                'ComplianceResourceId': 'i-00000000',
                'ComplianceType': 'NON_COMPLIANT',
                'Annotation': 'No Resources should be deployed in this Region',
                'OrderingTimestamp': '2016-10-06T16:46:16.261Z'
            }
        ],
        ResultToken='myResultToken'
    )


def test_config_stack_is_compliant(config, mocker, context):
    fail_all_resources.handler(STACK_EVENT, context)
    config.put_evaluations.assert_called_with(
        Evaluations=[
            {
                'ComplianceResourceType': 'AWS::CloudFormation::Stack',
                'ComplianceResourceId': 'TestStack',
                'ComplianceType': 'COMPLIANT',
                'Annotation': 'Compliant',
                'OrderingTimestamp': '2016-02-17T01:36:34.043Z'
            }
        ],
        ResultToken='myResultToken'
    )


def test_ignores_audit_stack_set(config, mocker, context):
    fail_all_resources.handler(AUDIT_STACK_SET_EVENT, context)
    config.put_evaluations.assert_called_with(
        Evaluations=[
            {
                'ComplianceResourceType': 'AWS::CloudFormation::Stack',
                'ComplianceResourceId': 'StackSet-audit-test-something',
                'ComplianceType': 'COMPLIANT',
                'Annotation': 'Compliant',
                'OrderingTimestamp': '2016-02-17T01:36:34.043Z'
            }
        ],
        ResultToken='myResultToken'
    )


def test_ignores_lambda(config, mocker, context):
    fail_all_resources.handler(LAMBDA_FUNCTION_EVENT, context)
    config.put_evaluations.assert_called_with(
        Evaluations=[
            {
                'ComplianceResourceType': 'AWS::Lambda::Function',
                'ComplianceResourceId': LAMBDA_FUNCTION,
                'ComplianceType': 'COMPLIANT',
                'Annotation': 'Compliant',
                'OrderingTimestamp': '2016-02-17T01:36:34.043Z'
            }
        ],
        ResultToken='myResultToken'
    )
