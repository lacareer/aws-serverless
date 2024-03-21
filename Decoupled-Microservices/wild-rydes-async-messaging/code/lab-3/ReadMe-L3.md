# Lab 3 - Scatter-gather

<!-- Lab objectives -->
In this lab, you will acquire the following skills:

    How to implement a scatter pattern by sending messages through multiple channels
    How to implement a request response flow in asynchronous manner
    How to stage responses from multiple sources
    How to create a gather pattern by querying responses based on a request id
    
<!-- Lab overview -->
As Wild Rydes business has grown in its popularity, it has opened its platform for various unicorn providers to partner with Wild Rydes. Customers of Wild Rydes app will be able to submit a request for a ride from their mobile app. Behind the scenes, Wild Rydes service will talk to multiple service providers who will submit quotes for the customer. The platform will receive all the responses and stage it in a database. The app will then periodically poll for the response quotes using a REST API and present them to the customer. The end user app will keep updating the dashboard of the quotes as new providers keep sending the response.

In this architecture queues provide a loose coupling between the producer and consumer systems. In the absence of queues, the client systems would need to know the API endpoints for each of the server systems. It will need to be stored in a central database for any type of changes. It gets further complicated as additional instances are added or removed. In addition to it, client systems will need to implement failure and retry logic in their code. Queues help alleviate lot of such issues by decoupling the systems and providing a store and forward mechanism.

The service can be enhanced further to notify customers once all the service providers have responded or have exceeded the time for them to respond.

<!-- Build the lab artifacts from source -->
We provide you with an AWS SAM  template which we will use to bootstrap the initial state. In the bash tab (at the bottom) in you AWS Cloud9 IDE, run the following commands to build the lab code:

    cd ~/environment/wild-rydes-async-messaging/code/lab-3
    sam build

<!-- Deploy the application -->
Now we are ready to deploy the application, by running the following command in the lab-3 directory:

    sam deploy --guided --stack-name wild-rydes-async-msg-3 --capabilities CAPABILITY_IAM

<!-- Test Scatter-Gather -->

# 1. Get API Gateway endpoint to send request for quotes
The lab 3 SAM template created two separate API gateway endpoints. 
They will be shown under the outputs tab of the cloudformation stack once deployment is completed. 
RideBookingApiSubmitInstantRideRfqEndpoint is the API endpoint to submit request for quotes and RideBookingApiQueryInstantRideRfqEndpoint is used to query the response from various ride operators. 
You can run the following command to retrieve the RideBookingApiSubmitInstantRideRfqEndpoint API Gateway Endpoint URL.

    aws cloudformation describe-stacks \
        --stack-name wild-rydes-async-msg-3 \
        --query 'Stacks[].Outputs[?OutputKey==`RideBookingApiSubmitInstantRideRfqEndpoint`][OutputValue]' \
        --output text

Let's store this request API Gateway endpoint URL in an environment variable, so we don't have to repeat it all the time:

    export REQ_ENDPOINT=$(aws cloudformation describe-stacks \
        --stack-name wild-rydes-async-msg-3 \
        --query 'Stacks[].Outputs[?OutputKey==`RideBookingApiSubmitInstantRideRfqEndpoint`].OutputValue' \
        --output text)

# 2. Send the request for quotes
The trigger point of the flow is a request message that is sent to get the quote. 
The following is the structure of the request event message.
    {
        "from": "Frankfurt",
        "to": "Las Vegas",
        "customer": "cmr"
    }

The from tag represents the starting point and to indicates the destination. 
The customer is an id for the end ussr. Execute the below commands to send a request for quote.

    curl -XPOST -i -H "Content-Type\:application/json" -d @event.json $REQ_ENDPOINT

The output will have a rfq-id parameter. Save the value in a notepad as it will be used later to query the responses.

# 3. Get API Gateway endpoint to query responses
Before we can query the quotes, we have to lookup the response query endpoint. 
Execute the following command to query the RideBookingApiQueryInstantRideRfqEndpoint output in Amazon CloudFormation stack via the CLI:

    aws cloudformation describe-stacks \
        --stack-name wild-rydes-async-msg-3 \
        --query 'Stacks[].Outputs[?OutputKey==`RideBookingApiQueryInstantRideRfqEndpoint`][OutputValue]' \
        --output text

Let's store this request API Gateway endpoint URL in an environment variable, so we don't have to repeat it all the time:

    export RES_ENDPOINT=$(aws cloudformation describe-stacks \
        --stack-name wild-rydes-async-msg-3 \
        --query 'Stacks[].Outputs[?OutputKey==`RideBookingApiQueryInstantRideRfqEndpoint`].OutputValue' \
        --output text | cut -d'{' -f 1)

# 4. Query the RFQ response endpoint
Replace the <> in the below command with the value that was received in step 2. 
This is the correlation id to get the response quotes for the request that was sent. Execute the following command to query the responses:

    curl -i -H "Accept\:application/json" ${RES_ENDPOINT}<<rfq-id>>

    # e.g
    curl -i -H "Accept\:application/json" ${RES_ENDPOINT}fe4dab44-b446-4806-9969-42787b177d3c

The above call invokes a lambda function via API gateway end point. 
It queries the DynamoDB table to get the responses corresponding to the request id. 
The response will be a json payload showing the response quotes from different providers. A sample response is shown below:

    {
        "quotes": [
            {
            "responder": "UnicornManagementResource10",
            "quote": "45"
            },
            {
            "responder": "UnicornManagementResource2",
            "quote": "100"
            }
        ],
        "rfq-id": "8b095f9e-cffc-4790-91a6-28353fa30e42",
        "from": "Frankfurt",
        "to": "Las Vegas",
        "customer": "cmr"
    }

It shows the response quotes from two service providers. 
The function will need to be called in regular intervals if the service providers send responses at different times. 
You can also check the responses in the DynamoDB directly by querying based on the request id.

# How to verify the data is actually coming from DynamoDB?
All responses for the quotes are received in a SQS queue. 
A lambda function receives the messages and stages them in a DynamoDB table. 
You can verify the response data by accessing the DynamoDB table in your specific region.

<!-- Clean up -->
In this step, we will clean up all resources, we created during this lab, so that no further cost will occur.

# 1. Delete the AWS SAM template
In your Cloud9 IDE, run the following command to delete the resources we created with our AWS SAM template:

    cd ~/environment/wild-rydes-async-messaging/code/lab-3
    aws cloudformation delete-stack \
        --stack-name wild-rydes-async-msg-3

# 2. Delete the AWS Lambda created Amazon CloudWatch Log Group
Run the following command to delete all the log groups associated with the labs.

    aws logs describe-log-groups --query 'logGroups[*].logGroupName' --output table | awk '{print $2}' | \
        grep ^/aws/lambda/wild-rydes-async-msg-3 | while read x; \
        do  echo "deleting $x" ; aws logs delete-log-group --log-group-name $x; \
    done

Or you can follow this link  to list all Amazon CloudWatch Log Groups. 
Please filter with the prefix /aws/lambda/wild-rydes-async-msg-3, to find all CloudWatch Log Groups AWS Lambda created during this lab. 
Select all the Amazon CloudWatch Log Group one after each other and choose Delete log group from the Actions menu.