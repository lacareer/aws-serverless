<!-- Save code bindings -->
In this section, you will download the code bindings for the ContractStatusChanged event and uploading it to your IDE.

1. Navigate to Amazon EventBridge -> Schemas -> unicorn.contracts 

2. Select unicorn.contracts@ContractStatusChanged schema

3. Download code bindings for the appropriate language

4. Unzip the contents, copy the schema/unicorn_contracts_local folder to the property_service/src/schema directory. For Java language, copy the schema/unicorn_contracts_local folder to unicorn_properties/PropertyFunctions/src/main/java/schema. Create schema directory if it does not exist.

<!-- Save the contract status -->

Make the following updates to the src/properties/contract_status_changed_event_handler.py file.

1. Add the import statements to the start of the page

    from schema.unicorn_contracts_local.contractstatuschanged import (AWSEvent, ContractStatusChanged, Marshaller)
    OR
    from schema.unicorn_contracts_local.contractstatuschanged import AWSEvent, ContractStatusChanged, Marshaller

2. Before returning the 200 OK, deserialise the event to a strongly typed object, then call the save_contract_status by passing the ContractStatusChanged object.

    #Deserialize event into strongly typed object
    awsEvent:AWSEvent = Marshaller.unmarshall(event, AWSEvent)
    detail:ContractStatusChanged = awsEvent.detail
    save_contract_status(detail)