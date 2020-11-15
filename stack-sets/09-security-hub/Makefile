#!/usr/bin/env bash

#usage: enablesecurityhub.py [-h] --master_account MASTER_ACCOUNT --assume_role
#                          ASSUME_ROLE
#                          input_file
#
#Link AWS Accounts to central Security Hub Account
#
#positional arguments:
#  input_file            Path to CSV file containing the list of account IDs
#                        and Email addresses
#
#optional arguments:
#  -h, --help            show this help message and exit
#  --master_account MASTER_ACCOUNT
#                        AccountId for Central AWS Account
#  --assume_role ASSUME_ROLE
#                        Role Name to assume in each account
#  --enabled_regions ENABLED_REGIONS
#                        comma separated list of regions to enable SecurityHub.
#                        If not specified, all available regions are enabled
#  --enable_standards ENABLE_STANDARDS
#                        comma separated list of standards ARNs to enable (ex: arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0 )
#  
#2b. Disable Security Hub
#Copy the required CSV file to this directory
#Should be in the formation of "AccountId,EmailAddress,..."
#usage: disablesecurityhub.py [-h] --master_account MASTER_ACCOUNT
#                             --assume_role ASSUME_ROLE [--delete_master]
#                             [--enabled_regions ENABLED_REGIONS]
#                             [--disable_standards_only DISABLE_STANDARDS_ONLY]
#                             input_file
#
#Disable and unlink AWS Accounts from central SecurityHub Account
#
#positional arguments:
#  input_file            Path to CSV file containing the list of account IDs
#                        and Email addresses
#
#optional arguments:
#  -h, --help            show this help message and exit
#  --master_account MASTER_ACCOUNT
#                        AccountId for Central AWS Account
#  --assume_role ASSUME_ROLE
#                        Role Name to assume in each account
#  --delete_master       Disable SecurityHub in Master
#  --enabled_regions ENABLED_REGIONS
#                        comma separated list of regions to remove SecurityHub.
#                        If not specified, all available regions disabled
#  --disable_standards_only DISABLE_STANDARDS_ONLY
#                        comma separated list of standards ARNs to disable (ie.
#                        arn:aws:securityhub:::ruleset/cis-aws-foundations-
#                        benchmark/v/1.2.0 )

CIS_STANDARD_RESOURCE='ruleset/cis-aws-foundations-benchmark/v/1.2.0'
CIS_STANDARD_ARN='arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0'
PCI_STANDARD_ARN="arn:aws:securityhub:ap-northeast-2::standards/pci-dss/v/3.2.1"

ACCOUNT_ID=$(shell aws sts get-caller-identity --output text --query Account)
ENABLED_REGIONS='ap-northeast-2'
INPUT_FILE='member.csv'

enablesecurityhub:
	/app/scripts/securityhub/enablesecurityhub.py --master_account ${ACCOUNT_ID} --enabled_regions ${ENABLED_REGIONS} --assume_role ManageSecurityHubRole ${INPUT_FILE} 

disablesecurityhub:
	/app/scripts/securityhub/disablesecurityhub.py --master_account ${ACCOUNT_ID} --enabled_regions ${ENABLED_REGIONS} --assume_role ManageSecurityHubRole ${INPUT_FILE}

disablesecurityhubmaster:
	/app/scripts/securityhub/disablesecurityhub.py --delete_master --master_account ${ACCOUNT_ID} --enabled_regions ${ENABLED_REGIONS} --assume_role ManageSecurityHubRole ${INPUT_FILE}