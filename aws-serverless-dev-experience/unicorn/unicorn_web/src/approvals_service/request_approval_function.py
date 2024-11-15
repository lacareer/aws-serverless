# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
from typing import Tuple
import os
import re
import json

import boto3
from botocore.exceptions import ClientError

# Initialise Environment variables
if (SERVICE_NAMESPACE := os.environ.get('SERVICE_NAMESPACE')) is None:
    raise EnvironmentError('SERVICE_NAMESPACE environment variable is undefined')
if (DYNAMODB_TABLE := os.environ.get('DYNAMODB_TABLE')) is None:
    raise EnvironmentError('DYNAMODB_TABLE environment variable is undefined')
if (EVENT_BUS := os.environ.get('EVENT_BUS')) is None:
    raise EnvironmentError('EVENT_BUS environment variable is undefined')

EXPRESSION = r"[a-z-]+\/[a-z-]+\/[a-z][a-z0-9-]*\/[0-9-]+"
TARGET_STATE = 'PENDING'

# Initialise boto3 clients
event_bridge = boto3.client('events')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE)  # type: ignore


def publish_event(detail_type, resources, detail):
    try:
        entry = {'EventBusName': EVENT_BUS,
                 'Source': SERVICE_NAMESPACE,
                 'DetailType': detail_type,
                 'Resources': resources,
                 'Detail': json.dumps(detail)}
        print(entry)

        response = event_bridge.put_events(Entries=[entry])
        print(response)
    except ClientError as e:
        error_msg = f"Unable to send event to Event Bus: {e}"
        print(error_msg)
        raise Exception(error_msg)

    failed_count = response['FailedEntryCount']

    if failed_count > 0:
        error_msg = f"Error sending requests to Event Bus; {failed_count} message(s) failed"
        print(error_msg)
        raise Exception(error_msg)

    entry_count = len(response['Entries'])
    print(f"Sent event to EventBridge; {failed_count} records failed; {entry_count} entries received")
    return response


def get_property(pk: str, sk: str) -> dict:
    response = table.get_item(
        Key={ 'PK': pk, 'SK': sk },
        AttributesToGet=['currency', 'status', 'listprice', 'contract', 
                         'country', 'city', 'number', 'images',
                         'description', 'street']
    )
    if 'Item' not in response:
        print(f"No item found in table {DYNAMODB_TABLE} with PK {pk} and SK {sk}")
        return dict()

    return response['Item']


def get_keys_for_property(property_id: str) -> Tuple[str, str]:
    # Validate Property ID
    if not re.fullmatch(EXPRESSION, property_id):
        error_msg = f"Invalid property id '{property_id}'; must conform to regular expression: {EXPRESSION}"
        print(error_msg)
        return '', ''

    # Extract components from property_id
    country, city, street, number = property_id.split('/')

    # Construct DDB PK & SK keys for this property
    pk_details = f"{country}#{city}".replace(' ', '-').lower()
    pk = f"PROPERTY#{pk_details}"
    sk = f"{street}#{str(number)}".replace(' ', '-').lower()
    return pk, sk


def request_approval(raw_data: dict):
    property_id = raw_data['property_id']

    # Validate property_id, parse it and extract DynamoDB PK/SK values
    pk, sk = get_keys_for_property(property_id=property_id)
    # Get property details from database
    item = get_property(pk=pk, sk=sk)

    if (status := item.pop('status')) in [ 'APPROVED' ]:
        print(f"Property '{property_id}' is already {status}; no action taken")
        return

    item['property_id'] = property_id
    item['address'] = {
        'country': item.pop('country'),
        'city': item.pop('city'),
        'street': item.pop('street'),
        'number': int(item.pop('number')),
    }
    item['status'] = TARGET_STATE
    item['listprice'] = int(item['listprice'])

    publish_event(detail_type='PublicationApprovalRequested', resources=[property_id], detail=item)


def lambda_handler(event: dict, context: dict):
    # Multiple records can be delivered in a single event
    for record in event['Records']:
        request_approval(json.loads(record['json_body']))
