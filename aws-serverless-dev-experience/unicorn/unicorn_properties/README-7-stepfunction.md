<!-- Approvals workflow -->
In this section, you will build the Unicorn Properties approval workflow. There are 4 main parts to this workflow:

1. Check if contract exists
You first check if a contract exists before proceeding. A contract must be in place before publishing any property online. If no contract exists, an error is raised, and the process enters a failed state.

2. Check if content is appropriate
For a property listing upload, you ensure that the images and description are appropriate. Inappropriate images or descriptions with negative sentiment will result in the listing being rejected.

3. Check if contract is approved
After verifying the content, you ensure that the contract with the seller is approved. The agency may take time to approve the contract. You must pause the workflow until the contract is approved before publishing listings for public consumption.

4. Publish an event to signal the completion of the evaluation
Once all checks and balances are complete, you notify the web component by emitting a PublicationEvaluationCompleted event with an APPROVED or DECLINED result, indicating whether the property

<!-- SF Code -->
find code here: https://ws-assets-prod-iad-r-iad-ed304a55c2ca1aee.s3.us-east-1.amazonaws.com/9a27e484-7336-4ed0-8f90-f2747e4ac65c/prebuilt_workflow.yaml

Paste in /home/wsl/chuks-project-directory/aws-serverless/aws-serverless-dev-experience/unicorn/unicorn_properties/state_machine/property_approval.asl.yaml

<!-- Make sure that the template follows best practices. -->
There are a few mechanisms to ensure that the solution follows best practices. For this workshop, we want to utilise cfn-lint , paired with serverless-rules .

In the terminal, run:

    cfn-lint template.yaml -a cfn_lint_serverless.rules

<!-- Deploy solution -->
Run:

    poetry export --without-hashes --format=requirements.txt --output=src/requirements.txt
    sam build
    sam deploy

# Done
Congratulations! You have now successfully copied over the changes you made using Step Functions Workflow Studio into your codebase, and deployed it using AWS SAM.    