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