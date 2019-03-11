import pytest
import org_iterator
import os


EXAMPLE_FRAGMENT = {
    'Resources': {
        'DeveloperRoleACCOUNT_ID': {
            'Properties': {
                'Developer': 'ACCOUNT_ID',
                'Test': ['ACCOUNT_ID', 'ACCOUNT_NAME', 'ACCOUNT_EMAIL']
            },
            'Type': 'AWS::IAM::Role'
        },
        'Test': {
            'Properties': {
                'Admin': 'ACCOUNT_ID'
            },
            'Type': 'AWS::IAM::Role'
        }
    }
}

MASTER_ACCOUNT_ID = 'master'
ACCOUNT_ID = 'acc1'
ACCOUNT_ID_2 = 'acc2'


ACCOUNT_NAME = 'aa bb cc'
ACCOUNT_EMAIL = "test@test.com"
ACCOUNTS = {'Accounts': [
    {'Id': MASTER_ACCOUNT_ID, 'Name': ACCOUNT_NAME, 'Status': 'ACTIVE', 'Email': ACCOUNT_EMAIL},
    {'Id': ACCOUNT_ID, 'Name': ACCOUNT_NAME, 'Status': 'ACTIVE', 'Email': ACCOUNT_EMAIL},
    {'Id': ACCOUNT_ID_2, 'Name': ACCOUNT_NAME, 'Status': 'SUSPENDED', 'Email': ACCOUNT_EMAIL}]
}

RESPONSE = {
    'requestId': ACCOUNT_ID,
    'status': 'success',
    'fragment': {
        'Resources': {
            'DeveloperRole' + ACCOUNT_ID: {
                'Properties': {
                    'Developer': ACCOUNT_ID,
                    'Test': [ACCOUNT_ID, ACCOUNT_NAME, ACCOUNT_EMAIL]
                },
                'Type': 'AWS::IAM::Role'
            },
            'Test': {
                'Properties': {
                    'Admin': 'ACCOUNT_ID'
                },
                'Type': 'AWS::IAM::Role'
            }
        }
    }
}

RESPONSE_WITH_MASTER = {
    'requestId': ACCOUNT_ID,
    'status': 'success',
    'fragment': {
        'Resources': {
            'DeveloperRole' + ACCOUNT_ID: {
                'Properties': {
                    'Developer': ACCOUNT_ID,
                    'Test': [ACCOUNT_ID, ACCOUNT_NAME, ACCOUNT_EMAIL]
                },
                'Type': 'AWS::IAM::Role'
            },
            'DeveloperRole' + MASTER_ACCOUNT_ID: {
                'Properties': {
                    'Developer': MASTER_ACCOUNT_ID,
                    'Test': [MASTER_ACCOUNT_ID, ACCOUNT_NAME, ACCOUNT_EMAIL]
                },
                'Type': 'AWS::IAM::Role'
            },
            'Test': {
                'Properties': {
                    'Admin': 'ACCOUNT_ID'
                },
                'Type': 'AWS::IAM::Role'
            }
        }
    }
}

LIST_RESPONSE = {
    'requestId': ACCOUNT_ID,
    'status': 'success',
    'fragment': [ACCOUNT_ID]
}

LIST_RESPONSE_WITH_MASTER = {
    'requestId': ACCOUNT_ID,
    'status': 'success',
    'fragment': [MASTER_ACCOUNT_ID, ACCOUNT_ID]
}


@pytest.fixture
def organizations(mocker):
    os.environ['AccountId'] = MASTER_ACCOUNT_ID
    orgs = mocker.patch('org_iterator.organizations')
    orgs.list_accounts.return_value = ACCOUNTS
    return orgs


def test_iterate_accounts_for_resources(organizations):
    assert org_iterator.handler({'requestId': ACCOUNT_ID, 'fragment': EXAMPLE_FRAGMENT, 'transformId': 'MacroName'},
                                None) == RESPONSE


def test_iterate_accounts_with_master(organizations):
    assert org_iterator.handler({'requestId': ACCOUNT_ID, 'fragment': EXAMPLE_FRAGMENT,
                                 'transformId': 'MacroNameWithMaster'},
                                None) == RESPONSE_WITH_MASTER


def test_account_list(organizations):
    assert org_iterator.account_list({'requestId': ACCOUNT_ID, 'fragment': EXAMPLE_FRAGMENT,
                                      'transformId': 'MacroName'},
                                     None) == LIST_RESPONSE


def test_account_list_with_master(organizations):
    assert org_iterator.account_list({'requestId': ACCOUNT_ID, 'fragment': EXAMPLE_FRAGMENT,
                                      'transformId': 'MacroNameWithMaster'},
                                     None) == LIST_RESPONSE_WITH_MASTER
