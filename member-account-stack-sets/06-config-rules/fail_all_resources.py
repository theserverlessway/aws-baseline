import boto3
import json
import os

config = boto3.client('config')

CLOUDFORMATION_TYPE = 'AWS::CloudFormation::Stack'


def handler(event, context):
    invoking_event = json.loads(event['invokingEvent'])
    configItem = invoking_event.get('configurationItem') or invoking_event['configurationItemSummary']
    resource_id = configItem['resourceId']
    resource_type = configItem['resourceType']
    print("FunctionName: " + context.function_name)
    print("ResourceId: " + resource_id)
    print("Resourcetype: " + resource_type)
    compliance_type = 'NON_COMPLIANT'
    annotation = 'No Resources should be deployed in this Region'
    if (
            (context.function_name == resource_id and resource_type == 'AWS::Lambda::Function') or
            (os.environ['StackName'] in resource_id and resource_type == CLOUDFORMATION_TYPE) or
            ('StackSet-' in resource_id and resource_type == CLOUDFORMATION_TYPE)
    ):
        compliance_type = 'COMPLIANT'
        annotation = 'Compliant'

    print('ComplianceStatus: ' + compliance_type)
    config.put_evaluations(
        Evaluations=[
            {
                'ComplianceResourceType': resource_type,
                'ComplianceResourceId': resource_id,
                'ComplianceType': compliance_type,
                'Annotation': annotation,
                'OrderingTimestamp': configItem['configurationItemCaptureTime']
            }
        ],
        ResultToken=event['resultToken']
    )
