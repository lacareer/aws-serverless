<!-- EventBridge Pipes -->

EventBridge Pipes allows you to create point-to-point integrations between message producers and consumers, with optional transformation, filtering, and enrichment steps.

To complete the Unicorn Contracts implementation, you'll use EventBridge Pipes to process the latest records from the Contracts table DynamoDB stream and transform them into ContractStatusChanged events.

The following steps guide you through visually building the Pipe, defining the source, filters, patterns, and transformations to construct the ContractStatusChanged event. This event will be published to the UnicornContracts-local event bus. Afterwards, you'll update the AWS SAM template in the Unicorn Contracts project.

<!-- Building the DevPipe -->
1- Open the the Amazon EventBridge console  and navigate to the Pipes feature.

2- Click the Create pipe button and name your Pipe DevPipe.

3- Specify the source as DynamoDB and select the latest stream for the Contracts table.

4- Click Next to continue

5- In the Filtering step, select Enter my own sample event. Copy and paste the events for your specific runtime from the table below.

    {
        "eventID": "f596bdbb621c57e694189ae9f1c172c2",
        "eventName": "INSERT",
        "eventVersion": "1.1",
        "eventSource": "aws:dynamodb",
        "awsRegion": "ap-southeast-2",
        "dynamodb": {
            "ApproximateCreationDateTime": 1692929660,
            "Keys": {
                "property_id": {
                    "S": "usa/anytown/main-street/123"
                }
            },
            "NewImage": {
                "contract_last_modified_on": {
                    "S": "25/08/2023 02:14:20"
                },
                "address": {
                    "M": {
                        "country": {
                            "S": "USA"
                        },
                        "number": {
                            "N": "123"
                        },
                        "city": {
                            "S": "Anytown"
                        },
                        "street": {
                            "S": "Main Street"
                        }
                    }
                },
                "seller_name": {
                    "S": "John Smith"
                },
                "contract_created": {
                    "S": "25/08/2023 02:14:20"
                },
                "contract_id": {
                    "S": "5bb04023-74aa-41fc-b86b-447602759270"
                },
                "contract_status": {
                    "S": "DRAFT"
                },
                "property_id": {
                    "S": "usa/anytown/main-street/123"
                }
            },
            "SequenceNumber": "4800600000000041815691506",
            "SizeBytes": 303,
            "StreamViewType": "NEW_AND_OLD_IMAGES"
        },
        "eventSourceARN": "arn:aws:dynamodb:ap-southeast-2:123456789012:table/uni-prop-local-contracts-ContractsTable-JKAROODQJH0P/stream/2023-08-24T00:35:44.603"
    }

6- In the Event pattern configuration create a pattern that only handles "INSERT" or "MODIFY" events, and where the 
  Contract Status in a NewImage is either "DRAFT" or "APPROVED". Make sure you test the pattern before continuing.

    {
        "eventName": ["INSERT", "MODIFY"],
        "dynamodb": {
            "NewImage": {
            "contract_status": {
                "S": ["DRAFT", "APPROVED"]
                }
            }
        }
    }

7- Click Next, and skip the Enrichment screen. Move straight to defining the Target.

8- On the Target screen, select EventBridge Bus and then UnicornContractsBus-local as the EventBridge event bus target. 
  Complete the rest of the Target configuration, so that it represents a put-event API call that represents the ContractStatusChanged event you want to publish.

### Hint
Remember what you are trying to do here. You have a DDB Stream event that represents the status change of a Contract. 
However, this is a service-level event type that does not represent the "domain" event you want to publish, so you need to transform 
it into a ContractStatusChanged event, and that requires you to specify fields such as the domain from which the event originated, 
and the type of event you are publishing. Hint: look at the Additional settings

9- Under Target Input Transformer, paste the same payload (item 5 above) that you used to define the source to the Sample events/Event Payload box.

10- Create your Transformer using the tools in the console. This is achieved by first selecting the datatype (for example S) for the property you want to add to the transformer. 
    Name the property in the transformer before selecting the next field from the sample event.

When you are finished, the Output box should contain a payload that looks like this. Make sure you name the properties according to the casing convention for your selected runtime. 
Note, that this casing may vary depending on your choice of runtime.

    {
    "property_id": "usa/anytown/main-street/123",
    "contract_id": "5bb04023-74aa-41fc-b86b-447602759270",
    "contract_status": "DRAFT",
    "contract_last_modified_on": "25/08/2023 02:14:20"
    }

11- Once you are satisfied with your Pipe configuration, click Create Pipe.

<!-- Using the Pipe definition in the Properties template -->
Creating a Pipe in the console is useful to get started, but you need to define this resource in the AWS SAM template so you can manage it as part of your application. 
You can, however, export the pipe you just created from the console using the CloudFormation Template feature. Select YAML as the export format.

1- Copy the generated output and paste it into a new file in your VS Code editor. This includes other resources and definitions, 
   but what you need to focus on is the AWS::Pipes::Pipe definition in out template.yaml.

2- Open template.yaml file and find ContractsTableStreamToEventPipe resource. Uncomment this resource, and complete the implementation 
   by adding the missing filtering pattern and target input transformer, you defined in the console.

        - In the SourceParameters property, complete the FilterCriteria by replacing the comment with the pattern you exported from the console.
        - In the TargetParameters property, replace the comment in the InputTemplate property with the pattern you exported from the console.

3- Under TargetParameters, note that we have replaced the hard coded value for the Source field with the SSM parameter value. This is to maintain consistency with how we reference our namespaces:

        EventBridgeEventBusParameters:
        Source: !Sub "{{resolve:ssm:/uni-prop/UnicornContractsNamespace}}"
        DetailType: ContractStatusChanged

4- Run sam build && sam deploy to deploy the changes. 

<!-- Testing the Pipes integration -->
To test whether the Pipes integration works as expected, create a new contract via the Contracts API. Assuming all the previous integrations worked, you should see the published EventBridge event event in the /aws/events/local/unicorn.contracts-catchall CloudWatch log group.

1- First, delete the DevPipe you created earlier. You won't need it moving forward now that you have defined the pipe in the template.

        aws pipes delete-pipe --name DevPipe  

2- In the terminal, paste this command (make sure your $API variable resolves to the Contract API):

        export API=`aws cloudformation describe-stacks --stack-name uni-prop-local-contracts --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" --output text`

3- Open the /aws/events/local/unicorn.contracts-catchall CloudWatch log group. If all your integrations to this point have been successfully implemented you should be able 
   to see your ContractStatusChanged event appear in your unicorn.contracts-catchall log group.   

   Alternatively, you can use sam logs --cw-log-group /aws/events/local/unicorn.contracts-catchall --tail in your terminal to see the event arrive in your "catch all" log group.  

You can add powertools to following application files:

1. contract_event_handler.py
2. helper.py (couldn't find file, perhaps it was just a mistake from workshop guys) 

Import and initialize statements:

        from aws_lambda_powertools import Logger, Metrics, Tracer
        from aws_lambda_powertools.logging import correlation_paths

        logger: Logger = Logger()
        tracer: Tracer = Tracer()
        metrics: Metrics = Metrics()

Function decorators for lambda_handler function:

        @logger.inject_lambda_context(log_event=True)
        @metrics.log_metrics(capture_cold_start_metric=True)
        @tracer.capture_method
        def lambda_handler(event, context: LambdaContext):
        # [...]     