import boto3
import json
import os
from datetime import datetime, timedelta

config = boto3.client('config')
cloudformation = boto3.client('cloudformation')
organizations = boto3.client('organizations')
sts = boto3.client('sts')
ec2 = boto3.client('ec2')

COMPLIANT = 'COMPLIANT'
NON_COMPLIANT = 'NON_COMPLIANT'
COMPLIANT_STATUS = ['CURRENT', 'RUNNING']

MAX_EVALS_PER_REQUEST = 100


def tags_to_map(tags):
    tags_map = {}
    for tag in tags:
        tags_map[tag['Key']] = tag['Value']
    return tags_map


class Validation:
    def __init__(self, event, stack_set, evaluations):
        self.event = event
        self.stack_set = stack_set
        self.stack_set_name = stack_set['StackSetName']
        self.result_token = event['resultToken']
        self.invoking_event = json.loads(event['invokingEvent'])
        self.tags = tags_to_map(self.stack_set['Tags'])
        self.evaluations = evaluations

    def add_evaluation(self, resource_id, compliance, annotation):
        self.evaluations.append({
            'ComplianceResourceType': 'AWS::CloudFormation::Stack',
            'ComplianceResourceId': resource_id,
            'ComplianceType': compliance,
            'Annotation': annotation,
            'OrderingTimestamp': self.invoking_event['notificationCreationTime']
        })


def send_evaluations(evaluations, result_token):
    evaluations_length = len(evaluations)
    print('Evaluations: {}'.format(evaluations_length))
    for x in range(0, evaluations_length, MAX_EVALS_PER_REQUEST):
        put_evaluations = evaluations[x:x + MAX_EVALS_PER_REQUEST]
        print('Sending Evaluations: {}'.format(len(put_evaluations)))
        put_evaluation_options = dict(Evaluations=put_evaluations,
                                      ResultToken=result_token)
        print(config.put_evaluations(**put_evaluation_options))
    print('Sent Evaluations')


def handle_validation(validation_type, event):
    stack_sets = [s['StackSetName'] for s in cloudformation.list_stack_sets(Status='ACTIVE')['Summaries']]
    evaluations = []
    for stack_set_name in stack_sets:
        print('----- StackSet {}:  ---------'.format(stack_set_name))
        stack_set = cloudformation.describe_stack_set(
            StackSetName=stack_set_name
        )['StackSet']
        validation_type(event, stack_set, evaluations).validate()
    send_evaluations(evaluations, event['resultToken'])


def validatestacksetuptodate(event, context):
    handle_validation(CrossAccountStackSetValidation, event)


def validatestacksetdeployments(event, context):
    handle_validation(InstanceDeploymentValidation, event)


class CrossAccountStackSetValidation(Validation):
    def validate(self):
        validation_account = self.tags.get('ComparisonAccount', '')
        validation_stack_set_name = self.tags.get('ComparisonStackSetName', '')
        grace_period = int(self.tags.get('GracePeriod') or '14')
        commit_id = self.tags.get('CommitId', '')
        commit_count = int(self.tags.get('CommitCount', '0'))
        last_updated = self.tags.get('LastUpdated', '')
        print('ComparisonAccount: {}'.format(validation_account))
        print('ComparisonStackSetName: {}'.format(validation_stack_set_name))
        if validation_account or validation_stack_set_name:
            describe_client = cloudformation
            if validation_account:
                target_role = 'arn:aws:iam::{}:role/CrossAccountStackSetVerificationTargetRole'.format(
                    validation_account)
                response = sts.assume_role(
                    RoleArn=target_role,
                    RoleSessionName='CrossAccountStackSetValidation',
                )
                credentials = response['Credentials']
                describe_client = boto3.client('cloudformation',
                                               aws_access_key_id=credentials['AccessKeyId'],
                                               aws_secret_access_key=credentials['SecretAccessKey'],
                                               aws_session_token=credentials['SessionToken'])
            stack_set = describe_client.describe_stack_set(
                StackSetName=validation_stack_set_name or self.stack_set_name
            )['StackSet']
            tags = tags_to_map(stack_set.get('Tags', {}))
            target_commit_id = tags.get('CommitId') or ''
            target_commit_count = tags.get('CommitCount', '0')
            try:
                target_commit_count = int(target_commit_count)
            except ValueError:
                print('CommitCount is not a valid number {}'.format(target_commit_count))

            print('CommitId: {}'.format(commit_id))
            print('CommitCount: {}'.format(commit_count))
            print('TargetCommitId: {}'.format(target_commit_id))
            print('TargetCommitCount: {}'.format(target_commit_count))
            print('LastUpdated: {}'.format(last_updated))
            print('GracePeriod: {}'.format(grace_period))

            if (not target_commit_id or not target_commit_count) or (
                    target_commit_id != commit_id and commit_count <= target_commit_count):
                timestamp = datetime.fromisoformat(last_updated)
                with_grace_period = datetime.now() - timedelta(days=grace_period)
                if timestamp < with_grace_period:
                    annotation = 'StackSet {}: CommitId and Count not matching and not within Grace Period of {} days'
                    compliance = NON_COMPLIANT
                else:
                    annotation = 'StackSet {}: CommitId and Count not matching, but within Grace Period of {} days'
                    compliance = COMPLIANT
            else:
                annotation = 'StackSet {}: CommitId and Count matching so StackSet is up to date'
                compliance = COMPLIANT
            formatted_annotation = annotation.format(self.stack_set_name, grace_period)
            print('{}: {}'.format(formatted_annotation, compliance))
            self.add_evaluation(self.stack_set_name, compliance, formatted_annotation)


