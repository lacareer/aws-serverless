<!-- Test the deployed API using cURL to WRITE an item -->
You can test uisng the console by following the lab instructions or using the below:

- Open a new terminal window in your AWS Cloud9 environment.

- Copy the below cURL command and paste it into the terminal window, replacing <api-id> with your API ID and <region> with the region where your API is deployed. You can also get the full URL from the Outputs section from your SAM deployment. You can also find the full invoke URL in the API Gateway console by navigating to Stages > dev.

    $ curl -X POST \
        'https://<api-id>.execute-api.<region>.amazonaws.com/dev/resource/2' \
        -H 'Content-Type: application/json' \
        -d '{"name": "John", "lastName": "Doe", "email": "jd@example.com"}'

The Response Body output should be:

 {
    
 }

<!-- Test the deployed API using cURL to READ an item -->
You can test uisng the console by following the lab instructions or using the below:

- Open a new terminal window in your AWS Cloud9 environment.

- Copy the below cURL command and paste it into the terminal window, replacing <api-id> with your API ID and <region> with the region where your API is deployed. You can also get the full URL from the Outputs section from your SAM deployment. You can also find the full invoke URL in the API Gateway console by navigating to Stages > dev.

    $ curl -X GET \
        'https://<api-id>.execute-api.<region>.amazonaws.com/dev/resource?id=2' \
        -H 'Content-Type: application/json' 

The Response Body output should be:

    {
    "Names": [
        {
            "id": "2",
            "name": "Joanna",
            "lastName": "Doe",
            "email": "joannad@example.com"
        }           
        ]
    }