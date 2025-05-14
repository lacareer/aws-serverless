<!-- Authentication and Authorization -->
***https://spec.openapis.org/oas/v3.1.0#openapi-specification***
At this point, our API is publicly exposed and you need to protect it by implementing an authentication mechanism. API Gateway supports IAM auth, Cognito User Pools, and custom authorizers written as Lambda function. In this lab, you will leverage Amazon Cognito  to have only registered users use your module-2-my-first-api API.

Below are the steps to enable authentication and authorization on the API:

- Create Cognito User Pool
- Create a User
- Login as user
- Update API Gateway Authentication
- Test the API with authentication

<!-- Create Cognito User Pool -->
The first step is to create a Cognito User Pool . A User Pool is our user directory. We can register users in the pool and users can authenticate with their credentials. The outcome of a successful authentication against User Pools is an Open ID Connect-compatible (OIDC)  identity token and a JWT access token

Add the Cognito User Pool  and a User Pool Client  to your SAM template file template.yaml.

<!-- Create a User -->
The next step is to create users that will be allowed to call our module-2-my-first-api. Perform the following:

1- Open the Amazon Cognito  user pools console and sign in.
2- Click on CostCalculatorUserPool to open the user pool.
3- In the Users tab click on Create User
4- Enter the following values:
    - On Invitation Message select Don't send an invitation.
    - UserName: testUser
    - On Temporary password select Set a password.
    - In password paste: testUser123!
5- Click Create User    

Now follow the lab instructions for the rest of the commands to login, change password, and get token

First time login (Enter the following command. Replace the user-pool-id, client-id attributes):

       aws cognito-idp admin-initiate-auth --user-pool-id <YOUR_POOL_ID> --client-id <YOUR_CLIENT_ID> --auth-flow ADMIN_NO_SRP_AUTH --auth-parameters 'USERNAME=testUser,PASSWORD="testUser123!"'

The first response to this request should be an authentication challenge, the user pool reminds you that you need to change the password for the user. If you recall, when we created the user it asked us for a temporary password, not the final one

{
   "ChallengeName": "NEW_PASSWORD_REQUIRED",
   "Session": "...",
   "ChallengeParameters": {
      "USER_ID_FOR_SRP": "testUser",
      "requiredAttributes": "[]",
      "userAttributes": "{\"email_verified\":\"true\",\"phone_number_verified\":\"true\",\"phone_number\":\"+14325551212\",\"email\":\"user@eMail\"}"
   }
}

Use the CLI to set the final password for the user. Replace the pool ID, client ID, username/pwd and the session attributes. The session value can be retrieved from the response to step 2. Ensure your final passwords contains lower case, upper case, number and character symbols:

       aws cognito-idp admin-respond-to-auth-challenge --user-pool-id <YOUR_POOL_ID>  --client-id <YOUR_CLIENT_ID> --challenge-name NEW_PASSWORD_REQUIRED --challenge-response "USERNAME=testUser,NEW_PASSWORD=<FINAL_PASSWORD>" --session "<SESSION_VALUE_FROM_PREVIOUS_RESPONSE>"

The output from this call should be a valid session:

{
   "ChallengeParameters": {},
   "AuthenticationResult": {
      "AccessToken": "...",
      "ExpiresIn": 3600,
      "TokenType": "Bearer",
      "RefreshToken": "...",
      "IdToken": "..."
   }
}       



<!-- Update API Gateway Authentication -->
Now that we already have the Cognito UserPool  properly configured and the user created to login, we will update the OpenAPI  definition to add the new authorizer to the specification file.

Here we're defining the security  requirement to our path /pricepermeter on method POST. Here we're defining the CostCalculatorAuthorizer as the security requirement during the executions:

    security:
        - CostCalculatorAuthorizer: []

Defines a security scheme (***https://spec.openapis.org/oas/v3.1.0#security-scheme-object***) that can be used by the operations. Here we're declaring a new authorizer called CostCalculatorAuthorizer AND we're specifying the type apiKey to our authorizer, which will be present at the Authorization header:


    securitySchemes:
        CostCalculatorAuthorizer:
            type: apiKey
            name: Authorization
            in: header
            x-amazon-apigateway-authtype: cognito_user_pools
            x-amazon-apigateway-authorizer:
                type: cognito_user_pools
                providerARNs:
                  - Fn::GetAtt: [CostCalculatorUserPool, Arn]

<!-- Test Authentication and Authorization -->

Below are the commands for testing this part of the lab for easy access during practice:

$ aws cognito-idp admin-initiate-auth --user-pool-id <YOUR_POOL_ID> --client-id <YOUR_CLIENT_ID> --auth-flow ADMIN_NO_SRP_AUTH --auth-parameters 'USERNAME=testUser,PASSWORD="<FINAL_PASSWORD>"'

$ aws cognito-idp admin-respond-to-auth-challenge --user-pool-id <YOUR_POOL_ID>  --client-id <YOUR_CLIENT_ID> --challenge-name NEW_PASSWORD_REQUIRED --challenge-responses 'USERNAME=testUser,NEW_PASSWORD=Test1234!,userAttributes.email=test@user.com' --session '<SESSION_VALUE_FROM_PREVIOUS_RESPONSE>'

$ aws cognito-idp admin-initiate-auth --user-pool-id <YOUR_POOL_ID> --client-id <YOUR_CLIENT_ID> --auth-flow ADMIN_NO_SRP_AUTH --auth-parameters 'USERNAME=testUser,PASSWORD="Test1234!"'

$ curl --location '[insert your invoke URL here]/pricepermeter' \
--header 'Content-Type: application/json' \
--header 'Authorization: [insert your IdToken here]' \
--data '{
    "price": 400000,
    "size": 1600,
    "unit": "sqFt",
    "downPayment" : 20
}'
