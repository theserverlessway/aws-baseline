import boto3
import os
from time import sleep
from datetime import datetime, timedelta

TableName = os.environ['PartitionCheckTable']
GlueTable = os.environ['CloudTrailTable']
AthenaQueryResults = os.environ['AthenaQueryResults']
AuditingGlueDatabaseName = os.environ['AuditingGlueDatabaseName']

dynamo = boto3.client('dynamodb')
athena = boto3.client('athena')


def handler(event, context):
    key = event['Records'][0]['s3']['object']['key']
    # Hadoop creates temporary files with '%folder%' in the name and we shouldn't react to those
    if 'folder%' in key:
        return
    bucket = event['Records'][0]['s3']['bucket']['name']
    print('S3 Object: s3://{}/{}'.format(bucket, key))
    keys = key.split('/')
    account = keys[1]
    region = keys[3]
    year = keys[4]
    month = keys[5]
    day = keys[6]
    dynamo_key = '-'.join([bucket, account, region, year, month, day])
    date = '{}-{}-{}'.format(year, month, day)
    ddb_item = {
        'partition': {
            'S': dynamo_key
        }
    }
    dynamo_result = dynamo.get_item(
        TableName=TableName,
        Key=ddb_item
    )
    if dynamo_result.get('Item'):
        print('Already added Partition for {}'.format(dynamo_key))
    else:
        partition_location = '/'.join(keys[0:-1])
        print('Adding Partition for {}'.format(dynamo_key))
        query = "ALTER TABLE {database_name}.{table_name} ADD PARTITION (account='{account}',region='{region}',date='{date}') LOCATION 's3://{bucket}/{partition_location}'".format(
            database_name=AuditingGlueDatabaseName,
            table_name=GlueTable,
            account=account,
            region=region,
            date=date,
            bucket=bucket,
            partition_location=partition_location
        );
        print(query)
        athena_query = athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': AuditingGlueDatabaseName
            },
            ResultConfiguration={
                'OutputLocation': "s3://{}".format(AthenaQueryResults)
            }
        )
        while True:
            athena_query_result = athena.get_query_execution(QueryExecutionId=athena_query['QueryExecutionId'])
            athena_query_status = athena_query_result['QueryExecution']['Status']['State']
            if athena_query_status not in ['QUEUED', 'RUNNING']:
                break
            sleep(2)
        if athena_query_status == 'SUCCEEDED' or 'Partition already exists' in athena_query_result['QueryExecution']['Status']['StateChangeReason']:
            dynamo.put_item(
                TableName=TableName,
                Item={
                    'partition': {
                        'S': dynamo_key
                    },
                    'ttl': {
                        'N': str(int((datetime.now() + timedelta(weeks=4)).timestamp()))
                    }
                }
            )
        else:
            print(athena_query_result)
            raise Exception('Athena Query failed')
