<!-- Test the deployed API using cURL -->
Follow the lab docs to test using the console or the instructions below for testing on the commnad line

- Open a new terminal window in your AWS Cloud9 environment.

- Copy the following cURL command and paste it into the terminal window, replacing <api-id> with your API ID and <region> with the region where your API is deployed. You may have copied this URL in from the CloudFormation output in the last step. You can also find the full invoke URL in the API Gateway console by navigating to Stages > dev.

    $ curl -X GET 'https://<api-id>.execute-api.<region>.amazonaws.com/dev/pets' -G -d 'scope=internal'

The Response Body output should be:

    {
        "statusCode": 200,
        "message": "Go ahead without me"
    }