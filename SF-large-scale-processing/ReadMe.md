<!-- workshop link -->

# # https://catalog.us-east-1.prod.workshops.aws/workshops/2a22e604-2f2e-4d7b-85a8-33b38c999234/en-US

 <!-- Cloudformation custom resources -->

Note that some/all of the cloudformation templates are using custom resources. This is to make sure the associated lambda runs each time when the stack is created, updated or deleted. This makes sure the S3 buckets contains the required files/data when the stack is deployed initially and updates the content when the stack is updated.

References: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html

"Custom resources enable you to write custom provisioning logic in templates that AWS CloudFormation runs anytime you create, update (if you changed the custom resource), or delete stacks. For example, you might want to include resources that aren't available as AWS CloudFormation resource types. You can include those resources by using custom resources. That way you can still manage all your related resources in a single stack.

Use the AWS::CloudFormation::CustomResource or Custom::MyCustomResourceTypeName resource type to define custom resources in your templates. Custom resources require one property: the service token, which specifies where AWS CloudFormation sends requests to, such as an Amazon SNS topic."