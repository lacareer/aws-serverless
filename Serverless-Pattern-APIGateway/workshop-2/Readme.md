<!-- Welcome to WorkShop 2 -->

** Workshop was completed using us-east-1 region **

***https://catalog.us-east-1.prod.workshops.aws/workshops/5079f77b-4228-442e-baba-06a1065f67e1/en-US***

<!-- Workshop setup -->

Add the following files in ws-infra folder to an s3 bucket
    - shared-resources.yaml
    - module-1.yaml
    - module-3.yaml

Now, using the AWS console, go to CloudFormation, deploy the workshop infrastructure using template.yaml and give it the stack name: ws-aws-apigateway

OR

You can also deploy the individual template in the same order: shared-resources.yaml, module-1.yaml, and module-3.yaml with named stack being api-gateway-workshop-shared, api-gateway-workshop-functions, and api-gateway-workshop-vpc respectively



