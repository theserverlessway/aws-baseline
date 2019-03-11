import boto3
import copy
import os

organizations = boto3.client('organizations')

REPLACE_KEYS = {
    'Id': 'ACCOUNT_ID',
    'Name': 'ACCOUNT_NAME',
    'Email': 'ACCOUNT_EMAIL'
}


def replace(string, account):
    for key, value in REPLACE_KEYS.items():
        string = string.replace(value, account[key])
    return string


def walk_resource(resource, account):
    if type(resource) is list:
        items = enumerate(resource)
    elif type(resource) is dict:
        items = resource.items()
    else:
        print('Unsupported Type')
        print(type(resource))
        raise
    for index, value in items:
        if type(value) is str:
            resource[index] = replace(value, account)
        else:
            walk_resource(value, account)
    return resource


def handle_resources(resource_templates, account):
    resources = {}
    for key, resource in resource_templates.items():
        if not any(replacer in key for replacer in REPLACE_KEYS.values()):
            resources[key] = resource
        else:
            new_key = replace(key, account)
            new_resource = copy.deepcopy(resource)
            walk_resource(new_resource, account)
            resources[new_key] = new_resource
    return resources


def handler(event, context):
    print(event)
    fragment = copy.deepcopy(event['fragment'])
    resources = event['fragment']['Resources']
    new_resources = {}
    acc = org_accounts(event['transformId'])
    for account in acc:
        new_resources.update(handle_resources(resources, account))
    fragment['Resources'] = new_resources
    return {
        "requestId": event['requestId'],
        "status": 'success',
        "fragment": fragment
    }


def org_accounts(transform_id):
    ACCOUNT_ID = os.environ['AccountId']
    accounts = organizations.list_accounts()['Accounts']
    with_master = 'WithMaster' in transform_id

    accounts = [a for a in accounts if a['Status'] == 'ACTIVE' and (
        with_master or (not with_master and a['Id'] != ACCOUNT_ID))]
    return accounts


def account_list(event, context):
    print(event)
    accounts = [account['Id'] for account in org_accounts(event['transformId'])]
    return {
        "requestId": event['requestId'],
        "status": 'success',
        "fragment": accounts
    }
