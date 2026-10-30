# Reference: https://aws.amazon.com/blogs/compute/build-scalable-rest-apis-using-amazon-api-gateway-private-integration-with-application-load-balancer/

The old way of accessing private resources from API Gateway was to use a NLB and ALB

This new removes the need to use a NLB

Note that this new template is not a serverless template although it can be and deployed using SAM


<!-- Deploy template-->
# abandoned bcs it did not work. Try at a later time using the lab docs
- Since it is not a SAM template you can just use the console to deploy it

- Wait for it to succeed

<!-- Test the deployed API using cURL -->
Test the end point using the  syntax: https://<rest-api-id>.execute-api.<your-aws-region>.amazonaws.com/<your-stage-name>/internal-alb

    $ curl https://t6qbwm0jni.execute-api.us-east-1.amazonaws.com/test/internal-alb

        {"message": "Hello from internal ALB"}[cogu@ip-172-19-160-197 ~]$ 
 