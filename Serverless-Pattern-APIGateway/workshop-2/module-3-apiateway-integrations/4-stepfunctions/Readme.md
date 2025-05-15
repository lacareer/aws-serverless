<!-- Test the deployed API using cURL -->
Test using console by folloing the lab instrustions or do the below:

- Open a new terminal window in your AWS Cloud9 environment.

- Copy the following cURL command and paste it into the terminal window, replacing <api-id> with your API's API ID and <region> with the region where your API is deployed. You may have copied this URL in from the CloudFormation output in the last step. You can also find the full invoke URL in the API Gateway console by navigating to Stages > dev. This will call an Step Functions Asynchronous.

    $ curl -X POST https://<api-id>.execute-api.<region>.amazonaws.com/dev/async -H 'Content-Type: application/json' -d '{"number" : 31}'

The output should be:

    {"executionArn":"arn:aws:states:us-east-1:XYZ:execution:StateMachineStandard:XYZ,"startDate":1.680118019525E9}%

Do the same to test the Step Functions Synchronous call.

    $ curl -X POST https://<api-id>.execute-api.<region>.amazonaws.com/dev/sync -H 'Content-Type: application/json' -d '{"number" : 31}'

The output should be:

    {
    "billingDetails":{
    "billedDurationInMilliseconds":100,
    "billedMemoryUsedInMB":64
    },
    "executionArn":"arn:aws:states:us-east-1:233167937349:express:StateMachineExpress:cfd77ee3-6fdb-43d4-a7fb-8e96b0a32c15:4eea1880-b652-421f-a8c3-7b5a6ff251f0",
    "input":"{\"number\":31}",
    "inputDetails":{
        "__type":"com.amazonaws.swf.base.model#CloudWatchEventsExecutionDataDetails",
        "included":true
    },
    "name":"cfd77ee3-6fdb-43d4-a7fb-8e96b0a32c15",
    "output":"{\"message\":\"Hello from Step Functions!\"}",
    "outputDetails":{
        "__type":"com.amazonaws.swf.base.model#CloudWatchEventsExecutionDataDetails",
        "included":true
    },
    "startDate":1.680118226325E9,
    "stateMachineArn":"arn:aws:states:us-east-1:233167937349:stateMachine:StateMachineExpress",
    "status":"SUCCEEDED",
    "stopDate":1.680118226335E9,
    "traceHeader":"Root=1-642491d2-4380e8cb5764286d73bf0198;Sampled=1"
    }