class InstanceDeploymentValidation(Validation):
    def validate(self):
        if self.tags.get('ValidateAllAccounts'):
            accounts = all_accounts()
        elif self.tags.get('ValidateMainAccount'):
            accounts = [os.environ['AccountId']]
        elif self.tags.get('ValidateAllSubAccounts'):
            accounts = [a for a in all_accounts() if a != os.environ['AccountId']]
        elif (self.tags.get('ValidateAccounts')):
            accounts = self.tags.get('Accounts').split('/')
        elif (self.tags.get('ValidateExcludedAccounts')):
            excluded_accounts = self.tags.get('ExcludedAccounts').split('/')
            accounts = [a for a in all_accounts() if a not in excluded_accounts]
        else:
            accounts = []

        if self.tags.get('ValidateAllRegions'):
            regions = all_regions()
        elif (self.tags.get('ValidateRegions')):
            regions = self.tags.get('ValidateRegions').split('/')
        elif (self.tags.get('ValidateExcludedRegions')):
            excluded_regions = self.tags.get('ValidateExcludedRegions').split('/')
            regions = [r for r in all_regions() if r not in excluded_regions]
        else:
            regions = []

        print('Accounts: {}:'.format(accounts))
        print('Regions: {}:'.format(regions))

        expected_instances = []
        for account in accounts:
            for region in regions:
                expected_instances.append((account, region))

        deployed_instances = all_stack_instances(StackSetName=self.stack_set_name)
        print('Deployed Instances: {}'.format(len(deployed_instances)))

        for expected_instance in expected_instances:
            if expected_instance not in deployed_instances.keys():
                compliance = NON_COMPLIANT
                message = 'StackSet {} needs to be deployed to account {} in region {}'
            else:
                status = deployed_instances[expected_instance]
                if status in COMPLIANT_STATUS:
                    compliance = COMPLIANT
                    message = 'StackSet {} is successfully deployed to account {} in region {}'
                else:
                    compliance = NON_COMPLIANT
                    message = 'StackSet {} is deployed but not in status CURRENT in account {} and region {}'
            options = self.stack_set_name, expected_instance[0], expected_instance[1]
            self.add_evaluation('{}-{}-{}'.format(*options),
                                compliance,
                                message.format(
                                   *options))

        if expected_instances:
            for instance in (deployed_instances.keys() - expected_instances):
                self.add_evaluation('{}-{}-{}'.format(self.stack_set_name, instance[0], instance[1]),
                                    NON_COMPLIANT,
                                   'StackSet {} is deployed but not defined in tags in account {} and region {}'.format(
                                       self.stack_set_name, instance[0], instance[1]))
        else:
            for instance, status in deployed_instances.items():
                if status in COMPLIANT_STATUS:
                    compliance = COMPLIANT
                    message = 'StackSet {} not configured in tags but successfully deployed to account {} in region {}'
                else:
                    compliance = NON_COMPLIANT
                    message = 'StackSet {} is deployed but in Status {status} in account {} and region {}'
                options = [self.stack_set_name, instance[0], instance[1]]
                self.add_evaluation('{}-{}-{}'.format(*options),
                                    compliance,
                                    message.format(*options, status=status))


def all_stack_instances(StackSetName, **Parameters):
    # TODO use Paginator for listing StackSet Instances
    result = cloudformation.list_stack_instances(StackSetName=StackSetName, **Parameters)
    instances = {}
    for i in result['Summaries']:
        instances[(i['Account'], (i['Region']))] = i['Status']
    if result.get('NextToken'):
        instances = {**instances, **all_stack_instances(StackSetName=StackSetName, NextToken=result['NextToken'])}
    return instances


def all_accounts():
    return [a['Id'] for a in organizations.list_accounts()['Accounts'] if a['Status'] == 'ACTIVE']


def all_regions():
    return [r['RegionName'] for r in ec2.describe_regions()['Regions']]
