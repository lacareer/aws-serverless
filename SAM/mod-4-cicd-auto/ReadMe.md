# Herein are the instructions for this module 


# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-reference.html


<!-- Module goals -->
Learn how to create a CI/CD pipeline for a SAM appliction using AWS CodePipeline
Inspect the generated CI/CD pipeline to understand how it works
Learn how to enable unit tests for the generated CI/CD pipline
<!-- Notes -->
Note that the SAM app has been built from the previous module. Rather than use "sam deploy" manually, here we will us a pipeline
In this chapter, you are going to use a feature of SAM called SAM Pipelines . When you are ready to deploy your serverless application in an automated manner, you can generate a deployment pipeline for your CI/CD system of choice. AWS SAM provides a set of starter pipeline templates with which you can generate pipelines in minutes using the sam pipeline init command.

Currently, the AWS SAM CLI supports generating starter CI/CD pipeline configurations for the following providers:

AWS CodePipeline 
Jenkins 
GitLab CI/CD 
GitHub Actions 
Bitbucket Pipelines 

In this chapter, you are going to learn how to setup a CI/CD pipeline using AWS CodePipeline . You will use SAM Pipelines  to generate a self-updating, multi-stage CI/CD pipeline.

Below are the steps:

<!-- create an aws codecommit repo  -->
aws codecommit create-repository --repository-name sam-app

    Make sure your Git is configured and looks similar to what is shown below. This is so you can communicate with aws codecommit

[credential "https://git-codecommit.ca-central-1.amazonaws.com"]
	helper = !aws codecommit credential-helper --profile iamadmin-general $@ 
	UseHttpPath = true
[core]
	editor = code --wait
[user]
	name = Chuks Ogu
	email = Chuksogu98@yahoo.com

<!-- Initialize a git repo -->
First copy the sam-app from mod-3 and run the below:

    cd ~/PATH_TO/sam-app
    git init -b main
    echo -e "\n\n.aws-sam" >> .gitignore
    echo -e "target" >> .gitignore
    git add .
    git commit -m "Initial commit"
    git remote add origin "remote_codecommit_url"
    git push -u origin main

    <!-- don't run the below although the workshop say you should. This file is used for sample deployment -->
    echo -e "samconfig.toml" >> .gitignore

You sam-app code should now be in AWS Codecommit

<!-- Build a pipeline notes -->
SAM Pipelines  works by creating a set of configuration and infrastructure files you use to create and manage your CI/CD pipeline.

As of this writing, SAM Pipelines can bootstrap CI/CD pipelines for the following providers:

Jenkins
GitLab CI/CD
GitHub Actions
Bitbucket Pipelines
AWS CodePipeline

SAM Pipelines is a feature which bootstraps CI/CD pipelines for the listed providers. This saves you the work of setting them up from scratch. However, you can use SAM as a deployment tool with any CI/CD provider. You use various sam commands to build and deploy SAM applications regardless of your CI/CD toolset. Furthermore, the configurations SAM Pipelines creates are a convienence to get you started. You are free to edit these CI/CD configuration files after SAM creates them.

SAM Pipelines creates appropriate configuration files for your CI/CD provider of choice. For example, when using GitHub Actions, SAM will synthesize a .github/workflows/pipeline.yaml file. This file defines your CI/CD pipeline using GitHub Actions. In this workshop, we will use AWS CodePipeline. As you will soon see, SAM creates multiple files, one of which is a CloudFormation template named codepipeline.yaml. This template defines multiple AWS resources that work together to deploy our serverless application automatically.

    <!-- CodePipeline architecture -->
At the end of this section, we will have a self-updating CI/CD pipeline using CodePipeline that will perform the following steps.

Trigger after a commit to the main branch (Source in the screenshot below)
Look for changes to the pipeline itself and self-update using CloudFormation (UpdatePipeline)
Run unit tests via CodeBuild (UnitTest)
Build and package the application code via CodeBuild (BuildAndPackage)
Deploy to a dev/test environment (DeployTest)
Deploy to a production environment (DeployProd)

<!-- Creating the SAM Pipeline -->
There are three distinct steps with SAM Pipelines and AWS CodePipeline.

Create required IAM roles and infrastructure
Create CloudFormation pipeline template
Deploy CloudFormation pipeline template
SAM Pipelines automates all of this for us.

    <!-- Note -->
The sam pipeline init --bootstrap command will guide you through a long series of questions. In this section of the lab, it's critical to answer the questions as documented below.

