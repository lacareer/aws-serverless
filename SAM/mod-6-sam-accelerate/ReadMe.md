# Herein are the instructions for this module 

# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-reference.html

<!-- Module Goals -->
Understand how SAM Accelerate can speed up the development workflow
Learn how SAM Accelerate can bypass full CloudFormation deployments to quickly apply code changes
Learn how use the SAM CLI to observe application logs

<!-- SYNC NOTE -->
You can use the above 'sync' command when you manuall create a project that contains the serverless definitions
and samconfig.toml file. Later, you can create a codepipeline for cicd or use 'sam deploy'

<!-- Notes -->
Building a serverless application changes the way developers think about testing their code. Previously, developers would emulate the complete infrastructure locally and only commit code ready for testing. AWS SAM Accelerate  is a set of features built to enable developers to test their code quickly against production AWS services in the cloud. Developers don't need to spend time setting up local emulation if they can quickly get their code integrated with production services in the cloud.

You'll make a code change to the application that AWS SAM Accelerate automatically deploys and then you'll test the update in the AWS Cloud. You’ll then make an infrastructure change that AWS SAM Accelerate automatically deploys and test that update in the AWS Cloud.

Here's a diagram depicting the SAM CLI commands for your new development workflow with SAM Accelerate.


                                //=====================================================\\
                               //                                                       \\
                               \/                                                       \/
    "sam init" ========> "sam sync --watch" ===================> "test" ============> "iterate"
                                                                    ||                    /\
                                                                    ||                    ||
                                                                    ||                    ||
                                                                    ||                    ||
                                                                    ||                    ||
                                                                    \/                    ||
                                                                "sam log --tail" ==========


Before we look at how to use SAM Accelerate, we should understand why we use it and how it can help. Let's take a look at how the sam deploy command works and compare it to SAM Accelerate.

Deploying with sam deploy requires a full CloudFormation deployment every time you want to test a code change. This is great if you have a stable application or are deploying to production, but not so much during active development. Any change to your business logic or AWS SDK calls has to go through a CloudFormation stack update. Of course, business logic can be tested using unit tests, but how do we test AWS SDK calls from Lambda to DynamoDB? Deploying to AWS every time using sam deploy takes a long time and reduces development velocity.

While there are a number of frameworks out there that aim to simulate AWS services like DynamoDB or S3 locally for the purpose of integration tests, we believe developers are best served by testing their applications against the actual services in their AWS accounts. After all, they'll be using those services in production, so if they can start testing with those services in the cloud as soon as possible, they can identify unexpected behavior and potential errors early on.

This understanding drove us towards building SAM Accelerate. We knew developers could benefit from quick feedback on updates to AWS SDK calls - like an update to a DynamoDB PutItem or SQS SendMessage request. SAM Accelerate considerably reduces deployment time for Lambda code changes, so you don't need to wait around for sam deploy each time you want to test small updates. If there's any issue in your AWS SDK calls, you can catch it early on during your testing without having to set up a local emulator.

Above is a diagram depicting the SAM CLI commands for your new development workflow with SAM Accelerate.

Once your integration tests pass and you're ready to promote your application to production, you're ready to switch back to using sam deploy. Thanks to using SAM Accelerate, you know your AWS SDK calls have been thoroughly tested against live AWS services.

<!-- Clone repo fom previous module -->
This module is a continuation of the mod-5 sam-app(repo clone into this folder) and then:

<!-- Run sam sync command -->
    cd ~/PATH_TO/sam-app
    sam sync --watch --stack-name NameOfDevelopmentStack (the name can be anything you want)

Note that the above creates a "AwsSamAutoDependency" nested stack in addition to your "NameOfDevelopmentStack"

<!-- SYNC NOTE -->
You can use the above 'sync' command when you manuall create a project that contains the serverless definitions
and samconfig.toml file. Later, you can create a codepipeline for cicd or use 'sam deploy'

<!-- Make a change to your application -->
With the sync --watch process running, update your local Lambda function code.

Remove this part of the function in app.py

    if True:
        raise Exception("This will cause a deployment rollback")

And copy and paste the print at the beginning of the handler function (hello/app.py) and save the file.

    print("Change deployed with SAM Accelerate");

<!-- Update API Gateway Path -->
SAM Accelerate isn't only limited to Lambda code changes, it can also automate deployment of infrastructure changes in template.yaml through CloudFormation.

Let's try to update the path of our API and observe how SAM Accelerate deploys it. With the sync --watch process running, update your template.yaml file.

Update the the path of the HelloWorld event of the HelloWorldFunction to be /helloworld instead of /hello. After saving the file, you will see a new CloudFormation deployment in the terminal.

        Events:
            HelloWorld:
                Type: Api
                Properties:
                Path: /helloworld
                Method: get

SAM Accelerate automatically builds your new infrastructure template and deploys your update to the AWS Cloud through CloudFormation. While this isn't as fast as using service API's, it still automates the step of manually deploying infrastructure changes to your application using sam deploy.

<!-- Test your application and check the logs -->
You're ready to test and verify the change to your API using curl and sam logs.

Enter the curl command to send a request to your API. 
Replace the url with yours copied from the API console API ==> Prod or Stages. Remember to append the new path 'helloworld'

    curl https://{restapiid}.execute-api.us-east-1.amazonaws.com/Prod/helloworld/

Now, check the logs from your Lambda function to verify the change using sam logs.
Use the logs  command to fetch logs from your application.

    cd ~/environment/sam-app
    sam logs --tail --stack-name sam-app NameOfDevelopmentStack

If you see the log statement added in the previous step in the logs, then SAM Accelerate successfully deployed the API Gateway configuration update to the AWS Cloud.