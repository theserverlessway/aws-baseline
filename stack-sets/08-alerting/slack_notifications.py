import json
from urllib.request import Request, urlopen
from os import environ




def post_to_slack(event, context):
    actual_message = event[u'Records'][0][u'Sns'][u'Message']

    message = json.loads(actual_message)
    slack_message = message

    if isinstance(message, dict):
        slack_message = json.dumps(message, sort_keys=True, indent=4)
        for key, func in MessageIdentifiers.items():
            if type(key) == tuple:
                if message.get(key[0]) == key[1]:
                    slack_message = func(message)
                    break
            else:
                if message.get(key):
                    slack_message = func(message)
                    break

    data = {
        'text': slack_message,
        'username': 'Notification'}

    webhook_url = environ['SLACK_WEBHOOK_URL']
    request = Request(webhook_url, json.dumps(data).encode("UTF-8"))
    request.add_header('Content-Type', 'application/json')
    urlopen(request)


def alarm(message):
    alarm_name = message['AlarmName']
    account_id = message['AWSAccountId']
    new_state_value = message['NewStateValue']
    new_state_reason = message['NewStateReason']
    return "`%s` on AWS account `%s` switched to state `%s` due to: \\n`%s` \\n" % (
        alarm_name, account_id, new_state_value, new_state_reason)


def config_event(message):
    detail = message['detail']
    resource_type = detail['resourceType']
    resource_id = detail['resourceId']
    aws_region = detail['awsRegion']
    aws_account_id = detail['awsAccountId']
    message_string = "`{}` with Id `{}` on AWS account `{}` in Region `{}` became NON_COMPLIANT"
    return message_string.format(resource_type, resource_id, aws_account_id, aws_region)


MessageIdentifiers = {
    'AlarmName': alarm,
    ('detail-type', 'Config Rules Compliance Change'): config_event
}