<!-- Create required IAM roles and infrastructure -->

    <!-- Dev stage: setup using command prompt-->

        A list of the questions and required answers for this workshop is enumerated below. Note that numbers may be different when choosing from an enumerated list. The full output and answers are provided below as an additional reference.

        Select a pipeline template to get started: AWS Quick Start Pipeline Templates (1)
        Select CI/CD system: AWS CodePipeline (5)
        Which pipeline template would you like to use? Two-stage pipeline (1)
        Do you want to go through stage setup process now? [Y/n]:
        [1] Stage definition. Stage configuration name: dev
        [2] Account details. Select a credential source to associate with this stage: default (named profile) (2)
        Enter the region in which you want these resources to be created: Your region of choice
        Enter the pipeline IAM user ARN if you have previously ... [] return/enter
        Enter the pipeline execution role ARN if you have previously ... []: return/enter
        Enter the CloudFormation execution role ARN if you have previously ... []: return/enter
        Please enter the artifact bucket ARN for your Lambda function. If you do not ... []: return/enter
        Does your application contain any IMAGE type Lambda functions? [y/N]: N
        Press enter to confirm the values above ... : return/enter
        Should we proceed with the creation? [y/N]: y

    <!-- Note that once the below command is ran, sam pipeline init --bootstrap, each resource is created one after the other, dev => prod => pipeline in the same terminal -->
    Now run the below command and respond to the prompts using the above answers:

        cd ~/PATH_TO/sam-app
        sam pipeline init --bootstrap


    should see something similar to below once complete
    <!-- 
                    Successfully created!
        The following resources were created in your account:
                - Pipeline IAM user
                - Pipeline execution role
                - CloudFormation execution role
                - Artifact bucket
        Pipeline IAM user credential:
                AWS_ACCESS_KEY_ID: AAAAAAAAAAAAIFRDVPDX
                AWS_SECRET_ACCESS_KEY: xxxxxxxxxxxxxxxxxxxxxxkMYI9RatNgVcIybUwh
     -->

    These resources were created with a CloudFormation stack that SAM Pipelines synthesized and launched. You may optionally navigate to the CloudFormation console and inspect this stack to see everything that was created.

    In this step, SAM pipelines created a Pipeline IAM user with an associated ACCESS_KEY_ID and SECRET_ACCESS_KEY shown in the output. The CodePipeline we will eventually create uses this user to deploy artifacts to your AWS accounts. This IAM user will be the default value in subsequent steps.


    <!-- Prod stage: setup using command prompt-->

    SAM Pipelines detects that a second stage is required and prompts you to go through the set-up process for this new stage. Since you have created the necessary resource for the dev stage, you need to go through the same steps for a prod stage. 

    Select y to the question, "Do you want to go through stage setup process now? ... [y/N]:". This will continue the wizard to setup the prod stage.

    Most questions can be answered the same as the dev stage, created above. The one change you need to make is first question which is the "Stage configuration name" which should be prod. Also, note the default value for the "Pipeline IAM user ARN" (question 4) prompt will be filled in. This is the ARN for the pipeline user created during the dev stage above.

    [1] Stage definition. Stage configuration name: prod
    [2] Account details. Select a credential source to associate with this stage: default (named profile) (2)
    Enter the region in which you want these resources to be created: Your region of choice
    Pipeline IAM user ARN: arn:aws:iam::123456789012:user/aws-sam... : return/enter
    Enter the pipeline execution role ARN if you have previously ... []: return/enter
    Enter the CloudFormation execution role ARN if you have previously ... []: return/enter
    Please enter the artifact bucket ARN for your Lambda function. If you do not ... []: return/enter
    Does your application contain any IMAGE type Lambda functions? [y/N]: N
    Press enter to confirm the values above ... : return/enter
    Should we proceed with the creation? [y/N]: y
    Once this is complete, SAM will launch a new CloudFormation stack. This stack will create new resources for your prod deployment. You can optionally inspect this template in the CloudFormation console. It looks very similar to the dev pipeline stack.


    Upon complete the screen should show a similar message like when the dev stage completed


