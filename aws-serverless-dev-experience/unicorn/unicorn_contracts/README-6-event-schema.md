<!-- Share your schema -->
A schema defines the structure of events that are sent to EventBridge. In order to share the ContractStatusChanged event with other services in our architecture, 
you will create a schema and share it via schema registry. Schema registries collect and organize schemas so that your schemas are in logical groups, and for 
the Contract Service this logical grouping is the service namespace, unicorn.contracts.

You can create schemas in either OpenAPI 3 and JSONSchema Draft4 formats. You have the option to create these manually or through an EventBridge feature called 
Schema Discovery, which infers the schema from events on an event bus.

<!-- EventBridge schema discovery -->
1. Open the Amazon EventBridge console

2. Under Buses in the left hand navigation select Event buses.

3. Under Custom event bus select the UnicornContractsBus-local and click Start discovery
   This will start schema discovery in the background.
   Send additional traffic to the application by using one of the options provided in testing section section of Creating contracts page. 
   Once few requests have been sent, you can click Delete discoverer button.
4. Navigate to the Schemas under Schema Registry.

5. Open the Discovered Schema Registry. You should see a discovered schema in there called unicorn.contracts@ContractStatusChanged.   
   It can take a few minutes for the discovered schema to show up. Wait 2-5 minutes and refresh the page.

6. Click on unicorn.contracts@ContractStatusChanged and you will see the below as was my case.
   Add this content to the "content" node of ContractStatusChangedEventSchema in event-schema.yaml in unicorn_contracts/integration directory

{
  "openapi": "3.0.0",
  "info": {
    "version": "1.0.0",
    "title": "ContractStatusChanged"
  },
  "paths": {},
  "components": {
    "schemas": {
      "AWSEvent": {
        "type": "object",
        "required": ["detail-type", "resources", "detail", "id", "source", "time", "region", "version", "account"],
        "x-amazon-events-detail-type": "ContractStatusChanged",
        "x-amazon-events-source": "unicorn.contracts",
        "properties": {
          "detail": {
            "$ref": "#/components/schemas/ContractStatusChanged"
          },
          "account": {
            "type": "string"
          },
          "detail-type": {
            "type": "string"
          },
          "id": {
            "type": "string"
          },
          "region": {
            "type": "string"
          },
          "resources": {
            "type": "array",
            "items": {
              "type": "object"
            }
          },
          "source": {
            "type": "string"
          },
          "time": {
            "type": "string",
            "format": "date-time"
          },
          "version": {
            "type": "string"
          }
        }
      },
      "ContractStatusChanged": {
        "type": "object",
        "required": ["contract_last_modified_on", "contract_id", "contract_status", "property_id"],
        "properties": {
          "contract_id": {
            "type": "string"
          },
          "contract_last_modified_on": {
            "type": "string"
          },
          "contract_status": {
            "type": "string"
          },
          "property_id": {
            "type": "string"
          }
        }
      }
    }
  }
}