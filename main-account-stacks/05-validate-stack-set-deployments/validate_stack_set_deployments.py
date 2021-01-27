# To fit into the Lambda this code is minified

import boto3
import json
import os

c = boto3.client('config')
cf = boto3.client('cloudformation')
sts = boto3.client('sts')
ec2 = boto3.client('ec2')

C = 'COMPLIANT'
NC = 'NON_COMPLIANT'
CS = ['CURRENT', 'RUNNING']

M = 100

LIST_ACCOUNTS = ['268875736166', '206924800932', '815637454826']

def o(k):
    return os.environ.get(k, '')


def p(f, **o):
    print(o)
    while True:
        r = f(**o)
        n = r.get('NextToken')
        if n:
            o['NextToken'] = n
            return [r] + p(f, **o)
        else:
            return [r]


def ae(resource_id, compliance, annotation, evaluations, invoking_event):
    evaluations.append({
        'ComplianceResourceType': 'AWS::CloudFormation::Stack',
        'ComplianceResourceId': resource_id,
        'ComplianceType': compliance,
        'Annotation': annotation,
        'OrderingTimestamp': invoking_event['notificationCreationTime']
    })


def se(evaluations, result_token):
    el = len(evaluations)
    print(el)
    for x in range(0, el, M):
        put_evaluations = evaluations[x:x + M]
        put_evaluation_options = dict(Evaluations=put_evaluations,
                                      ResultToken=result_token)
        print(c.put_evaluations(**put_evaluation_options))


def vs(event, context):
    evaluations = []
    # TODO Use Paginator when available
    sse = [s['StackSetName'] for page in p(cf.list_stack_sets, Status='ACTIVE') for s in page['Summaries']]
    print(sse)
    for sn in sse:
        print(sn)
        v(event, sn, cf.describe_stack_set(
            StackSetName=sn
        )['StackSet'], evaluations)
    se(evaluations, event['resultToken'])


def v(e, sn, ss, ev):
    inv = json.loads(e['invokingEvent'])
    t = {tag['Key']: tag['Value'] for tag in ss['Tags']}
    if t.get('ValidateAllAccounts'):
        ac = aa()
    elif t.get('ValidateMainAccount'):
        ac = [os.environ['AccountId']]
    elif t.get('ValidateAllSubAccounts'):
        ac = [a for a in aa() if a != os.environ['AccountId']]
    elif (t.get('ValidateAccounts')):
        ac = t.get('Accounts').split('/')
    elif (t.get('ValidateExcludedAccounts')):
        ac = [a for a in aa() if a not in t.get('ExcludedAccounts').split('/')]
    else:
        ac = []

    if t.get('ValidateAllRegions'):
        re = ar()
    elif t.get('ValidateRegions'):
        re = t.get('ValidateRegions').split('/')
    elif t.get('ValidateExcludedRegions'):
        re = [r for r in ar() if r not in t.get('ValidateExcludedRegions').split('/')]
    else:
        re = []

    exp = [(a, r) for a in ac for r in re]
    # TODO Switch to Paginator
    di = {(i['Account'], (i['Region'])): i['Status'] for page in
          p(cf.list_stack_instances, StackSetName=sn) for i in page['Summaries']}
    print(f'Expected: {exp}')
    print(f'Deployed: {di}')

    for ei in exp:
        if ei not in di.keys():
            compliance = NC
            message = o('NC1')
        else:
            s = di[ei]
            if s in CS:
                compliance = C
                message = o('C1')
            else:
                compliance = NC
                message = o('NC2')
        options = sn, ei[0], ei[1]
        ae('{}-{}-{}'.format(*options),
           compliance,
           message.format(
               *options), ev, inv)

    if exp:
        for i in set(di.keys()) - set(exp):
            ae('{}-{}-{}'.format(sn, i[0], i[1]),
               NC,
               o('NC3').format(
                   sn, i[0], i[1]), ev, inv)
    else:
        for i, s in di.items():
            if s in CS:
                compliance = C
                message = o('C2')
            else:
                compliance = NC
                message = o('NC4')
            options = [sn, i[0], i[1]]
            ae('{}-{}-{}'.format(*options),
               compliance,
               message.format(*options, status=s), ev, inv)


def aa():
    #return [a['Id'] for a in org.list_accounts()['Accounts'] if a['Status'] == 'ACTIVE']
    return [a['Id'] for a in LIST_ACCOUNTS if a['Status'] == 'ACTIVE']


def ar():
    return [r['RegionName'] for r in ec2.describe_regions()['Regions']]
