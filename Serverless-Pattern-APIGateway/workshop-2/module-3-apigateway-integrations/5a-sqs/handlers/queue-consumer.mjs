import {DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {DynamoDBDocumentClient,PutCommand} from "@aws-sdk/lib-dynamodb";
// Get the DynamoDB table and Region name from environment variables
const tableName = process.env.SAMPLE_TABLE;
const regionName = process.env.REGION;
const dynamo = DynamoDBDocumentClient.from(new DynamoDBClient({region: regionName}));

export const handler = async (event, context) => {

    console.log('Received event:', JSON.stringify(event));
    
    let response_payload = {};
    let body;
    let statusCode = 200;
    const headers = {
        "Content-Type": "application/json",
    };
    
    try {
        for (const record of event.Records) {
            console.log(`Received message ${record.messageId} from SQS:`);
            console.log(record.body);    
            let requestJSON = JSON.parse(record.body);
            await dynamo.send(
            new PutCommand({
                TableName: tableName,
                Item: {
                    id: requestJSON.id,
                    price: requestJSON.price,
                    name: requestJSON.name,
                },
            })
            );
            body = `Put item ${requestJSON.id}`;
        }
    } catch (err) {
        statusCode = 500;
        body = err.message;
    } finally {
        body = JSON.stringify(body);
    }
    
    response_payload = {
        statusCode,
        headers,
        body
    };
    
    console.log('Response:', JSON.stringify(response_payload));
    return response_payload;
};

function isEmpty(obj) {
   return Object.keys(obj).length === 0;
}