#### NOTE THAT I STARTED THE "Deploy Network LB and EC2" BUT COULD NOT GET MY NLB TO GET HEALTHY STATUS FROM MY INSTANCE

### SO I STOPPED. THIS LAB WAS NOT COMPLETED

<!-- Deploy Network LB and EC2-->
# abandoned bcs it did not work. Try at a later time using the lab docs
Before deploying your SAM aaplication, do the following in this order using the console:

1-   Create an EC2 KeyPair and save the name somewhere

2-   Deploy the vpc.yaml template and save the VpcID, PrivateSubnet1 and PrivateSubnet2 (as MyPrivateSubnet1  and MyPrivateSubnet1 respectively)

3-   Deploy the networkLB.yaml using the save parameters from the previous steps (1 and 2) and save the DNS name and the ARN of the Network Load Balancer.

4-  Read and understand the template.yaml and openapi.yaml files

5-  Use the DNS name and the ARN of the Network Load Balancer values when you deploy the template.yaml using SAM or just hard code as default which I did
    
    Then run:

        sam build && sam deploy --guided

<!-- Test the deployed API using cURL -->
Follow the lab docs for testing on the console or the below for testing using command line:

- Open a new terminal window in your AWS Cloud9 environment.

- Copy the below cURL command and paste it into the terminal window, replacing <api-id> with your API ID and <region> with the region where your API is deployed. You can also get the full URL from the Outputs section from your SAM deployment. You can also find the full invoke URL in the API Gateway console by navigating to Stages > dev.

    curl -X GET 'https://<api-id>.execute-api.<region>.amazonaws.com/dev/internal-nlb'

The Response Body output should be:

    <h1>Hello World from ip-10-0-10-63.ap-south-1.compute.internal</h1>    