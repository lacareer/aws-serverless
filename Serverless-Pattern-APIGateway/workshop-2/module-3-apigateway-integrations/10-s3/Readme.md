<!-- Test the deployed API using cURL -->
You can test uisng the console by following the lab instructions or using the below:

- Open a new terminal window in your AWS Cloud9 environment.

- Copy the below cURL command and paste it into the terminal window, replacing <api-id> with your API ID and <region> with the region where your API is deployed. You can also get the full URL from the Outputs section from your SAM deployment. You can also find the full invoke URL in the API Gateway console by navigating to Stages > dev.

    $curl -X PUT \
    'https://<api-id>.execute-api.<region>.amazonaws.com/dev/sample-2.txt' \
    -H 'Content-Type: application/json' \
    -d 'One more test file. This time, we are using cURL to test the integration'

This code will create a new file inside our S3 bucket. Note that the file name is specified inside the URL path /sample-2.txt and the file content is sent as the payload data. Now let's check the content of our file's by requesting it using cURL

- Using your terminal, run the following command:

    $curl -X GET \
    'https://<api-id>.execute-api.<region>.amazonaws.com/dev/sample-2.txt' \
    -H 'Content-Type: application/json' 

- Using your terminal, run the following command:

    $curl -X DELETE \
    'https://<api-id>.execute-api.<region>.amazonaws.com/dev/sample-2.txt' \
    -H 'Content-Type: application/json' 