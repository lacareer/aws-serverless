<!-- Add event pattern and IAM policies -->
In this section, you will learn about two 3rd party open-source tools that helps building serverless applications.

1. evb-cli  - an open source EventBridge pattern generator and debugging tool.
2. iam-policies-cli  - an open-source IAM policy generator tool.

We have intentionally left out a few things in the template.yaml file. In this section, we will use the above tools to fill them out.

<!-- Add an event pattern using EVB CLI -->
Explore the template.yaml file, specifically the ContractStatusChangedHandlerFunction resource. You will see the Pattern section is empty.

In a production-like scenario, we expect a lot of events of differing types and sources coming through the event bus. In order to ensure that we only trigger this function for a specific event, we need to filter the events with an event pattern.

Let's add the missing event pattern.

- In the terminal, enter evb pattern --region <REPLACE_WITH_YOUR_REGION>.
- Select registry unicorn.contracts.
- Select source unicorn.contract.
- Select detail-type ContractStatusChanged.
- Select done.
- Select Output to stdout.
- Copy the output, and paste it in template.yaml file under ContractStatusChangedHandlerFunction -> Properties -> Events -> StatusChangedEvent -> Properties -> Pattern. 
  NOTE: source property can come from SSM Parameter Store using !Sub "{{resolve:ssm:/uni-prop/UnicornContractsNamespace}}". 
  This is to show the power of EVB CLI to get started adding patterns and other powerful features really quickly.

<!-- Create missing IAM policies -->
Explore the template.yaml file, specifically the ContractStatusChangedHandlerFunction resource. 
This function requires access to write to the ContractStatusTable DynamoDB table. 
It also needs access to send messages to the PropertiesServiceDLQ queue.

In order to add permissions, we will be using AWS SAM Policy templates . We will use iam-policies-cli , to include these missing policies. This tool helps us interactively select a policy, rather than having to remember these policies yourself.

Let's add the two missing policies.

# Add the DynamoDB policy
- In the terminal, enter iam-pol.
- Select DynamoDB for 'Build statement for'.
- Select DynamoDBWritePolicy for 'Add actions' (press spacebar to select the item, then return key to select).
- Select ContractStatusTable for 'Select resource to grant access to'.
- Select Stdout for 'Send output to'.
- Copy the output from the terminal (just above the last line), and paste it in template.yaml file under ContractStatusChangedHandlerFunction -> Properties -> Policies.

<!-- Add the Queue policy -->
- In the terminal, enter iam-pol.
- Select SQS for 'Build statement for'.
- Select SQSSendMessagePolicy for 'Add actions' (press spacebar to select the item, then return key to select).
- Select PropertiesServiceDLQ for 'Select resource to grant access to'.
- Select Stdout for 'Send output to'.
- Copy the output from the terminal (just above the last line), and paste it in template.yaml file under ContractStatusChangedHandlerFunction -> Properties -> Policies.

<!-- Deploy the handler -->
Once you have completed this step build and deploy your application. In the next section we will test the handler.  