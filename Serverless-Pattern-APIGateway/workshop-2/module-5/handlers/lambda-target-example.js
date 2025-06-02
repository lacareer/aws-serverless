import { v4 as uuidv4 } from 'uuid';
import { Common  }  from "./common.js"

const sessionTable = process.env.SESSION_TABLE
const orderTable = process.env.ORDER_TABLE

export const handler = async (event) => {
   console.log('testing Websocket event:', JSON.stringify(event));
   
   // get request details
   const { orderDetails, status, connectionId } = event.detail;

   try {
      // get session data
      const sessionRecord = await Common.dynamodb_get("connectionId", connectionId, sessionTable);
      
      if (!sessionRecord){
          throw Error(`API integration failed ${connectionId} not found in ${sessionTable}`); 
      }
      
      let currentRecord = {};

      // check if order already exists
      if (sessionRecord.orderId){
         
        console.log("order already exists... updating")
         
        // fetch order record
        const orderRecord = await Common.dynamodb_get("orderId", sessionRecord.orderId, orderTable);

        // update order with new details
        currentRecord = { ...orderRecord, ...orderDetails, status }
        await Common.dynamodb_write(currentRecord, orderTable);     
        
      } else {
        
        const newOrderId = uuidv4();
        console.log("order id: ", newOrderId);

           // set session with order id
        const sessionData = {
            ...sessionRecord,
            orderId : newOrderId
        }
          
        currentRecord = {
            ...orderDetails,
            connectionId:connectionId,
            orderId:newOrderId,
            domainName: sessionRecord.domainName,
            stage: sessionRecord.stage,
            status: status
        }    
         
        // update session table with new order 
        await Common.dynamodb_write(sessionData, sessionTable);
        
        // update order table with new order
        await Common.dynamodb_write(currentRecord, orderTable);
      }

      // send websocket message
      await Common.websocket_send(currentRecord.domainName,currentRecord.stage,connectionId,status);
      return Common.http_ok({message: JSON.stringify(currentRecord)});

  } catch(error) {
      return Common.http_notfound({message: JSON.stringify({
        message: 'invalid order', 
        err: error
    })});
  }
}