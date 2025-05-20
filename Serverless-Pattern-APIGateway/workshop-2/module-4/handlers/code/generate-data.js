exports.handler = async (event) => {
  //generate random number to set as sleep duration
  const randomDuration = getRandomArbitrary(250, 1500)
  //sleep function to force sporadic timeouts
  await new Promise(r => setTimeout(r, randomDuration));
  
  //if function executes successfully, return HTTP 200 back to client
  const response = {
     statusCode: 200,
     headers: {
        'Content-Type': 'application/json',
     },
     body: JSON.stringify({
        message: 'Hello from Lambda!'
     }),
  };
console.log('Response:', JSON.stringify(response));
return response;
};
//logic to generate the random value
function getRandomArbitrary(min, max) {
return Math.random() * (max - min) + min;
}