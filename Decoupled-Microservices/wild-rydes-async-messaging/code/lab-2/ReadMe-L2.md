# Lab 2 - Topic-queue chaining & load balancing

# NB That I removed/commented the reservedConcurrency of the function bcs ca-central-1 has a default reserved concurrency of 10
# that is also the minimum for ca-central in my aws account which cases the template to fail.

# Another option will be to request increase in quota using the console.

<!-- Lab objectives -->
In this lab, you will acquire the following skills:

    How to create an Amazon SQS queue
    How to leverage Amazon SQS as event source for AWS Lambda
    How to add an Amazon SQS subscription to an Amazon SNS topic
    How to define a subscription filter in an Amazon SNS subscriptions
    How to call Amazon SNS from AWS Lambda
<!-- Lab overview -->
Let’s look once more at the publish/subscribe channel between the unicorn management service and all 3 backend services on the right hand side that are interested in getting notified about ride completions.

One of these services could happen to be taken offline for maintenance. Or the code that processes messages coming in from the ride completion topic could run into an exception. These are two examples where a subscriber service could potentially miss topic messages. A good pattern to apply here is topic-queue-chaining. That means that you add a queue, in our case an Amazon SQS queue, between the ride completion Amazon SNS topic and each of the subscriber services.
As messages are buffered in a persistent manner in an SQS queue, no message will get lost should a subscriber process run into problems for many hours or days, or has exceptions or crashes.

But there is even more to it. By having an Amazon SQS queue in front of each subscriber service, we can leverage the fact that a queue can act as a buffering load-balancer. Due to nature that every queue message is delivered to one of potentially many consumer processes, you can easily scale your subscriber services out & in and the message load will be distributed over the available consumer processes. Furthermore, since messages are buffered in the queue, also a scaling event, for instance when you need to wait until an additional consumer process becomes operational, will not make you lose messages.

In this lab, we will develop the architecture below:

                                                ------>> SQS ------>> LAMBDA
                                                |
                                                |
user --->> ---->> API --->>  LAMBDA --->> SNS --|---->> SQS -------->> LAMBDA
                                |               |
                                |               |
                                |               |
                                |               ------>> SQS ------>> LAMBDA
                                |
                                |
                                |
                            DYNAMODB    

# Proceed with folowing steps if you downloaded the code in the LAB-1. Otherwise download it here: https://github.com/aws-samples/asynchronous-messaging-workshop/tree/master/code/lab-2 and proceed.

<!-- Build the lab artifacts from source -->

We provide you with an AWS SAM  template which we will use to bootstrap the initial state. 
In the bash tab (at the bottom) in your IDE, run the following commands to build the lab code:

    cd ~/wild-rydes-async-messaging/code/lab-2
    sam build

<!-- Deploy the application -->
Now we are ready to deploy the application, by running the following command in the lab-1 directory:

    export AWS_REGION=$(aws --profile default configure get region)  [This is optional command]

    sam deploy \
        --stack-name wild-rydes-async-msg-1 \
        --capabilities CAPABILITY_IAM \
        --region $AWS_REGION \
        --guided

It takes usually 4 minutes until the stack launched. You can monitor the progress of the wild-rydes-async-msg-2 stack in your SAM CLI or your AWS CloudFormation Console . When the stack is launched, the status will change from CREATE_IN_PROGRESS to CREATE_COMPLETE.

<!-- Create the Amazon SNS topic using SAM -->

# 1. Update the AWS SAM template
In your IDE for this workshop, open the SAM template file wild-rydes-async-messaging/CODE/lab-2/template.yaml. 
In the Resources section, add the definition for an Amazon SNS topic with the name RideCompletionTopic. 
You can find the AWS CloudFormation documentation to do so here: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html

# 2. Build and deploy after adding Ride Completion SNS Topic 
    cd ~/environment/wild-rydes-async-messaging/code/lab-2
    sam build
    sam deploy

# Note: you do not need to provide the arguments for the deployment, because AWS SAM saved the parameter values in a configuration file called samconfig.toml. See the documentation  more information on the AWS SAM CLI configuration file.

In the meantime while your waiting, you may want to have a look at the AWS SAM template to make yourself familiar with the stack we launched. Just click on the template.yaml attachment below to see the content.

<!-- Create Customer Notification service subscription -->

# 1. Update the AWS SAM template
In your IDE for this workshop, open the SAM template file wild-rydes-async-messaging/lab-2/template.yaml. In the Resources section, add the definition for an Amazon SQS queue with the name CustomerNotificationServiceQueue, the CustomerNotificationService will use to consume messages from. You can find the AWS CloudFormation documentation to do so here: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html

      CustomerNotificationServiceQueue:
        Type: AWS::SQS::Queue

