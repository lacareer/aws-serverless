<!-- Create subscription to Topic -->

With our SNS topic created, you now need to create a subscription in order to receive the messages sent to this topic. For the purposes of this demo, you will use your email address as the notification endpoint. Return to your Cloud9 environment and paste in the below command, being sure to replace SNS Topic ARN with the ARN provided in the Outputs section of the SAM deployment and YOUR EMAIL HERE with an email address you have ownership of.

    $ aws sns subscribe --topic-arn <!SNS Topic ARN!> --protocol email --notification-endpoint <!YOUR EMAIL HERE!> --region us-east-1

<!-- Test the deployed API using cURL -->
Follow the lab docs for testing on the console or the below for testing using command line:

- Open a new terminal window in your AWS Cloud9 environment.

- Copy the below cURL command and paste it into the terminal window, replacing <api-id> with your API ID and <region> with the region where your API is deployed. You can also get the full URL from the Outputs section from your SAM deployment. You can also find the full invoke URL in the API Gateway console by navigating to Stages > dev.

    $ curl -X POST \
    'https://<api-id>.execute-api.<region>.amazonaws.com/dev/email-me' \
    -H 'Content-Type: application/json' \
    -d 'Hello from API Gateway workshop'

The Response Body output should be:

    {
        "PublishResponse": {
            "PublishResult": {
                "MessageId": "f9f3e5e7-58b4-5e4d-84bc-b97923a2ee97",
                "SequenceNumber": null
            },
            "ResponseMetadata": {
                "RequestId": "d26b09c6-99e0-5213-8e39-5558e2f612c9"
            }
        }
    }