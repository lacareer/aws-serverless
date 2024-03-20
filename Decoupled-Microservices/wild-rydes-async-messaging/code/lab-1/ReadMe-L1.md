# Lab 1 - Fan-out & message filtering

<!-- Lab objectives -->
In this lab, you will acquire the following skills:

    How to create an Amazon SNS topic
    How to add a AWS Lambda subscription to an Amazon SNS topic
    How to define a subscription filter in an Amazon SNS subscriptions
    How to call Amazon SNS from AWS Lambda

<!-- Lab overview -->
As a registered customer, when you need a ride, you can use the Wild Rydes customer app to request a unicorn and manage everything around it. As a registered unicorn, you can use the Wild Rydes unicorn app to manage everything around your business.

In particular, unicorns are interested to use the app to submit a ride completion after they have successfully delivered a customer to their destination. This is the use case we will now have a closer look at.

At Wild Rydes, end-user clients typically communicate via REST APIs with the backend services. For our use case, the Wild Rydes unicorn app interacts with the API exposed by the unicorn management service. It uses the submit-ride-completion resource to send the relevant details of the ride to the backend. In response to that, the backend creates a new completed-ride resource and returns the respective status code, the location, and a representation of the new resource to the client.

It’s probably not a surprise that there are other services in the Wild Rydes microservices landscape, that are also interested in a new completed ride:

Customer notification service: Customers should get a notification into their app about their latest completed ride.
Customer accounting service: After all, Wild Rydes is a business, so this service would be responsible to collect the fare from the customer.
Extraordinary rides service: This is special service that is interested in rides with fares or distances above certain thresholds - preparing the respective data for marketeers and success managers.
This use case obviously cries for making use of publish/subscribe messaging, which can comfortably done using Amazon SNS in a serverless and scalable manner. It decouples both sides as much as possible. Services on the right hand side can autonomously subscribe to the topic, transparent to the left hand side.


                                                 ------>> SNS
                                                |
                                                |
user --->> ---->> API --->>  LAMBDA --->> SNS --|---->> SNS
                                |               |
                                |               |
                                |               |
                                |                ------>> SNS 
                                |
                                |
                                |
                            DYNAMODB            
                                                
                                                
<!-- Download the workshop code -->

First you need to download the code required for this workshop. Run the following command in the bash terminal:

    sam init --location https://ws-assets-prod-iad-r-dub-85e3be25bd827406.s3.eu-west-1.amazonaws.com/e8738cf6-6eb0-4d1d-9e98-ae240d229535/code.zip

<!-- Build the lab artifacts from source -->

We provide you with an AWS SAM  template which we will use to bootstrap the initial state. 
In the bash tab (at the bottom) in your IDE, run the following commands to build the lab code:

    cd ~/wild-rydes-async-messaging/code/lab-1
    sam build

<!-- Deploy the application -->
Now we are ready to deploy the application, by running the following command in the lab-1 directory:

    export AWS_REGION=$(aws --profile default configure get region)  [This is optional command]

    sam deploy \
        --stack-name wild-rydes-async-msg-1 \
        --capabilities CAPABILITY_IAM \
        --region $AWS_REGION \
        --guided

Confirm the first 5 proposed arguments by hitting ENTER. When you get asked SubmitRideCompletionFunction may not have authorization defined, Is this okay? [y/N]:, enter y and hit ENTER for remaining options.

Wait until the stack is successfully deployed
It takes usually 4 minutes until the stack launched. You can monitor the progress of the wild-rydes-async-msg-1 stack in the SAM CLI or in your AWS CloudFormation Console . When the stack is launched, the status will change from CREATE_IN_PROGRESS to CREATE_COMPLETE.

<!-- Create the Ride Completion SNS Topic -->
Using the console, enter the topic name RideCompletionTopic and leave the default values. Scroll to the bottom of the page and click Create topic. 