The next step, before we can define the subscription, is granting our Amazon SNS topic the permissions to publish messages into this Amazon SQS queue. You can find the AWS CloudFormation documentation to do so here: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queuepolicy.html

    
  CustomerNotificationServiceQueuePolicy:
      Type: AWS::SQS::QueuePolicy
      Properties:
        Queues:
          - !Ref CustomerNotificationServiceQueue
        PolicyDocument:
          Statement:
            Effect: Allow
            Principal: '*'
            Action: sqs:SendMessage
            Resource: '*'
            Condition:
              ArnEquals:
                aws:SourceArn: !Ref RideCompletionTopic

Now we are ready to create the Amazon SNS subscription for the CustomerNotificationService. You can find the AWS CloudFormation documentation to do so here: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html

    
    CustomerNotificationServiceQueueToRidesTopicSubscription:
      Type: AWS::SNS::Subscription
      Properties:
        Endpoint: !GetAtt CustomerNotificationServiceQueue.Arn
        Protocol: sqs
        RawMessageDelivery: true
        TopicArn: !Ref RideCompletionTopic

The next step is to attach an AWS IAM policy tou our CustomerNotificationService AWS Lambda function, which grants permission to access our previously created Amazon SQS queue, to consume the messages. You can find the AWS SAM documentation to do so here  and here: https://github.com/aws/serverless-application-model/blob/develop/samtranslator/policy_templates_data/policy_templates.json

    
    Policies:
        - SQSPollerPolicy:
            QueueName: !Ref CustomerNotificationServiceQueue

Last but not least, we have to declare the CustomerNotificationServiceQueue as event source for our CustomerNotificationService. You can find the AWS SAM documentation to do so here: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html

    Events:
        CustomerNotificationServiceJobQueue:
          Type: SQS
          Properties:
            Queue: !GetAtt CustomerNotificationServiceQueue.Arn
            BatchSize: 1

# 2. Build and deploy after adding Ride Completion SNS Topic 
    cd ~/environment/wild-rydes-async-messaging/code/lab-2
    sam build
    sam deploy

<!-- Create Customer Accounting service subscription -->
# 1. Update the AWS SAM template

Open the SAM template file wild-rydes-async-messaging/code/lab-2/template.yaml. In the Resources section, add the definition for an Amazon SQS queue with the name CustomerAccountingServiceQueue, the CustomerAccountingService will use to consume messages from

    CustomerAccountingServiceQueue:
     Type: AWS::SQS::Queue

The next step, before we can define the subscription, is granting our Amazon SNS topic the permissions to publish messages into this Amazon SQS queue.

    CustomerAccountingServiceQueuePolicy:
        Type: AWS::SQS::QueuePolicy
        Properties:
            Queues:
            - !Ref CustomerAccountingServiceQueue
            PolicyDocument:
            Statement:
                Effect: Allow
                Principal: '*'
                Action: sqs:SendMessage
                Resource: '*'
                Condition:
                ArnEquals:
                    aws:SourceArn: !Ref RideCompletionTopic

Now we are ready to create the Amazon SNS subscription for the CustomerAccountingService.

    CustomerAccountingServiceQueueToRidesTopicSubscription:
        Type: AWS::SNS::Subscription
        Properties:
            Endpoint: !GetAtt CustomerAccountingServiceQueue.Arn
            Protocol: sqs
            RawMessageDelivery: true
            TopicArn: !Ref RideCompletionTopic

The next step is to attach an AWS IAM policy tou our CustomerAccountingService AWS Lambda function, which grants permission to access our previously created Amazon SQS queue, to consume the messages

    Policies:
        - SQSPollerPolicy:
            QueueName: !Ref CustomerAccountingServiceQueue

Last but not least, we have to declare the CustomerAccountingServiceQueue as event source for our CustomerAccountingService. 

    Events:
        CustomerAccountingServiceJobQueue:
          Type: SQS
          Properties:
            Queue: !GetAtt CustomerAccountingServiceQueue.Arn
            BatchSize: 1
# 2. Build and deploy after adding Ride Completion SNS Topic 
    cd ~/environment/wild-rydes-async-messaging/code/lab-2
    sam build
    sam deploy

<!-- Create Extraordinary Rides service subscription -->
# 1. Update the AWS SAM template
In your Cloud9 IDE for this workshop, open the SAM template file wild-rydes-async-messaging/lab-2/template.yaml. In the Resources section, add the definition for an Amazon SQS queue with the name ExtraordinaryRidesServiceQueue, the ExtraordinaryRidesService will use to consume messages from.

    ExtraordinaryRidesServiceQueue:
        Type: AWS::SQS::Queue

