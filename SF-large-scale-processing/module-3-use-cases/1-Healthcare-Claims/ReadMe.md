 <!-- Use Cases -->

# HealthCare Claims Processing
In the US healthcare system, claims are typically categorized as professional, institutional, or dental claims when they are submitted to health insurance payers. Health plans are responsible for validating these claims, responding to the provider, assessing the claims, making payments to the provider, and providing an explanation of benefits to the member. In this module, we focus on the validation phase of the claims process, which occurs after the claims data has already been converted to comply with the FHIR specification. During the validation phase, various business rules are applied to validate and enrich the claims. This represents the final step in the incoming flow of claims before they are transformed into custom data formats required by backend claims adjudication systems.

<!-- Deploy stack -->

Using template.yaml, deploy the stack with cloudformation

<!-- Exploring the Dataset -->
Navigate to the S3 Bucket. Search for dmapworkshophealthcare bucket. This bucket contains 1026 JSON files with around 60,000 records, with a total size of 270MB. These JSON files are generated using Synthea Health Library, https://github.com/synthetichealth/synthea, to simulate patient claims data in FHIR  format.

The excerpt below shows one such daily claim record.

Each claim has a claim coding, the service dates, the provider details, the procedure details, an item-wise bill, the total amount and any additional information required for processing.

# exerpt
    {
        "resourceType": "Claim",
        "id": "d6c1872c-9b97-0fc1-161a-5c2c9b3f54bf",
        "status": "active",
        "type": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/claim-type",
                    "code": "institutional"
                }
            ]
        },
        "use": "claim",
        "patient": {
            "reference": "urn:uuid:86ad439b-3df7-8882-2458-af0d0743d12b",
            "display": "Alvin56 Zulauf375"
        },
        "billablePeriod": {
            "start": "2013-09-09T11:01:44+00:00",
            "end": "2013-09-09T12:01:44+00:00"
        },
        "created": "2013-09-09T12:01:44+00:00",
        "provider": {
            "reference": "Organization?identifier=https://github.com/synthetichealth/synthea|5c896155-eb9a-383e-9162-a43ebb7f1cc5",
            "display": "LINDEN PONDS"
        },
        "priority": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/processpriority",
                    "code": "normal"
                }
            ]
        },
        "facility": {
            "reference": "Location?identifier=https://github.com/synthetichealth/synthea|de4402eb-c9e7-3723-9584-345f665c5f5c",
            "display": "LINDEN PONDS"
        },
        "procedure": [
            {
                "sequence": 1,
                "procedureReference": {
                    "reference": "urn:uuid:ece5738e-95ce-4dc6-1df0-95f4dcccce9d"
                }
            }
        ],
        "insurance": [
            {
                "sequence": 1,
                "focal": true,
                "coverage": {
                    "display": "Medicaid"
                }
            }
        ],
        "item": [
            {
                "sequence": 1,
                "productOrService": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "182813001",
                            "display": "Emergency treatment (procedure)"
                        }
                    ],
                    "text": "Emergency treatment (procedure)"
                },
                "encounter": [
                    {
                        "reference": "urn:uuid:c6f74fed-bdb9-6f50-29c5-3519fd948936"
                    }
                ]
            },
            {
                "sequence": 2,
                "procedureSequence": [
                    1
                ],
                "productOrService": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "65546002",
                            "display": "Extraction of wisdom tooth"
                        }
                    ],
                    "text": "Extraction of wisdom tooth"
                },
                "net": {
                    "value": 14150.92,
                    "currency": "USD"
                }
            }
        ],
        "total": {
            "value": 14297.1,
            "currency": "USD"
        }
    }

** In the next step, you will build a workflow with a Distributed Map state to analyze this dataset.

<!-- Add SF Workflow -->

To build the SF workflow manually go to next step or add SF  to the template by uncommenting the code code related to it.


<!-- Creating the Workflow -->
- Navigate to AWS Step Functions  in your AWS console. Make sure you are in the correct region.

- If you are not on the State machines page, choose State machines on the left side hamburger menu icon and then select Create state machine

- On the Choose a template overlay, choose the Blank template, and select Select.

- Select patterns tab and drag Process S3 objects onto the Workflow Studio canvas.

