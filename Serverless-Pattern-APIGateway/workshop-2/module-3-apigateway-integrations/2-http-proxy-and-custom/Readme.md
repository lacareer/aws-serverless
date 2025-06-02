<!-- Test Integration -->
After you create your API Gateway REST API with HTTP integration, you can test it .

***For HTTP Proxy Integration:***


***For HTTP Custom Integration:***
Let's test the proxy integration first.

- Open a new terminal window in your AWS Cloud9 environment.

- Copy the following cURL command and paste it into the terminal window, replacing <api-id> with your APIs RestApiEndpoint id that was the output of your SAM deploy and <region> with the region where your API is deployed. You can also find the full invoke URL in the API Gateway console by navigating to Stages > dev.

    $ curl -X GET 'https://<api-id>.execute-api.<region>.amazonaws.com/dev/items'

The Response Body output should be:

    [{"price":87.7,"id":"UI678OI","name":"Echo Dot"}] or []