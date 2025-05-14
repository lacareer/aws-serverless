<!-- Request Validation -->
Request validation is used to ensure that the incoming request message is properly formatted and contains the proper attributes. You can set up request validators in an API’s OpenAPI  definition file and then import the OpenAPI  definitions into API Gateway. You can also set them up in the API Gateway console or by calling the API Gateway REST API, AWS CLI, or one of the AWS SDKs.

The x-amazon-apigateway-request-validators  object allows you to define custom validators for your API, for this there are three extensions that can be used:

- x-amazon-apigateway-request-validators  - Defines the supported request validators for the containing API as a map between a validator name and the associated request validation rules. This extension applies to a REST API.

- x-amazon-apigateway-request-validators.requestValidator  - Specifies the validation rules of a request validator as part of the - x-amazon-apigateway-request-validators object map definition.

- x-amazon-apigateway-request-validator  - Specifies a request validator, by referencing a request_validator_name of the x-amazon-apigateway-request-validators object map, to enable request validation on   the containing API or a method. The value of this extension is a JSON string.

Read more using the links below:

API gateway extension: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-swagger-extensions.html

lab sample validation: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-swagger-extensions-request-validator.html

<!-- Test Authentication and Authorization -->

Below are the commands for testing this part of the lab for easy access during practice:

$ aws cognito-idp admin-initiate-auth --user-pool-id <YOUR_POOL_ID> --client-id <YOUR_CLIENT_ID> --auth-flow ADMIN_NO_SRP_AUTH --auth-parameters 'USERNAME=testUser,PASSWORD="<FINAL_PASSWORD>"'

$ aws cognito-idp admin-respond-to-auth-challenge --user-pool-id <YOUR_POOL_ID>  --client-id <YOUR_CLIENT_ID> --challenge-name NEW_PASSWORD_REQUIRED --challenge-responses 'USERNAME=testUser,NEW_PASSWORD=Test1234!,userAttributes.email=test@user.com' --session '<SESSION_VALUE_FROM_PREVIOUS_RESPONSE>'

$ curl --location '[insert your invoke URL here]/pricepermeter' \
--header 'Content-Type: application/json' \
--header 'Authorization: [insert your IdToken here]' \
--data '{
    "price": 400000,
    "size": 1600,
    "unit": "sqFt",
    "downPayment" : 20
}'