<!-- Create CloudFormation pipeline template -->
    Now that AWS SAM has created supporting resources, we'll continue to create a CloudFormation template that will define our entire CI/CD pipeline.

    A list of the questions and required anwers for this workshop is enumerated below. Note that numbers may be different when choosing from an enumerated list. The full output and answers is provided below as an additional reference.

    What is the Git provider? Choice []: CodeCommit (2)
    What is the CodeCommit repository name?: sam-app (or your actual repo name)
    What is the Git branch used for production deployments? [main]: main
    What is the template file path? [template.yaml]: template.yaml
    Select an index or enter the stage 1's configuration name (as provided during the bootstrapping): 1
    What is the sam application stack name for stage 1? [sam-app]: sam-app-dev
    Select an index or enter the stage 2's configuration name (as provided during the bootstrapping): 2
    What is the sam application stack name for stage 2? [sam-app]: sam-app-prod

    What we've just done is create the CloudFormation template and supporting configuration files to create a full CI/CD Pipeline using AWS CodePipeline, CodeBuild, and other AWS services.

    Your project should have the structure below (only the most relevant files and folders are shown).

    └── sam-app
        ├── codepipeline.yaml       # (new) CodePipeline CloudFormation template
        ├── assume-role.sh          # (new) Helper script for CodePipeline
        ├── pipeline/               # (new) Build Specs for CodeBuild
        ├── events
        ├── hello-world/            # SAM application root
        ├── README.md
        ├── samconfig.toml          # Config file for manual SAM deployments
        └── template.yaml           # SAM template

    
    You can optionally open up codepipeline.yaml and other files to see what SAM Pipelines created for us. Looking at codepipeline.yaml you can see that there are nearly 700 lines of CloudFormation that SAM created. Think about how much time you just saved using SAM Pipelines rather than crafting this by hand!
    We haven't created any CI/CD systems just yet! You'll do that next. First, you need to commit your CI/CD configuration files into your repository. Once that's done, you can create your CodePipeline with CloudFormation via SAM.

<!-- Commit new changes  to repo -->
    git status
    git add .
    git commit -m "Adding SAM CI/CD Pipeline definition"
    git push

<!-- Create actual pipeline -->

    Now that the configuration is checked into source control, you can create a new CloudFormation stack which will set up our CI/CD pipeline. You will use the sam deploy command to launch this new stack. It's important to recognize that you're using SAM's ability to launch arbitrary CloudFormation templates. SAM isn't building or deploying your serverless application here, rather launching the codepipeline.yaml CI/CD template.
    Now run:

        cd ~/PATH_TO/sam-app
        sam deploy -t codepipeline.yaml --stack-name sam-app-pipeline --capabilities=CAPABILITY_IAM

    This will take a few minutes to complete, so be patient! You can optionally open the CloudFormation console to watch the progress of this new stack. Eventually, the stack will complete and you can see the final AWS resources it created

<!-- Inspect the pipeline -->
    Once the sam-app-pipeline CloudFormation stack has completed, you will have a new CodePipeline pipeline. Navigate to the CodePipeline Console . You should see a single pipeline. If you've navigated here soon after deploying the Pipeline CloudFormation stack, you will see your new pipeline executing its first deployment.
    Let your pipeline run every stage. After it finishes, all stages will be green.

    You may have noticed our sam-app-dev is deployed in a CodePipleine stage named DeployTest. The DeployTest name is hardcoded in the codepipeline.yaml file and does not relate in any way to our dev application that we named sam-app-dev. When you use this template outside this workshop you could rename DeployTest to anything appropriate

<!-- Inspect the dev/prod stages -->
    Nagivate to the CloudFormation console. After your first pipeline has finished, you will notice two new stacks named sam-app-dev and sam-app-prod. These are the names you provided during the SAM Pipelines wizard in the previous step.

    CodeBuild created the sam-app-dev stack during the DeployTest Pipeline step. Similarly, CodeBuild created sam-app-prod during the DeployProd step.

    Look at the Outputs tab for each of these CloudFormation stacks to see the API endpoints. You can use curl or other methods to verify the functionality of your two new APIs. You can export the URL endpoints for both stages in a terminal.

        export DEV_ENDPOINT=$(aws cloudformation describe-stacks --stack-name sam-app-dev | jq -r '.Stacks[].Outputs[].OutputValue | select(startswith("https://"))')
        
        export PROD_ENDPOINT=$(aws cloudformation describe-stacks --stack-name sam-app-prod | jq -r '.Stacks[].Outputs[].OutputValue | select(startswith("https://"))')

        echo "Dev endpoint: $DEV_ENDPOINT"
        echo "Prod endpoint: $PROD_ENDPOINT"

        curl -s $DEV_ENDPOINT
        curl -s $PROD_ENDPOINT