Better still using SAM is easier by doing the below:
In your Cloud9 IDE for this workshop, open the SAM template file wild-rydes-async-messaging/code/lab-1/template.yaml. 
In the Resources section, add the definition for an Amazon SNS topic with the name RideCompletionTopic. 
You can find the AWS CloudFormation documentation to do so here .
#        
  RideCompletionTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: RideCompletionTopic
#

<!-- Build and deploy after adding Ride Completion SNS Topic -->
    cd ~/environment/wild-rydes-async-messaging/code/lab-1
    sam build
    sam deploy

# Note: you do not need to provide the arguments for the deployment, because AWS SAM saved the parameter values in a configuration file called samconfig.toml. See the documentation  more information on the AWS SAM CLI configuration file.

In the meantime while your waiting, you may want to have a look at the AWS SAM template to make yourself familiar with the stack we launched. Just click on the template.yaml attachment below to see the content.

<!-- Create Customer Notification service subscription -->
open the SAM template file wild-rydes-async-messaging/code/lab-1/template.yaml. In the Resources section, uncomment the Amazon SNS event source for the CustomerNotificationFunction. You can find the AWS SAM documentation to do so here:  https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-sns.html

#
    Events:
    SNSEvent:
        Type: SNS
        Properties:
        Topic: !Ref RideCompletionTopic

#

<!-- Build and deploy after adding Customer Notification service subscription -->
    cd ~/environment/wild-rydes-async-messaging/code/lab-1
    sam build
    sam deploy

<!-- Create Customer Accounting service subscription -->
open the SAM template file wild-rydes-async-messaging/code/lab-1/template.yaml. In the Resources section, uncomment the Amazon SNS event source for the CustomerAccountingFunction. You can find the AWS SAM documentation to do so here: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-sns.html

#
    Events:
    SNSEvent:
        Type: SNS
        Properties:
        Topic: !Ref RideCompletionTopic
#

<!-- Build and deploy after adding Customer Accounting service subscription -->
    cd ~/environment/wild-rydes-async-messaging/code/lab-1
    sam build
    sam deploy

<!-- Create Extraordinary Rides service subscription -->
open the SAM template file wild-rydes-async-messaging/code/lab-1/template.yaml. In the Resources section, add the definition for the Amazon SNS subscription for the ExtraordinaryRidesService. You can find the AWS CloudFormation documentation to do so here: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html

#
    Events:
        SNSEvent:
            Type: SNS
            Properties:
            Topic: !Ref RideCompletionTopic
            FilterPolicy:
                fare:
                - numeric:
                    - '>='
                    - 50
                distance:
                - numeric:
                    - '>='
                    - 20
#

<!-- Build and deploy after adding Customer Accounting service subscription -->
    cd ~/environment/wild-rydes-async-messaging/code/lab-1
    sam build
    sam deploy

<!-- Update Unicorn Management Service -->
After creating the Amazon SNS topic and all the subscriptions, do the following:

# 1 Grant additional IAM permissions to Lambda
In your IDE for this workshop, open the SAM template file wild-rydes-async-messaging/code/lab-1/template.yaml. In the Resources section, look for the SubmitRideCompletionFunction definition. It already contains one policies entry called DynamoDBCrudPolicy. Directly below, add a policy entry which grants Amazon SNS publish message permission. You can look up the supported policies here: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-policy-templates.html

#
    - SNSPublishMessagePolicy:
        TopicName: !GetAtt RideCompletionTopic.TopicName
#

# 2  Provide the Amazon SNS topic ARN to Lambda
In your IDE for this workshop, open the SAM template file wild-rydes-async-messaging/code/lab-1/template.yaml. In the Resources section, look for the SubmitRideCompletionFunction definition. It already contains one environment variables entry called TABLE_NAME. Directly below, add an additional variable with the key TOPIC_ARN and the corresponding value.

#
    TOPIC_ARN: !Ref RideCompletionTopic
#