The next step, before we can define the subscription, is granting our Amazon SNS topic the permissions to publish messages into this Amazon SQS queue.

        ExtraordinaryRidesServiceQueuePolicy:
        Type: AWS::SQS::QueuePolicy
        Properties:
            Queues:
            - !Ref ExtraordinaryRidesServiceQueue
            PolicyDocument:
            Statement:
                Effect: Allow
                Principal: '*'
                Action: sqs:SendMessage
                Resource: '*'
                Condition:
                ArnEquals:
                    aws:SourceArn: !Ref RideCompletionTopic

Now we are ready to create the Amazon SNS subscription for the ExtraordinaryRidesService

    ExtraordinaryRidesServiceQueueToRidesTopicSubscription:
        Type: AWS::SNS::Subscription
        Properties:
            Endpoint: !GetAtt ExtraordinaryRidesServiceQueue.Arn
            Protocol: sqs
            RawMessageDelivery: true
            TopicArn: !Ref RideCompletionTopic
            FilterPolicy: { "fare": [{"numeric": [">=", 50]}], "distance": [{"numeric": [">=", 20]}] }

The next step is to attach an AWS IAM policy tou our ExtraordinaryRidesService AWS Lambda function, which grants permission to access our previously created Amazon SQS queue, to consume the messages. 

    Policies:
        - SQSPollerPolicy:
            QueueName: !Ref ExtraordinaryRidesServiceQueue

Last but not least, we have to declare the ExtraordinaryRidesServiceQueue as event source for our ExtraordinaryRidesService.

    Events:
        ExtraordinaryRidesServiceJobQueue:
          Type: SQS
          Properties:
            Queue: !GetAtt ExtraordinaryRidesServiceQueue.Arn
            BatchSize: 1

# 2. Build and deploy after adding Ride Completion SNS Topic 
    cd ~/environment/wild-rydes-async-messaging/code/lab-2
    sam build
    sam deploy

<!-- Update Unicorn Management Service -->

# 1. Grant additional IAM permissions to Lambda
In your IDE for this workshop, open the SAM template file wild-rydes-async-messaging/lab-2/template.yaml. In the Resources section, look for the SubmitRideCompletionFunction definition. It already contains one policies entry called DynamoDBCrudPolicy. Directly below, add a policy entry which grants Amazon SNS publish message permission. You can look up the supported policies here .

        - SNSPublishMessagePolicy:
            TopicName: !GetAtt RideCompletionTopic.TopicName

# 2. Provide the Amazon SNS topic ARN to Lambda
In your Cloud9 IDE for this workshop, open the SAM template file wild-rydes-async-messaging/lab-2/template.yaml. In the Resources section, look for the SubmitRideCompletionFunction definition. It already contains one environment variables entry called TABLE_NAME. Directly below, add an additional variable with the key TOPIC_ARN and the corresponding value.

    TOPIC_ARN: !Ref RideCompletionTopic

# 3. Update your Lambda function to call Amazon SNS
In your Cloud9 IDE, open the Python based AWS Lambda function wild-rydes-async-messaging/lab-2/unicorn-management-service/app.py.
Add the definition of the sns client directly after the dynamodb client:

    sns = boto3.client('sns', config=config)

# 4. Build and deploy after adding Ride Completion SNS Topic 
    cd ~/environment/wild-rydes-async-messaging/code/lab-2
    sam build
    sam deploy

<!-- Test Topic-Queue Chaining & Load Balancing -->

# 1. Look up the API Gateway endpoint
To look-up the API Gateway endpoint URL for the submit-ride-completion function, run the following command:

    aws cloudformation describe-stacks \
        --stack-name wild-rydes-async-msg-2 \
        --query 'Stacks[].Outputs[?OutputKey==`UnicornManagementServiceApiSubmitRideCompletionEndpoint`].OutputValue' \
        --output text

# 2. Send a couple requests to the Unicorn Management Service
Let's store this API Gateway endpoint URL in an environment variable, so we don't have to repeat it all the time:

    export ENDPOINT=$(aws cloudformation describe-stacks \
        --stack-name wild-rydes-async-msg-2 \
        --query 'Stacks[].Outputs[?OutputKey==`UnicornManagementServiceApiSubmitRideCompletionEndpoint`].OutputValue' \
        --output text)

To send a couple requests to the submit ride completion endpoint, execute the command below 5 or more times and change the request payload to test the filter criteria for the Extraordinary Rides Service:

    curl -XPOST -i -H "Content-Type\:application/json" -d '{ "from": "Berlin", "to": "Frankfurt", "duration": 420, "distance": 600, "customer": "cmr", "fare": 256.50 }' $ENDPOINT

# 3. Validate the message reception
Go to your Amazon CloudWatch Log console  and lookup all Log Groups with the prefix /aws/lambda/wild-rydes-async-msg-2.

Browse the most recent Log Streams to validate, that it could successfully process the message. You should also see some log entries, indicating a failed message processing. Shortly after, you should see the message redelivery from Amazon SNS and the successful message processing log entry.

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