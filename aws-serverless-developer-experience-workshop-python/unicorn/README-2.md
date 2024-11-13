<!-- Our deployment methodology in US-WEST-2-->
Many teams working on projects with multiple subsystems opt for the monorepo approach. Monorepos can generally improve development speed and collaboration efficiency. We've chosen this approach because, despite having independent subprojects, these projects collaborate to form a single, concise application workflow.

CodePipeline and Monorepos
In a monorepo scenario, AWS CodePipeline  cannot be directly triggered by repository changes, or every subproject would be built, tested, and deployed, even if unchanged. This is inefficient and can cause confusion when troubleshooting.

To address this, you'll leverage a modified version of the AWS reference implementation for monorepos with CodeCommit and CodePipeline (https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/automatically-detect-changes-and-initiate-different-codepipeline-pipelines-for-a-monorepo-in-codecommit.html).

A new AWS SAM Pipeline template supports monorepos with AWS CodePipeline. With it, you'll automate provisioning of the supporting infrastructure to trigger the appropriate pipeline as you add projects to your repository. The template deploys an AWS Lambda function responding to CodeCommit changes (by filtering EventBridge events) and, based on which files changed since the last commit, triggers the appropriate CodePipeline.

Each subproject will have its own pipeline, which you can manage, trigger, and operate independently from others.

If you would like to see how this works, the pipeline template is freely available here: https://s12d.com/aws-sam-pipelines-monorepo 

Using other pipeline templates
This workshop uses AWS CodePipeline for all CI/CD deployments, however, feel free to try others if you are running this workshop on your own.

<!-- Deploying the shared infrastructure -->
You need to deploy all three stacks in order to progress with the workshop!

Wait for all 3 stacks to deploy and ensure that they have completed successfully, you will see CREATE_COMPLETE message next to each stack once deployment has completed.

What is the shared infrastructure?
The Unicorn Properties has shared infrastructure dependencies that aid in the integration of services and application functionality

1. AWS Systems Manager Parameter Store: the namespaces of the services for each environment. These are referenced throughout CloudFormation templates and play an important part in consistently applying the namespace definitions across the three domains and environments.

/uni-prop/[local|dev|prod]/UnicornContractsNamespace     # Stores the namespace of the Unicorn.Contracts domain
/uni-prop/[local|dev|prod]/UnicornPropertiesNamespace    # Stores the namespace of the Unicorn.Properties domain
/uni-prop/[local|dev|prod]/UnicornWebNamespace           # Stores the namespace of the Unicorn.Web domain
/uni-prop/[local|dev|prod]/ImagesBucket 

2. Amazon S3 bucket: buckets containing the property images (one for ech environment).

<!-- Verify the shared infrastructure -->
Check to make sure that you have the following stacks. If you don't see these stacks follow the steps to deploy the shared resources

uni-prop-prod-shared (Production environment)
uni-prop-dev-shared (dev environment)
uni-prop-local-shared (local development environment)

<!-- Dependency Management -->

We are using Poetry  to manage dependencies in the Python project. You are of course welcome to use your own if you wish. To install Poetry (on MacOS or Linux):

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

Once you have everything installed, get started by Initializing your project .