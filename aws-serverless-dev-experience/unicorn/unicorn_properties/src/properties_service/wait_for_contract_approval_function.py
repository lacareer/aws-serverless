# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os

import boto3
from botocore.exceptions import ClientError

from properties_service.exceptions import ContractStatusNotFoundException


# Initialise Environment variables
if (SERVICE_NAMESPACE := os.environ.get("SERVICE_NAMESPACE")) is None:
    raise InternalServerError("SERVICE_NAMESPACE environment variable is undefined")
if (CONTRACT_STATUS_TABLE := os.environ.get("CONTRACT_STATUS_TABLE")) is None:
    raise InternalServerError("CONTRACT_STATUS_TABLE environment variable is undefined")

# Initialise boto3 clients
# sfn = boto3.client('stepfunctions')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(CONTRACT_STATUS_TABLE)  # type: ignore


def lambda_handler(event, context):
    """Function checks to see whether the contract status exists and waits for APPROVAL
    by updating contract status with task token.

    Parameters
    ----------
    event: dict, required
        Event passed into

    context: object
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
        The same input event file
    """

    task_token: str = event['TaskToken']
    detail: dict = event['Input']

    try:
        contract_status = get_contract_status(detail["property_id"])
        update_token_and_pause_execution(task_token=task_token,
            property_id=contract_status["property_id"])
        return detail
    except ContractStatusNotFoundException as error:
        print("Cannot approve a property that does not exist.")
        raise error

def get_contract_status(property_id: str) -> dict:
    """Returns contract status for a specified property

    Parameters
    ----------
    property_id : str
        Property ID

    Returns
    -------
    dict
        Contract info
    """

    try:
        response = table.get_item(
            Key={
                'property_id': property_id
            }
        )
        return response["Item"]

    except ClientError as error:
        if error.response["Error"]["Code"] == "ResourceNotFoundException":
            print("Error getting contract.")
            raise ContractStatusNotFoundException() from error
        raise error
    except KeyError as _:
        raise ContractStatusNotFoundException() from _


def update_token_and_pause_execution(task_token: str, property_id: str):
    """Update the Contract status table with task token for this state.

    Parameters
    ----------
    task_token : str
        AWS Step Functions task token
    property_id : str
        Property ID
    """
    table.update_item(
        Key={'property_id': property_id},
        UpdateExpression="set sfn_wait_approved_task_token = :g",
        ExpressionAttributeValues={
                ':g': task_token
        },
        ReturnValues='ALL_NEW'
    )
