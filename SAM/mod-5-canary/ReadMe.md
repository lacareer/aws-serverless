# Herein are the instructions for this module 

# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-reference.html


<!-- Module goals -->
Understand how canary deployments reduce the risk of deployments
Learn how Lambda versions and aliases can facilitate canary deployments
Use the SAM CLI to implement canary deployments
Use CodeDeploy to monitor and automatically rollback failed deployments

<!-- Notes -->
This is a continuation of the mod-4 sam-app(repo clone into this folder) that was deploy and deployed to same repo on Codecommit. 
Modifications are being made to show Canary deployments.
Gradual deployment with canaries  is a native feature of SAM and does not require a CI/CD pipeline. This module does show screenshots of the CI/CD pipeline created in the CodePipeline module. If you didn't create a CodePipeline you can still work through this module. Know that you can still view the deployment status in AWS CodeDeploy, but you will not have a pipeline to inspect.

<!-- update template.yaml -->
Open the SAM template (sam-app/template.yaml) in your project and add the AutoPublishAlias and DeploymentPreference blocks into the HelloWorldFunction properties section as shown below.

        <!-- 

                Runtime: nodejs16.x
                AutoPublishAlias: live
                DeploymentPreference:
                Type: Canary10Percent5Minutes
                Architectures:
                - x86_64

        -->
<!-- Validate the SAM template -->
cd ~/PATH_TO/sam-app
sam validate --lint

<!-- Push the changes -->
git add .
git commit -m "Add Canary deployment configuration to SAM"
git push

<!-- Make a code change -->
AWS SAM will not deploy anything when your code hasn't changed. Since our pipeline is using AWS SAM as the deployment tool, we need to make some changes to the application.

Change the message in your Lambda function's response code "I'm using canary deployments". Remember to update the unit tests! Make the below changes to:
    
    1.  ~/PATH_TO/sam-app/hello_world/app.py

    <!-- 
    
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "I'm using canary deployments!",
            }),
        }



    2. ~/PATH_TO/sam-app/tests/unit/test_handler.py

        def test_lambda_handler(apigw_event, mocker):
        ret = app.lambda_handler(apigw_event, "")
        data = json.loads(ret["body"])

        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "I'm using canary deployments!"



     -->

<!-- Push the code -->

git add .
git commit -m "Changed return message"
git push

<!-- Watch the canary -->

1.

It will take a few minutes for your pipeline to get to the DeployTest stage which will start the canary deployment of the stage you named sam-app-dev.

Export the HTTPS endpoints to environment variables. We will work with the dev stage.

    export DEV_ENDPOINT=$(aws cloudformation describe-stacks --stack-name sam-app-dev | jq -r '.Stacks[].Outputs[].OutputValue | select(startswith("https://"))')

    export PROD_ENDPOINT=$(aws cloudformation describe-stacks --stack-name sam-app-prod | jq -r '.Stacks[].Outputs[].OutputValue | select(startswith("https://"))')

Let's start a watcher which outputs your API's message every second and helps you notice when traffic shifting starts and completes. Hit the dev API endpoint every second with curl and print the return value to the screen. This command also appends the output to the outputs.txt file that you can inspect later. You can run this command from any directory.

    watch -n 1 "curl -s $DEV_ENDPOINT | jq '.message' 2>&1 | tee -a outputs.txt"

                                        or

    watch -n 1 "curl -s $PROD_ENDPOINT | jq '.message' 2>&1 | tee -a outputs.txt"

You should see "Hello my friend" in the terminal and later "I'm using canary deployments!" in the terminal or output.txt
 

2. Go to the lambda alias and you will find a weighted traffic split between lambda version 1 and 2 (the deployment creates a +1 lambda version. In this case version 2). 

3. Go to Codedeploy under deployments to see canary deploy and traffic shifting