# 3 Update your Lambda function to call Amazon SNS
In your IDE, open the Python based AWS Lambda function wild-rydes-async-messaging/code/lab-1/unicorn-management-service/app.py.
Add the definition of the sns client directly after the dynamodb client:

#
    sns = boto3.client('sns', config=config)

#

After the put item DynamoDB statement and before we are sending the response back to the caller, add the code to publish a message to Amazon SNS:

#
    response = sns.publish(
        TopicArn=TOPIC_ARN,
        Message=json.dumps(request),
        MessageAttributes = {
            'fare': {
                'DataType': 'Number',
                'StringValue': str(request['fare'])
            },
            'distance': {
                'DataType': 'Number',
                'StringValue': str(request['distance'])
            }
        }
    )

#

<!-- Build and deploy after Updating Unicorn Management Service -->
    cd ~/environment/wild-rydes-async-messaging/code/lab-1
    sam build
    sam deploy

<!-- Test fan-out and message filtering -->
In this step, we will validate that the Amazon SNS topic is publishing all messages to all subscribers. Because a subscriber can also fail processing a message, we also want to validate that Amazon SNS is redelivering the message, so that we will not miss a single message.

# 1. Look up the API Gateway endpoint
To look-up the API Gateway endpoint URL for the submit-ride-completion function, run the following command:

        aws cloudformation describe-stacks \
            --stack-name wild-rydes-async-msg-1 \
            --query 'Stacks[].Outputs[?OutputKey==`UnicornManagementServiceApiSubmitRideCompletionEndpoint`].OutputValue' \
            --output text

# 2. Send a couple requests to the Unicorn Management Service
Let's store this API Gateway endpoint URL in an environment variable, so we don't have to repeat it all the time:

    export ENDPOINT=$(aws cloudformation describe-stacks \
        --stack-name wild-rydes-async-msg-1 \
        --query 'Stacks[].Outputs[?OutputKey==`UnicornManagementServiceApiSubmitRideCompletionEndpoint`].OutputValue' \
        --output text)

To send a couple requests to the submit ride completion endpoint, execute the command below 5 or more times and change the request payload to test the filter criteria for the Extraordinary Rides Service:

    curl -XPOST -i -H "Content-Type\:application/json" -d '{ "from": "Berlin", "to": "Frankfurt", "duration": 420, "distance": 600, "customer": "cmr", "fare": 256.50 }' $ENDPOINT

# 3. Validate the message reception
Go to your Amazon CloudWatch Log console  and your Log Groups beginning with /aws/lambda/wild-rydes-async-msg-1-. Select a Log Group to see all Log Streams available for that Log Group.

Browse each Log Stream to validate, that each of our 3 backend service could successfully process the message. You should also see some random log entries, indicating a failed message processing. Shortly after, you should see the message redelivery from Amazon SNS and the successful message processing log entry.

<!-- Clean up -->

In this step, we will clean up all resources, we created during this lab, so that no further cost will occur.

# 1. Delete the AWS SAM template
In your IDE, run the following command to delete the resources we created with our AWS SAM template:

    cd ~/environment/wild-rydes-async-messaging/code/lab-1
    aws cloudformation delete-stack \
    --stack-name wild-rydes-async-msg-1

# 2. Delete the AWS Lambda created Amazon CloudWatch Log Group
Run the following command to delete all the log groups associated with the labs.

    aws logs describe-log-groups --query 'logGroups[*].logGroupName' --output table | awk '{print $2}' | \
        grep ^/aws/lambda/wild-rydes-async-msg-1 | while read x; \
        do  echo "deleting $x" ; aws logs delete-log-group --log-group-name $x; \
    done

Or you can follow this link  to list all Amazon CloudWatch Log Groups. Please filter with the prefix /aws/lambda/wild-rydes-async-msg-1, to find all CloudWatch Log Groups AWS Lambda created during this lab. Select all the Amazon CloudWatch Log Group one after each other and choose Delete log group from the Actions menu.