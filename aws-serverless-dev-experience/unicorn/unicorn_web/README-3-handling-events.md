<!-- Handle Event -->

# Using cfn-lint and serverless-rules
A common development practice with Serverless applications is checking the integrity of your AWS SAM templates. 
Tools such as cfn-lint and serverless-rules help you do this, and apply best practices to your serverless resources.

To help you understand how to use this tool, we have intentionally omitted configuration from your template. 
Let's fix these before we do our first deployment.

1. Navigate to the root of the Unicorn Web folder.
2. Run the following command in your terminal.

    cfn-lint template.yaml -a cfn_lint_serverless.rules

The output that is generated should look something like this:

E2522 At least one of [EventPattern, ScheduleExpression] should be specified for Resources/PublicationApprovedFunctionApprovalEvent/Properties
template.yaml:82:1

WS2002 API Gateway stage WebApiStage does not have the TracingEnabled property set to true.
template.yaml:82:1

WS1004 Lambda function RequestApprovalFunction does not have a corresponding log group with a Retention property
template.yaml:113:3    

<!-- Save code bindings -->
In this section, we will be downloading the code bindings and uploading it to your IDE.

1. Navigate to Amazon EventBridge -> Schemas -> Discovered Schemas  (or Unicorn Properties Schemas  if you didn't build the Property Service)
2. Select unicorn.properties@PublicationEvaluationCompleted schema
3. Download code bindings for the appropriate language
4. Unzip the contents, copy the schema/unicorn_properties local folder to the unicorn_web/src/schema directory. 
   For Java language, copy the schema local directory to unicorn_web/PropertyFunctions/src/main/java/ directory.

<!-- Implement Schema -->
Make the following updates to the src/approvals_service/publication_approved_event_handler.py file.

1. Add the import statements to the start of the page

    from schema.unicorn_contracts.publicationevaluationcompleted import (AWSEvent, PublicationEvaluationCompleted, Marshaller)

2. At the beginning of Lambda Handler function, deserialise the event to a strongly typed object, 
   then call the publication_approved by passing the PublicationEvaluationCompleted object.

    # Deserialize event into strongly typed object
    awsEvent:AWSEvent = Marshaller.unmarshall(event, AWSEvent)
    detail:ContractStatusChanged = awsEvent.detail

    return publication_approved(detail, errors)

<!-- Initial deployment -->
Now it is time to build and deploy Web service for the first time using SAM.  

    poetry export --without-hashes --format=requirements.txt --output=src/requirements.txt
    sam build --cached
    sam deploy

<!-- Pre-populate DynamoDB table -->
For the solution to work, it requires a DynamoDB table to contain records which can be used to test the solution. 
As we want to independent of other teams in our development of this service, we are going to load some dummy records to DynamoDB table.

1. Load Dummy data    
    # add chmod permission to execute script if not already set
        ./data/load_data.sh 

    # If the 'yq' package was not installed on my machine so I did the substitute 'OR'
        web_table_name="$(aws cloudformation describe-stacks --stack-name uni-prop-local-web --query "Stacks[0].Outputs[?OutputKey=='WebTableName'].OutputValue" --output text)"

        aws ddb put $web_table_name  file://./data/property_data.json

2. Verify that data exists in DynamoDB table
   Run following command to verify whether the sample records have successfully been loaded to DynamoDB:    

    web_table_name="$(aws cloudformation describe-stacks --stack-name uni-prop-local-web --query "Stacks[0].Outputs[?OutputKey=='WebTableName'].OutputValue" --output text)"

    aws ddb select $web_table_name --projection 'PK, SK, city, street'

You should see an output similar to below:

    Count: 3
    Items:

    - PK: PROPERTY#usa#anytown
    SK: main-street#111
    city: Anytown
    street: Main Street
    - PK: PROPERTY#usa#anytown
    SK: main-street#333
    city: Anytown
    street: Main Street
    - PK: PROPERTY#usa#main-town
    SK: main-street#222
    city: Main Town
    street: My Street
    ScannedCount: 3   

<!-- Completing the integrations -->
Before the Unicorn Properties service can process the PublicationApprovalRequested, the Unicorn Properties Service needs to create a subscription (rule) on the Unicorn Web event bus.

To complete the integration between these two services, go back to the unicorn-properties/integration folder and open the subscriptions.yaml

Enable the PublicationApprovalRequestedSubscriptionRule rule that has been commented out (and the output) and redeploy the Properties service.

Verify that the unicorn.properties-PublicationApprovalRequested has been created on the UnicornWebBus-local event bus.     