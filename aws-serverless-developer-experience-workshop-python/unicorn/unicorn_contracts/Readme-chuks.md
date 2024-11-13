<!-- SEE ARCHITECTURE DIAGRAM IN CURRENT DIRECTORY -->
As an agent, you issue asynchronous commands to create or update Contract information to the Contact API. The API passes the request to SQS, which is processed by the Contracts function. The DynamoDB stream in the Contracts table captures changes as the Contract function creates or updates contracts. These records trigger an EventBridge Pipes execution which transforms the DynamoDB record and sends it to EventBridge. This event represents the ContractStatusChanged event. These events are consumed by Unicorn Properties, so it can track changes to contracts, without needing to take a direct dependency on Unicorn Contracts and its database.


<!-- In this section you will -->
- Complete the implementation of the Contract service.
- Create the EventBridge Pipe that converts the DynamoDB stream record into a EventBridge event.
- Implement Powertools for AWS to provide you best practice approaches to observability, including tracing and structured logging.
- Create a EventBridge schema for the ContractStatusChanged event and make available in the Unicorn.Contracts Schema Registry so it can be shared across services.
- Deploy the service using a AWS SAM Pipelines.
- Right size your functions using AWS Lambda Power Tuning tool (optional).

<!-- AWS SAM features -->
While developing this service, we will be introducing you to AWS SAM commands like sam init, sam build, sam deploy, sam sync, sam logs, sam pipeline and developer tools Serverless Rules.

Let's start building!