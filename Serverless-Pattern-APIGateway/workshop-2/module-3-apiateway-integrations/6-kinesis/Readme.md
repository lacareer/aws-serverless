<!-- Test the deployed API using cURL -->

You can test uisng the console by following the lab instructions or using the below:

Open a new terminal window in your AWS Cloud9 environment.

Copy the below cURL command and paste it into the terminal window, replacing <api-id> with your API ID and <region> with the region where your API is deployed. You can also get the full URL from the Outputs section from your SAM deployment. You can also find the full invoke URL in the API Gateway console by navigating to Stages > dev.

    $ curl -X PUT \
        'https://<api-id>.execute-api.<region>.amazonaws.com/dev/streams/KinesisStreamAPIGW/record' \
        -H 'Content-Type: application/json' \
        -d '{"Data": "eyJhIjogMX0=","PartitionKey": "test"}'

The Response Body output should be:

    {
    "SequenceNumber":"49642425449682996849330992744638041493183653490899025922",
        "ShardId":"shardId-000000000000"
    }