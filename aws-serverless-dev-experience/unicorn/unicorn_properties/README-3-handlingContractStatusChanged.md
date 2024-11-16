<!-- Handling the ContractStatusChanged event -->
In this section we are going to start building the Properties service.

<!-- Working with mhlabs iam-pol and evb-cli -->
Take a look at the ContractStatusChangedHandlerFunction function definition. This function is missing the required policies to be able to put 
items into the Amazon DynamoDB table ContractStatusTable, as well as the EventBridge rule patterns that processes the ContractStatusChanged event.

You will notice that it's missing AWS IAM policies for the function to be able to write and ready from the table.

Let resolve these using open source cli tools and libraries built and maintained by Mathem tech team (https://github.com/mhlabs ). There are many packages but I installed the below:

    sudo npm install -g @mhlabs/iam-policies-cli
    sudo npm install -g @mhlabs/evb-cli

Using the https://github.com/mhlabs , read more about the usage    


# DID NOT FULLY UNDERSTAND THE USE OF THE MHLABS PACKAGES BELOW AND HAD TO COPY THE POLICIES AND RULES FROM THE COMPLETED CODE 
# REFER TO README-5 FIL FOR MORE ON THIS PACKAGES
<!-- Creating the IAM policies for the ContractStatusChangedHandler function    -->
Your goal to create two policies to define a permissions target for DynamoDB. Create policies for both DynamoDBReadPolicy 
and DynamoDBWritePolicy for the ContractStatusTable. Run:

    iam-pol -t template.yaml -f yaml (follow prompts on cmd)

Available options for the above command are:
    Options:
    -v, --vers                        output the current version
    -t, --template <filename>         Template file name (default: "serverless.template")
    -f, --format <JSON|YAML>          Output format (default: "JSON")
    -o, --output <console|clipboard>  Template file namePolicy output (default: "console")
    -h, --help                        output usage information 
# Copied from completed code
The above generates a policy action like below each time you follow 
    DynamoDBReadPolicy:
        TableName: !Ref ContractStatusTable
OR
    DynamoDBWritePolicy:
        TableName: !Ref ContractStatusTable    

Attach the policies to ContractStatusChangedHandlerFunction lambda function        

<!-- Defining the pattern for the ContractStatusChangedHandler function event source -->
Once you have implemented the policy for the Lambda function, it's time to create the pattern for the StatusChangedEvent event source. 
Again, we are using open source tools from the Mathem tech team (https://github.com/mhlabs ).

The rule pattern should be source unicorn.contracts and detail-type ContractStatusChanged. Run:

    evb pattern --region <REPLACE_WITH_YOUR_REGION>  (follow prompts on cmd. Could not )

Basically the pattern, copied from completed code, for the rule should be since we have the 'source' in SSM nad the detail-type to be hardcoded:

    source:
        - "{{resolve:ssm:/uni-prop/UnicornContractsNamespace}}"
    detail-type:
        - ContractStatusChanged

<!-- Initial Deployment -->
Ensure you have installed the dependencies in README-2-Initialization.md

Build and deploy the service using the following commands (make you resolve any template issues before you do):

    cfn-lint template.yaml -a cfn_lint_serverless.rules
    sam build --cached
    sam deploy

This will take ~5 mins to complete, during which SAM CLI will provide feedback on the status of the deployment. If the deployment is successful, you will see following message:

    Successfully created/updated stack - uni-prop-local-properties in "Your-Region"    