import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, GetCommand, PutCommand} from "@aws-sdk/lib-dynamodb";
import { ApiGatewayManagementApiClient, PostToConnectionCommand } from "@aws-sdk/client-apigatewaymanagementapi";

const documentClient = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(documentClient);

// Get item from Dynamo db table
async function dynamodb_get(hash, value, TableName) {
    const command = new GetCommand({
        TableName,
        Key: {
            [hash] : value
        },
    });

    const response = await docClient.send(command);
    if (!response || !response.Item) {
        throw Error(`There was an error fetching the data for ID of ${ID} from ${TableName}`);
    }
    console.log(response);
    return response.Item;
}

// Write item to Dynamo db table 
async function dynamodb_write(item, TableName) {

    const command = new PutCommand({
        TableName,
        Item: item
    });

    await docClient.send(command);
}

// Return 200 status code 
function http_ok(data = {}) {
    return {
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Origin': '*',
        },
        statusCode: 200,
        body: JSON.stringify(data),
    };
}

// Return 404 status code 
function http_notfound(data = {}) {
    return {
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Origin': '*',
        },
        statusCode: 404,
        body: JSON.stringify(data),
    };
}

// Sending message to a websocket connection
async function websocket_send (domainName, stage, connectionId, status) {
    
    const callback = `https://${domainName}/${stage}`;
    
    console.log(`sending connection preparing sending message ${status} to ${callback}`);
    
    const client = new ApiGatewayManagementApiClient({ 
       endpoint: callback,
    });
    
    const message = {
       name : "STATUS_CHANGED_EVENT",
       status: status     
    }
 
    const messageEvent = {
         type: "CHANGED_EVENT",
         message : JSON.stringify(message)
    }
      
    const requestParams = {
       ConnectionId: connectionId,
       Data: JSON.stringify(messageEvent)
    };
 
    const command =  new PostToConnectionCommand(requestParams)
 
    console.log(`sending to ${connectionId} ...`);
    await client.send(command);
    console.log(`${status} sent`);
 };
 
export const Common = {
   http_ok,
   http_notfound,
   dynamodb_get,
   dynamodb_write,
   websocket_send
};