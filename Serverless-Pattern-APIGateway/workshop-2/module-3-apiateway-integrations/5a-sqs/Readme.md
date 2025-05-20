<!-- Test the deployed API using cURL -->
Follow the lab docs to test using the console of do the below on you command line:

- Open a new terminal window in your AWS Cloud9 environment.

- Copy the following cURL command and paste it into the terminal window, replacing <api-id> with your APIs API ID and <region> with the region where your API is deployed. You may have copied this URL in from the CloudFormation output in the last step. You can also find the full invoke URL in the API Gateway console by navigating to Stages > dev.

    $ curl -X POST https://<api-id>.execute-api.<region>.amazonaws.com/dev/order \
        -H 'Content-Type: application/json' \
        -d '{"id": "GF854123","price": 280.00,"name": "Karaoke"}'

The Response Body output should be

    {
        "SendMessageResponse":
        {
        "ResponseMetadata":
        {
            "RequestId":"83e347ef-8943-5068-a500-1b74442e02e6"
        },
        "SendMessageResult":
            {
            "MD5OfMessageAttributes":null,
            "MD5OfMessageBody":"f5373bd65c4ef0163e148862fb499944",
            "MD5OfMessageSystemAttributes":null,
            "MessageId":"ac4891c8-eca7-4ad3-8177-022bde2ce75c",
            "SequenceNumber":null
            }
        }
    }