<!-- OPTIONAL BUT IMPORTANT MONITORING SECTION BELOW -->
=========================================================
=========================================================
<!-- Define a CloudWatch Alarm -->
Add the following alarm definition to the template.yaml file in the Resources section after the HelloWorldFunction definition.
This block defines an Amazon CloudWatch Alarm. The alarm is triggered when the Lambda function throws errors. The alarm threshold is crossed when there is one or more errors in a given minute, for two consecutive minutes.

    CanaryErrorsAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
        AlarmDescription: Lambda function canary errors
        ComparisonOperator: GreaterThanThreshold
        EvaluationPeriods: 2
        MetricName: Errors
        Namespace: AWS/Lambda
        Period: 60
        Statistic: Sum
        Threshold: 0
        Dimensions:
        - Name: Resource
            Value: !Sub "${HelloWorldFunction}:live"
        - Name: FunctionName
            Value: !Ref HelloWorldFunction
        - Name: ExecutedVersion
            Value: !GetAtt HelloWorldFunction.Version.Version

<!-- Enable canary and alarm for production -->
Alarms and canaries are great for our production deployment. You may not want or need to use canary deployments for non-production environments. Using an AllAtOnce strategy for our development stage will make deployments faster. Let's configure our serverless application to use a canary deployment and the new CloudWatch alarm only for the sam-app-prod stage using a CloudFormation Condition.
First, create a IsProduction Condition statement after the Globals section near the top of template.yaml.

    Conditions:
        IsProduction: !Equals [!Ref "AWS::StackName", "sam-app-prod"]

<!-- Change Deployment preferences -->
Next, change the DeploymentPreference to use this new IsProduction condition.

    DeploymentPreference:
        Type: !If [IsProduction, "Canary10Percent5Minutes", "AllAtOnce"]
        Alarms: !If [IsProduction, [!Ref CanaryErrorsAlarm], []]

<!-- Do below to see alarm in action and rollback by codeploy when we Introduce an error -->
Monitoring the health of your canary allows CodeDeploy to make a decision to whether a rollback is needed. If our CloudWatch Alarm gets to ALARM status, CodeDeploy will roll back the deployment automatically.
Let's break the Lambda function on purpose so that the CanaryErrorsAlarm is triggered during deployment. Update the Lambda code to throw an error on every invocation. Make sure to update the unit test, otherwise the build will fail.

1. Change the lambda code in app.py to below: ~/PATH_TO/sam-app/hello_world/app.py

    def lambda_handler(event, context):

    if True:
        raise Exception("This will cause a deployment rollback")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "I'm using canary deployments",
        }),
    }

2. Change code in: ~/PATH_TO/sam-app/tests/unit/test_handler.py

        def test_lambda_handler(apigw_event, mocker):
            assert True

<!-- Push changes -->

cd ~/PATH_TO/sam-app
git add .
git commit -m "Breaking the lambda function on purpose"
git push

<!-- Generate traffic -->

Once you've pushed the code, you will need to generate traffic on your production API Gateway endpoint. If you don't generate traffic for your Lambda function, the CloudWatch alarm will not be triggered!

If you haven't exported the PROD_ENDPOINT, run the following command.

    export PROD_ENDPOINT=$(aws cloudformation describe-stacks --stack-name sam-app-prod | jq -r '.Stacks[].Outputs[].OutputValue | select(startswith("https://"))')
    
    echo "$PROD_ENDPOINT"

Start a watch command which will hit this endpoint twice per second.

    watch -n 0.5 "curl -s $PROD_ENDPOINT"

Now that you have pushed some bad code, let's watch CodeDeploy stop the deployment.

<!-- Monitor rollback -->

If you created a CI/CD pipeline, navigate to your pipeline in the CodePipeline console and keep an eye on its progression. You will see that the DeployTest stage is deployed quickly since it's using the AllAtOnce strategy. Even though our code is broken, thanks to our hard coded error, it's deployed automatically in the DeployTest stage.

Once your pipeline moves to the DeployProd stage, things gets more interesting. In the terminal window where you are running the watch command, you'll notice the message flash from I'm using canary deployments to Internal server error.

After a few minutes, you will see CodeDeploy mark this deployment as failed and roll back to the previous version. The Internal server error messages will go away as all traffic is shifted back to the previous version.

Navigate to the AWS CodeDeploy Console  Deployments page. Look at the Deployment which may be In-Progress or Stopped, depending on whether the rollback is complete. Click on the Deployment Id to see its details.

You will see that CodeDeploy detected CanaryErrorsAlarm has triggered and stopped the deployment.

Congratulations! You setup deployments for Lambda functions that gradually shift traffic and automatically rolls back code when it detects errors.