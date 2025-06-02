exports.handler = async (event) => {
    console.log('Received event:', JSON.stringify(event));
       const response = {
          statusCode: 200,
          headers: {
             'Content-Type': 'application/json',
          },
          body: JSON.stringify({
             message: 'Hello from Lambda Target!'
          }),
       };
    console.log('Response:', JSON.stringify(response));
    return response;
 };