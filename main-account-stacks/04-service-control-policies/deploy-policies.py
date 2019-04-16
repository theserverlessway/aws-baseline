import boto3
import sys
import glob

organizations = boto3.client('organizations')

if len(sys.argv) > 1:
    policy_files = sys.argv[1:]
else:
    policy_files = glob.glob('service-control-policies/*.scp.json')

policies = {file.replace('.scp.json', '').replace('service-control-policies/', ''): file for file in policy_files}

paginator = organizations.get_paginator('list_policies')
pages = [p['Policies'] for p in paginator.paginate(Filter='SERVICE_CONTROL_POLICY')]
deployed_policies = {item['Name']: item['Id'] for sublist in pages for item in sublist}

for policy, filename in policies.items():
    with open(filename, 'r') as f:
        parameters = dict(
            Content=f.read(),
            Description=policy,
            Name=policy
        )
    if policy in deployed_policies.keys():
        print('Updating Policy: {}'.format(policy))
        response = organizations.update_policy(
            PolicyId=deployed_policies[policy],
            **parameters
        )
    else:
        print('Creating Policy: {}'.format(policy))
        response = organizations.create_policy(
            **parameters,
            Type='SERVICE_CONTROL_POLICY'
        )
