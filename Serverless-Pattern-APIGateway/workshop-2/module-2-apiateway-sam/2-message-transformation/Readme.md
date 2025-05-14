<!-- Message Transformation -->
In API Gateway, a mapping template is used to transform data from one format to another. JSON path expressions can be used to map and transform the integration payload to any desired format. In addition, a model (schema) can be created to define the structure of a message payload. Having a model also enables you to generate an SDK that can be used by the client application to send properly formatted messages.
Read more on specification here: https://spec.openapis.org/oas/v3.1.0#components-object-example

Move into the first-api folder: 

    cd first-api

Add all the chnages in the lab to the respective files and run the command below. Or run the command for each new additions:

    sam build && sam deploy


