<!-- Our deployment methodology in ca-central-1-->
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

<!-- Project initialiazation -->
The entire content of this directory was gotten using 'sam init'

    $sam init --location 'https://ws-assets-prod-iad-r-iad-ed304a55c2ca1aee.s3.us-east-1.amazonaws.com/9a27e484-7336-4ed0-8f90-f2747e4ac65c/init/python_unicorn_contracts.zip'

Then:
- When cookiecutter asks for a project name, e.g. project_name [unicorn_contracts]: keep default value (press Enter).

- Open the Unicorn Contracts folder in your terminal, and explore the project source and test projects.   

<!-- Validating the template -->
A common development practice with Serverless applications is checking the integrity of your AWS SAM templates. Tools such as cfn-lint and serverless-rules help you do this, and apply best practices to your serverless resources.

To help you understand how to use this tool, we have intentionally omitted configuration from your template. Fix these before you do your first deployment.
- Install linters:

    - pip3 install cfn-lint cfn-lint-serverless 

- Navigate to the root of the Unicorn Contracts folder.
- Run the following command in your terminal.

Then run: 

    cfn-lint template.yaml -a cfn_lint_serverless.rules 

(THE ABOVE THREW A URLLIB ERROR THAT I RESOLVE BY UPGRDADING THE PYTHON REQUEST MODULE)

To read more about this linter, go to:
- https://awslabs.github.io/serverless-rules/
- https://github.com/aws-cloudformation/cfn-lint


<!-- NOTE -->
serverless-rules  is a plugin for cfn-lint . Running cfn-lint without serverless-rules will validate just your CloudFormation template, but we recommend running them together.

Note, you can also use the AWS SAM command sam validate --lint which is functionally equivalent to running cfn-lint template.yaml. However, this does not allow you to attach the serverless-rules plugin.

<!-- Initial deployment -->
In the terminal, navigate to the unicorn_contracts folder. Here you will find the samconfig.yaml file. We have created this file so that you can easily run your first deployment.

First, install the dependencies for your application. Depending on the runtime (Python in my case), different dependency management tool has been used for this:

    poetry install
    poetry export --without-hashes --format=requirements.txt --output=src/requirements.txt

OR BELOW IF THE ABOVE DID NOT WORK FOR YOU (I DID BELOW)

    sudo apt install pipx (IF NOT INSTALLED)
    pipx install poetry
    poetry export --without-hashes --format=requirements.txt --output=src/requirements.txt

Build and deploy the service using the following commands (make you resolve any template issues before you do):

    cfn-lint template.yaml -a cfn_lint_serverless.rules
    sam build --cached
    sam deploy

<!-- Synchronize code changes with sam sync -->
The AWS SAM sam sync command provides options to quickly sync local application changes to the AWS Cloud. By default, sam sync runs a full AWS Cloudformation stack update. Running sam sync --watch with --code will provide a way to run just code synchronization, speeding up start time skipping template changes. Remember to update the deployed stack by running without --code for infrastructure changes. sam sync also supports nested stacks and nested stack resources.

To start the sync process, run following command in your terminal:

    sam sync --stack-name uni-prop-local-contracts --watch

You may see a warning message advising that this feature should only be used in Development. Type in Y to confirm and proceed.    