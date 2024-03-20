

<!-- Download the workshop code -->

First you need to download the code required for this workshop. Run the following command in the bash terminal:

    sam init --location https://ws-assets-prod-iad-r-dub-85e3be25bd827406.s3.eu-west-1.amazonaws.com/e8738cf6-6eb0-4d1d-9e98-ae240d229535/code.zip

<!-- Build the lab artifacts from source -->

We provide you with an AWS SAM  template which we will use to bootstrap the initial state. 
In the bash tab (at the bottom) in your IDE, run the following commands to build the lab code:

    cd ~/wild-rydes-async-messaging/code/lab-1
    sam build

<!-- Deploy the application -->
Now we are ready to deploy the application, by running the following command in the lab-1 directory:

    export AWS_REGION=$(aws --profile default configure get region)  [This is optional command]

    sam deploy \
        --stack-name wild-rydes-async-msg-1 \
        --capabilities CAPABILITY_IAM \
        --region $AWS_REGION \
        --guided

