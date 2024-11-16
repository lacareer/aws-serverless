<!-- Test out the workflow -->
In this section, we will be testing a few scenarios:

- Check if the workflow fails when a contract does not exist.
- Check if inappropriate description is flagged
- Check if inappropriate images are flagged
- Check if the workflow pauses if the contract is not approved
- Check if the workflow automatically progresses when the contract is approved
- Check if the workflow fully completes without pauses for an approved contract

Let's take it step by step.

<!-- Check if the workflow fails when a contract does not exist -->
1. Run the following command to send an event with a contract that does not exist. Run:

    aws events put-events --entries file://./tests/events/eventbridge/publicaction_approval_requested_event_non_existing_contract.json

2. Open the Step Functions  console.

3. Select state machine with name uni-prop-local-properties-ApprovalStateMachine.

4. Select the latest execution from the Executions tab.

You will now see that the workflow will fail, while moving to the NotFound path.  

# I stopped here and did not complete the testing as I kelpt getting AWS Rekognition error.
# Please try to figure this out later
<!-- Check if inappropriate description is flagged -->
Run the following command to send an event with a contract that exists, but contains inappropriate description.

    aws events put-events --entries file://./tests/events/eventbridge/publicaction_approval_requested_event_inappropriate_description.json

1. Open the Step Functions  console.

2. Select state machine with name uni-prop-local-properties-ApprovalStateMachine.

3. Select the latest execution from the Executions tab.

You will now see that the workflow will pass, but will take the Declined path because the description was inappropriate

<!-- Check if inappropriate images are flagged -->
Run the following command to send an event with a contract that exists, content is good, but it contains inappropriate images. Run:

    aws events put-events --entries file://./tests/events/unit/eventbridge/publicaction_approval_requested_event_inappropriate_description.json

1. Open the Step Functions  console.

2. Select state machine with name uni-prop-local-properties-ApprovalStateMachine.

3. Select the latest execution from the Executions tab.  

You will now see that the workflow will pass, but will take the Declined path because one of the images was inappropriate.

<!-- Check if the workflow pauses if the contract is not approved -->
Run the following command to send an event with everything perfect, but the contract is not APPROVED yet. So we expect at this stage, the workflow to pause.
Run:
    aws events put-events --entries file://./tests/events/unit/eventbridge/publicaction_approval_requested_event_pause_workflow.json

1. Open the Step Functions  console.

2. Select state machine with name uni-prop-local-properties-ApprovalStateMachine.

3. Select the latest execution from the Executions tab.    

You will now see that the workflow will pause, waiting for the contract to be approved.

<!-- Check if the workflow automatically progresses when the contract is approved -->
Run the following command to send an event that will approve the contract that is related to this property.

1. Open the Step Functions  console.

2. Select state machine with name uni-prop-local-properties-ApprovalStateMachine.

3. Select the latest execution from the Executions tab. 

You will now see that the workflow resume from where it left off, and move on to approved.

<!-- Check if the workflow fully completes without pauses for an approved contract -->
Run the following command to send an event with everything perfect - no issues. We expect no pauses, but a full "approved" path.

1. Open the Step Functions  console.

2. Select state machine with name uni-prop-local-properties-ApprovalStateMachine.

3. Select the latest execution from the Executions tab. 

You will now see that the workflow will run to completion, without any pauses, and end up being approved.

# Done
Congratulations! You have successfully used Step Functions Workflow Studio to build a full-fledged workflow visually from scratch. 
You have then incorporated the resulting template into your codebase, and deployed using AWS SAM CLI via a makefile. 
Then you have tested the workflow to make sure that the changes work as expected.