import {DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {DynamoDBDocumentClient,ScanCommand,PutCommand} from "@aws-sdk/lib-dynamodb";
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
        switch (event.httpMethod) {
            case "GET":
                body = await dynamo.send(
                    new ScanCommand({TableName: tableName})
                );
                body = body.Items;
                if(isEmpty(body)) {
                    statusCode = 404;
                }
                break;
            case "POST":
                let requestJSON = JSON.parse(event.body);
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
                break;
            default:
                throw new Error(`Unsupported Method: "${event.httpMethod}"`);
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
