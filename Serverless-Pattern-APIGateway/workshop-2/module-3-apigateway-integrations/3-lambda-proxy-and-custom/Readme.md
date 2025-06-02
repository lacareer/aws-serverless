<!-- Test Integration -->
After you create your API Gateway REST API with Lambda integration, you can test the API.

Test Lambda Proxy Integration using API Gateway console

Follow the lab doc to complete testing

<!-- Test the deployed API using cURL -->

- Open a new terminal window in your AWS Cloud9 environment.

- Copy the following cURL command and paste it into the terminal window, replacing <api-id> with your API's API ID and <region> with the region where your API is deployed. You may have copied this URL in from the CloudFormation output in the last step. You can also find the full invoke URL in the API Gateway console by navigating to Stages > dev.

    $ curl -X GET 'https://<api-id>.execute-api.<region>.amazonaws.com/dev/resource/{proxy+}'

The Response Body output should be:

    "Hello from Lambda!"   

Do the same to test the custom integration with the PUT method 

    $ curl -X PUT https://<api-id>.execute-api.<region>.amazonaws.com/dev/resource \
        -H 'Content-Type: application/json' \
        -d '{"name": "John Dee", "age": 45,"email": "jd@jd.com"}'

The Response Body output should be

    {
        "status": 200,
        "message": "{"message":"Hello from Lambda!"}",
        "message_details" "This message was inserted from the response transformation."
    }

