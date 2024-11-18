<!-- Testing web service -->
In this section, we will be testing out a few scenarios:

- search for available property listings as a customer

- send property listing for approval as an agent

<!-- Run query against web service -->
First query we will run is to list the properties which are approved and ready to be viewed by customers.

Run the query to search for all APPROVED listings as per below:

    API_URL="$(aws cloudformation describe-stacks --stack-name uni-prop-local-web --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' --output text)"
    
    curl -s ${API_URL}search/usa/anytown | jq

You will see that the search results have not returned any results. This is because none of the listings in our data is currently in APPROVED status.

<!-- Request property approval -->
Pick one of the property listings in the table and use it with the request_approval API call.

For example:

        API_URL="$(aws cloudformation describe-stacks --stack-name uni-prop-local-web --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' --output text)"

        curl -X POST ${API_URL}request_approval \
            -H 'Content-Type: application/json' \
            -d '{"property_id":"usa/anytown/main-street/111"}' \
        | jq

You should see following message in response to your API call:

        { "message": "OK" }        

This indicates that the Lambda function was able to send "Publication approval requested" event to EventBridge.   

<!-- Publication approval completed -->

# If you have not completed the "Developing Unicorn Properties" section of this workshop, then the approval workflow will not be implemented. 
# This means that this event will not be read and no action will be taken just now.

We can simulate the "publication evaluation completed" event sent by property service by sending following mock event to EventBridge:

aws events put-events --entries file://./tests/events/eventbridge/put_event_publication_evaluation_completed.json

If the event was sent correctly, you should see response similar to below:

{
    "FailedEntryCount": 0,
    "Entries": [
        {
            "EventId": "35835b32-3b67-4d59-dc47-008e717af412"
        }
    ]
}

Look over the DynamoDB table entries again. Can you see the status change of the property you've upated above?

<!-- Run search query again -->
Now that the property listing is approved, run the same search query again:

    API_URL="$(aws cloudformation describe-stacks --stack-name uni-prop-local-web --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' --output text)"
    
    curl -s ${API_URL}search/usa/anytown | jq

You should see an output similar to below:

[
    {
        "city":"Anytown",
        "currency":"SPL",
        "number":"111",
        "listprice":"200",
        "contract":"sale",
        "country":"USA",
        "street":"Main Street"
    }
]

As you can see, the API has returned JSON output with property listing information.