<!-- Test event -->
In this section, we will start testing the event.

<!-- Contract for Property 111 -->
In this test, we will use EventBridge to submit an event to the bus. After the event is submitted, expect a record show up in the ContractStatusTable table in the draft.

# NOTE
Make sure the event bus name matches you contract bus  name in the test  files. e.g

      "EventBusName": "UnicornPropertiesEventBus-Local" (wrong)

      "EventBusName": "UnicornPropertiesBus-local",  (correct)

1. Run the following command to put an event into the event bus:

    aws events put-events --entries file://./tests/unit/events/eventbridge/contract_status_changed_event_contract_1_draft.json

2. Open the DynamoDB Item Explorer  console.

3. Select table that starts with uni-prop-properties-service-local-ContractStatusTable-

4. Confirm that you can now see a record corresponding to property 111 with a DRAFT status.

<!-- Contract for Property 222 - DRAFT -->
Let's use another new contract, but this time, for property 222. After the event is submitted, expect another record in the ContractStatusTable table with a DRAFT status.

1. Run the following command to put an event into the event bus:   

    aws events put-events --entries file://./tests/unit/events/eventbridge/contract_status_changed_event_contract_2_draft.json

2. Open the DynamoDB Item Explorer  console.

3. Select table that starts with uni-prop-local-properties-ContractStatusTable-

4. Confirm that you can now see a new record corresponding to property 222 with a DRAFT status.

<!-- Contract for Property 222 - changed to APPROVED -->
Now let's simulate changing the contract for property 222 to APPROVED. After the event is submitted, expect no new records in the ContractStatusTable, but the existing contract for property 222 changed to APPROVED.

1. Run the following command to put an event into the event bus:    

    aws events put-events --entries file://./tests/unit/events/eventbridge/contract_status_changed_event_contract_2_approved.json

2. Open the DynamoDB Item Explorer  console.

3. Select table that starts with uni-prop-local-properties-ContractStatusTable-

4. Confirm that you can now see the existing record corresponding to property 222 with the status changed to APPROVED

# Done
Congratulations! You have successfully used schema registry to download the appropriate code binding for the ContractStatusChanged event, use it to consume the event and take appropriate action - which in this case, save the status of the contract in the DynamoDB table.