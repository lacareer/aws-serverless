Workshop url: 
<!-- https://catalog.workshops.aws/serverless-developer-experience/en-US -->

<!-- DEPLOYMENT OF READ MADE INFRA -->
Move/cd into each unicorn_contracts, unicorn_properties, unicorn_web directories and run the below coomand to deploy the infrastructure

   sam build && sam deploy

<!-- Workshop steps to build and understand infra -->
1. Deploy the share SSM secret infrastructure using the uni-prop-namespaces.yaml file using the console. Ensure that stack name is 'uni-prop-namespaces'

   Afterward, deploy the s3-common.yaml three times passing local, dev, and dev for the 1st, 2nd, and 3rd time respectively. And make sure the stack names corresppond to below:
   
   uni-prop-local-shared
   uni-prop-dev-shared
   uni-prop-prod-shared

2: Got to readme files in unicorn contracts directory

3: Got to readme files in unicorn properties directory

4: Got to readme files in unicorn web directory
