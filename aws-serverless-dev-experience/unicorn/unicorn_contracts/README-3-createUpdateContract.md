<!-- Creating contracts -->
#### A closer look at the integration
Agents manage contract information by issuing two commands: CreateContract and UpdateContract. The Contract API that processes these requests exposes two methods, POST and PUT, on the Contracts resource, that represent creating and updating actions on the backend, respectively. These methods validate the expected payload with the CreateContractModel and UpdateContractModel.

Both commands are directive in nature, and have no reason to fail. An agent should reasonably expect that when they ask the service to create or update a Contract that will be dealt with, eventually. For this reason, we have implemented an asynchronous messaging pattern, integrating Amazon API Gateway with Amazon SQS.

The Integration requests for both methods are configured to send messages to a single queue. We differentiate the operation (whether to create or update the contract) by the HTTP method which we map as an SQS message attribute in the mapping template. The mapping template defines the SendMessage API action of the SQS service

<!-- update the create method  -->
Open unicorn_contracts/src/contracts_service/contract_event_handler.py and find the create_contract method. You will find that it does not have an implementation.

Copy the following method implementation, and update the method:


        def create_contract(event: dict) -> None:
            """Create contract inside DynamoDB table

            Execution logic:
                if contract does not exist
                or contract status is either of [ CANCELLED | CLOSED | EXPIRED]
                then
                    create or replace contract with status = DRAFT
                    log response
                    log trace info
                    return
                else
                    log exception message

            Parameters
            ----------
                contract (dict): _description_

            Returns
            -------
            dict
                DynamoDB put Item response
            """

            current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            contract = {
                "property_id":                  event["property_id"],  # PK
                "address":                      event["address"],
                "seller_name":                  event["seller_name"],
                "contract_created":             current_date,
                "contract_last_modified_on":    current_date,
                "contract_id":                  str(uuid.uuid4()),
                "contract_status":              ContractStatus.DRAFT.name,
            }

            print(f"Creating contract: {contract} From event: {event}")

            try:
                response = table.put_item(
                    Item=contract,
                    ConditionExpression=
                        Attr('property_id').not_exists()
                    | Attr('contract_status').is_in([
                        ContractStatus.CANCELLED.name,
                        ContractStatus.CLOSED.name,
                        ContractStatus.EXPIRED.name,
                        ]))
                print(f'var:response - "{response}"')
                
            except ClientError as e:
                code = e.response["Error"]["Code"]
                if code == 'ConditionalCheckFailedException':
                    print(f"""
                            Unable to create contract for Property {contract['property_id']}.
                            There already is a contract for this property in status {ContractStatus.DRAFT.name} or {ContractStatus.APPROVED.name}
                            """)
                else:
                    raise e


Ensure you have sam sync activated. Otherwise make sure you use sam build and sam deploy to update your code changes.

<!-- Testing the creation of new contracts -->
Let's test and make sure that the updates have worked and that the integrations with API Gateway, SQS, Lambda and DynamoDB are working.

Open your terminal and runt the following commands:

        export API=`aws cloudformation describe-stacks --stack-name uni-prop-local-contracts --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" --output text`     

From your cmd run:

    curl --location --request POST "${API}contracts" \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "address": {
    "country": "USA",
    "city": "Anytown",
    "street": "Main Street",
    "number": 111
    },
    "seller_name": "John Doe",
    "property_id": "usa/anytown/main-street/111"
    }'

Verify that the record has been written to the DynamoDB table. The Contract Status should be set to DRAFT.

<!-- Updating Contracts -->
Now that the functionality for creating functions has been verified, let implement the updates of contracts.

Open unicorn_contracts/src/contracts_service/contract_event_handler.py and find the update_contract method. You will find that it does not have an implementation.

Copy the following method implementation, and update the method:

    def update_contract(contract: dict) -> None:
        """Update an existing contract inside DynamoDB table

        Execution logic:

            if  contract exists exist
            and contract status is either of [ DRAFT ]
            then
                update contract status to APPROVED
                log response
                log trace info
                return
            else
                log exception message

        Parameters
        ----------
            contract (dict): _description_

        Returns
        -------
        dict
            DynamoDB put Item response
        """

        print(f"Updating contract: {contract}")

        try:
            contract["contract_status"] = ContractStatus.APPROVED.name
            current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            response = table.update_item(
                Key={
                    'property_id': contract['property_id'],
                },
                UpdateExpression="set contract_status=:t, modified_date=:m",
                ConditionExpression=
                    Attr('property_id').exists()
                & Attr('contract_status').is_in([
                    ContractStatus.DRAFT.name
                    ]),
                ExpressionAttributeValues={
                    ':t': contract['contract_status'],
                    ':m': current_date,
                },
                ReturnValues="UPDATED_NEW")
            print(f'var:response - "{response}"')
            
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code == 'ConditionalCheckFailedException':
                print(f"Unable to update contract Id {contract['property_id']}. Status is not in status DRAFT")
            elif code == 'ResourceNotFoundException':
                print(f"Unable to update contract Id {contract['property_id']}. Not Found")
            else:
                raise e

<!-- Testing the updates of contracts -->
Ensure you have sam sync activated. Otherwise make sure you use sam build and sam deploy to update your code changes.

Return to the terminal and execute the following curl command (you should have the $API variable set from the previous test):        

        curl --location --request PUT "${API}contracts" \
        --header 'Content-Type: application/json' \
        --data-raw '{"property_id": "usa/anytown/main-street/111"}' | jq

<!-- Review the logs -->
AWS SAM has a convenient feature that lets you easily view CloudWatch logs for your serverless app you just deployed.

Keep your terminal window with sam sync running as is. Start new terminal window to run following command to see the latest log entries:

        sam logs --stack-name uni-prop-local-contracts -t

Hint: you can run sam logs with -t option to have sam logs "tail" the CloudWatch Logs for log entries as they come in to the CloudWatch Logs console.

You should see lambda messages in there indicating that the function executed        