- Configure the Distributed Map state with the following values:



# Setting	                                    Value	                                                    Notes

State                                           name	                                                    Healthcare Claims processing	


Processing mode	                                Distributed	                                                Distributed mode runs child workflow executions for each map iteration to achieve up to 10K concurrent 


workflows


Item source	                                    Amazon S3	


S3 item source	                                S3 object list	                                             Since we have multiple CSV files we want to analyze, we'll use this item source as it uses S3 ListObjects 

to get a list a paginated list of objects in the bucket.


S3 bucket	                                    DMapHealthCareProcessingDestBucket from cfn o/p	            You can find the S3 bucket name in the CloudFormation  stack outputs tab for this module or use the Browse 

S3 or enter S3 URI to browse and select the bucket having dmapworkshophealthcare in its name


Enable                                          batching	Check this box	


Max items per batch	                            50	                                                        Define the number of items to be processed by each child workflow execution


Set concurrency limit	                        500	                                                        The Lambda burst concurrency limit  varies by region. You can modify this concurrency setting based on the 


capacity of your downstream systems.


Child execution type	                        Standard	                                                Some of these child workflow executions take more than a minute to run, so we can use Standard workflows..


Set a tolerated failure threshold	Expand Additional configuration to see this setting. Check this box	


Tolerated failure threshold	                    5%	                                                        Use this setting to consider a job failed if a minimum threshold of child workflow executions failed. This 

is useful if you have inconsistencies in your dataset.


Use state name as label in Map Run ARN	        Check this box	


Export Map state results to Amazon S3	        Leave as it is (Unchecked)	



- Select the Lambda Invoke state within the Distributed Map state. Configure the state with the following values.

        Setting	                                Value

        State name	                            Load claims

        Function name	                        DMapHealthCareProcessingLambdaFunction:$LATEST

        Payload	                                Use state input as payload


- Search for AWS Lambda and drag the Invoke state onto the canvas within the Distributed Map under the existing Lambda state. Configure the state with the following values:

        Setting	                Value

        State name	            Validate claims

        Function name	        DMapHealthCareRuleEngineLambdaFunction:$LATEST

        Payload	                Use state input as payload

- Select the Config tab next to the state machine name at the top of the page and Edit the State machine name: HealthCareClaimProcessingStateMachine

- For the Execution role, choose an existing role containing HealthCareClaimProcessingStateMachineRole in its name

- Leave the rest of the defaults and select Create.

*** If you have exceptions in the lambda child workflows as a result of too many request, change the currency of you sf map

<!-- Executing the Workflow and Viewing the Results -->

# View map run

- Select Start execution and use the default input payload.

- The execution will take up to 5 minutes to complete successfully.

- In the execution details page, select Distributed Map state in the Graph View, then select Details tab.

- Select Map Run link to view details of the Distributed Map execution.

- This page provides a summary of the Distributed Map job.

We can see that 21 child workflow executions completed successfully with 0 failures. Each child workflow processed 50 files.
We can view the duration of each child workflow execution. You can see overlapping timestamps for the start and end times, indicating that the data was processed in parallel.
If you select the execution name, you can use the Execution Input and output tab to view the input files for a child workflow execution and the execution output with details.

<!-- Verifying DynamoDB results -->
The Validate Claim function will apply the rules on the claims and store the claim status (Approved / Rejected) along with the rejected reason in the DynamoDB table DMapHealthCareClaimTable. 
You can use the gear icon on the right side of the screen to select which columns you want to view.

<!-- Extra Credits -->
Great! You have now executed and analyzed the results of the workflow. Well done!

But you cannot stop there! You will need to optimize for performance and cost!

Here is a list of things to try in order to understand the various handles you have at your disposal to optimize a workflow (be careful of your account lambda concurrency limit):

- Increase the concurrency limit to 1000 and execute it again. Does it change the duration of the execution?

- What happens if you decrease the Item Batching size to 25 and execute the workflow? What is the impact on duration as well as cost?

- What combination of concurrency limit and batching size would be optimal?

- What happens if you change the type of the workflow to 'Express' and execute it? What is the impact on cost? Would this workflow type work for any batching size of the provided data set?
