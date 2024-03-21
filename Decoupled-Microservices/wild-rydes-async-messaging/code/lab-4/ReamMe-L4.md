# Lab 4 - Orchestration and coordination

<!-- Lab objectives -->
In this lab, you will acquire the following skills:
    How to create a Step Functions State Machine
    How to use the Step Functions Workflow Studio
    How to catch exceptions and manage retries in a Step Functions State Machine
    How to manage successful and non-successful execution flows in a Step Functions State machine

The process consists of three discrete transactions that need to be treated as a single, distributed transaction.

1. Register Fare: register the fare in a DynamoDB table.
2. Payment Service: calls a payment gateway for credit card pre-authorisation, and using the pre-authorisation code, completes the payment transaction
3. Customer Accounting Service: once the payment has been processed, update the Wild Rydes Customer accounting system with the transaction details.

# See arctitectural diagram

<!-- Lab overview -->
AWS Step Functions is a fully managed Serverless workflow management service for managing long running processes and coordinating the components of distributed applications and microservices using visual workflows. But did you know it can also help you deal with the complexities of dealing with a long lived transaction across distributed components in your microservices architecture?

In this Builder session, you will learn how AWS Step Functions can help us to implement the Saga design pattern.

What problems are we trying to solve
When building cloud-based distributed architectures, one of the questions we need to ask ourselves is how do we maintain data consistency across microservices that have their own database / persistence mechanism? We do not have support for Distributed Transaction Coordinators (DTC) or two-phase commit protocols responsible for coordinating transactions across multiple cloud resources. We need a mechanism coordinate multiple local transactions.

<!-- The Saga pattern -->
A Saga is a design pattern for dealing with “long-lived transactions” (LLT), published by Garcia-Molina and Salem in 1987. Their original paper can be found here https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf .

“LLT is a saga if it can be written as a sequence of transactions that can be interleaved with other transactions.” (Garcia-Molina, Salem 1987)

Fundamentally the Saga Pattern is a failure management pattern that provides a mechansim for providing semantic consistency in our distributed applications by providing compensating transactions for every transaction where you have more than one collaborating services or functions. This compensating transactions ensures the system remains in a consistent state by rolling back or compensating for partially completed transactions.

<!-- Why AWS Step Functions -->
AWS Step Functions provide us with a mechanism for dealing with long-lived transactions, by providing us with the ability to build fully managed state machines that:
coordinate the components of distributed applications and microservicesallowing us to build our state machines using visual workflows provides us with a way to manage state and deal with failure

<!-- Build the lab artifacts from source -->
We provide you with an AWS SAM  template which we will use to bootstrap the initial state. In the bash tab (at the bottom) in your IDE, run the following commands to build the lab code:

    cd ~/environment/wild-rydes-async-messaging/code/lab-4
    sam build

<!-- Deploy the application -->
Now we are ready to deploy the application, by running the following command in the lab-3 directory:

    export AWS_REGION=$(aws --profile default configure get region)
    sam deploy \
        --stack-name wild-rydes-async-msg-4 \
        --capabilities CAPABILITY_IAM \
        --region $AWS_REGION \
        --guided

Wait until the stack is successfully deployed
It takes usually 4 minutes until the stack launched. You can monitor the progress of the wild-rydes-async-msg-4 stack in your AWS CloudFormation Console . 
When the stack is launched, the status will change from CREATE_IN_PROGRESS to CREATE_COMPLETE.

<!-- Build guide -->
The bootstrap script provisions the AWS resources required for the workflow, including the Lambda functions to execute transactions, Amazon DynamoDB table to store Fare items, and an Amazon SNS topic for notifications with Amazon SQS subscriptions for success and failures.

The bootstrapping process also provisions two Step Functions State Machines:

wild-rydes-async-msg-4-start-here - A starting point for your state machine, if you want to build it out yourself

wild-rydes-async-msg-4-completed - A completed state machine to use as a reference if you get stuck.

<!-- Executing and testing -->

# Executing the state machine
To begin testing your application, open the state machine and click Start execution
Copy and paste the fare payload into the Input field and click Start Execution. An execution will be successful if you invoke it with the following payload (you are free to update the values):

    {
        "customerId": "3",
        "fareId": "wr_563",
        "fareAmount": "$20.00",
        "cc": "2424 2424 2424 2424",
        "expiryDate": "12/22",
        "cvv": "111"
    }

# Testing failures
You can easily force custom exceptions from the Lambda functions by appending one of the following suffixes to the customerId. For example, if you want to test to see if your state machine is handling pre-authentication failures for the ChargeFare state, simply append _fail_auth to the customerId like so...

Here is a table that ilustrates some examples of the execution path your state machine will have when errors are invoked, and what a successful execution path looks like:


        <State>	                    <customerId Suffix>	            <Exception></Exception>

        ChargeFare	                _fail_auth	                    PaymentAuthException
        ChargeFare	                _fail_charge	                PaymentChargeException
        CustomerAccountCredit	    _fail_credit	                AccountCreditException

e.g 1

    {
        "customerId": "3_fail_auth",
        "fareId": "wr_563",
        "fareAmount": "$20.00",
        "cc": "2424 2424 2424 2424",
        "expiryDate": "12/22",
        "cvv": "111"
    }

e.g 2

    {
        "customerId": "_fail_charge",
        "fareId": "wr_563",
        "fareAmount": "$20.00",
        "cc": "2424 2424 2424 2424",
        "expiryDate": "12/22",
        "cvv": "111"
    }

e.g 3

    {
        "customerId": "3__fail_credit",
        "fareId": "wr_563",
        "fareAmount": "$20.00",
        "cc": "2424 2424 2424 2424",
        "expiryDate": "12/22",
        "cvv": "111"
    }


# Examining Notifications
You can examine success and failed notifications that are consumed from the SNS Topic by the respective SQS queues. Navigate to the SQS Console  and look at messages available.

<!-- Clean up -->
In this step, we will clean up all resources, we created during this lab, so that no further cost will occur.

# 1. Delete the AWS SAM template
In your Cloud9 IDE, run the following command to delete the resources we created with our AWS SAM template:

    cd ~/environment/wild-rydes-async-messaging/code/lab-3
    aws cloudformation delete-stack \
        --stack-name wild-rydes-async-msg-4

# 2. Delete the AWS Lambda created Amazon CloudWatch Log Group
Run the following command to delete all the log groups associated with the labs.

    aws logs describe-log-groups --query 'logGroups[*].logGroupName' --output table | awk '{print $2}' | \
        grep ^/aws/lambda/wild-rydes-async-msg-4 | while read x; \
        do  echo "deleting $x" ; aws logs delete-log-group --log-group-name $x; \
    done

Or you can follow this link  to list all Amazon CloudWatch Log Groups. 
Please filter with the prefix /aws/lambda/wild-rydes-async-msg-3, to find all CloudWatch Log Groups AWS Lambda created during this lab. 
Select all the Amazon CloudWatch Log Group one after each other and choose Delete log group from the Actions menu.