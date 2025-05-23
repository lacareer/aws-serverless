# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os

# Initialise Environment variables
if (SERVICE_NAMESPACE := os.environ.get("SERVICE_NAMESPACE")) is None:
    raise EnvironmentError("SERVICE_NAMESPACE environment variable is undefined")


def lambda_handler(event, context):
    """Validates the integrity of the property content

    Parameters
    ----------
    event : dict
        Payload from Step functions containing the results of the Rekognition and Comprehend analysis
    context : dict
        AWS Lambda context

    Returns
    -------
    dict
        Original payload with additional validation result.
    """

    status = "PASS"

    # Check for Image moderation results
    for imageModerations in event["imageModerations"]:
        if len(imageModerations["ModerationLabels"])>0:
            status = "FAIL"
            break

    ##check for contentSentiment
    if event["contentSentiment"]["Sentiment"] != "POSITIVE":
        status = "FAIL"

    # append the result
    event["validation_result"] = status

    ## return the event
    return event
