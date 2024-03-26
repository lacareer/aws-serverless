<!-- What you do in the module -->
In this module, you are going to build a distributed map workflow that processes thousands of weather data files from NOAA climatology data . The wokflow is going to find the highest precipitation for each weather station and store the results in DynamoDB table. Each weather station is an individual S3 object containing various weather data and there are about 1,000 stations.

<!-- Services used -->
- AWS Step Functions  - Serverless visual workflow service
- AWS Lambda  - Compute service; functions in serverless runtimes
- Amazon DynamoDB  is a fully managed, serverless, key-value NoSQL database designed to run high-performance applications. DynamoDB offers built-in security, continuous backups, automated multi-Region replication, in-memory caching, and data export tools.

<!-- Pre-created resources -->
To quickly build the workflow, we have created a few resources ahead of time using template.yaml.

Lambda function to find the highest precipitation for the station
One S3 bucket for the dataset and another S3 bucket for storing distributed map results
Sample dataset of 1,000 S3 objects from NOAA climatology data
Amazon DynamoDB table to store the precipitaion data

<!-- What you will accomplish -->
Build a Step Functions workflow with distributed map.
Modify the workflow to pass the S3 bucket information to Lambda function.
Run the workflow and verify the results.
In the process, you will learn how to process millions of S3 objects in parallel in a distributed fashion.

<!-- S3 Data can be view with below locally-->

# NB: The data url is used in the template (specifically in the lambda function) 

# get data
    curl https://ws-assets-prod-iad-r-pdx-f3b3f9f1a7d6a3d0.s3.us-west-2.amazonaws.com/2a22e604-2f2e-4d7b-85a8-33b38c999234/dataset/noah.zip --output noah.zip

# unzip the file the folder "noah"
    unzip noah.zip -d ~/chuks-project-directory/noah

<!-- deploy template -->
Deploy template.yaml using cloudformation

<!-- Deploy SF by uncommenting the sf code or build  it by follwing the steps in "Building the Workflow" section-->
Deploy SF by uncommenting the sf code in template.yaml.The template is very similar to the template in module-1-Basic/intro-to-distributedMaps/. 

# Note this new item which is a way to define global variables for all child workflows
So you can build custom variable this way

    "BatchInput": {
        "Bucket.$": "$.bucket"
    }
The above variable is accessed in the lambda HighPrecipitationFunction like below:
input_bucket_name = event["BatchInput"]["Bucket"]

<!-- Building the Workflow -->

# First, you will configure where to read the dataset from. You will pass the location of the precreated dataset in S3 as input.

Select Amazon S3 as the Item source.

Select S3 object list in S3 item source dropdown.

Select Get bucket and prefix at runtime from state input in S3 bucket dropdown.

For Bucket Name, enter $.bucket. For Prefix, enter $.prefix.

Enable batching and set the Max items per batch to 100.

Leave everything else as default and move on to adding the child workflow components.

Enter Lambda in the search textbox at the top left.

Drag and drop the Lambda - Invoke action to the center.

Click on the Function name dropdown and select function with HighPrecipitation in its name.

# Notice that the ItemReader object uses listobjectV2. In sub-module 1, you saw GetObject in ItemReader. The reason is that you processed a single S3 object in sub-module 1 (df_electronics.csv file) and you are processing multiple S3 objects here in this sub-module. You can nest both patterns to read multiple csv/json files in a highly parallel fashion
    "ItemReader": {
    "Resource": "arn:aws:states:::s3:listObjectsV2",
    "Parameters": {
        "Bucket.$": "$.bucket",
        "Prefix.$": "$.prefix"
        }
    },
Select the Config tab next to the state machine name at the top of the page and change the State machine name to FindHighPrecipitationWorkflow.

Choose an existing IAM role with the name StatesHighPrecipitation

Choose Create button at the top.

Run the workflow by choosing Start execution button.

Wait! You need the bucket and prefix as input to the workflow.

Open the S3 console  then copy the full name of the bucket containing MultiFileDataBucket in its name.

Return to the Start execution popup and enter the following json as input, replacing the bucket logical name, not ARN, with your bucket name from S3:
    {
    "bucket": "bucket-logical_name",
    "prefix":"csv/by_station"
    }

Choose Start Execution.

# Oops!!! The execution failed. Why???
By default, distributed map fails even when a single child fails. Lets explore what actually caused the child workflow to fail.

Click Map Run to check the child workflow executions.

Select a child workflow executions to see the error.

It looks like Lambda is expecting event[BatchInput][Bucket] and it is not found. Explore the input to the Lambda function by selecting Execution input and output at the top.

The input only contains the S3 key. It is missing the bucket name.

Alright! You are going back to Workflow Studio to pass the bucket name as input to the Lambda function.

Close this tab and return to the previous tab, or you can browse to the workflow by following the breadcrumb at the top.

Choose Edit button.

Select the map state in the workflow design.

Modify the Batch input under Item batching to include the bucket name. Batch Input enables you to send additional input to the child workflow steps as global data. For ex. Bucket name is a global data and does not have to be in individual line item


<!-- Summary -->
In this module, You built a data processing workflow with distributed map, configuring Step Functions to distribute the S3 objects across multiple child workflows to process them in parallel.

# Important
When processing large numbers of objects in S3 with Distributed Map, you have a couple of different options for listing those objects: S3 listObjectsV2 and S3 Inventory List . With S3 listObjectsV2, Step Functions is making S3 listObjectsV2 API calls on your behalf to retrieve all of the items needed to run the Distributed Map. Each call to listObjectsV2 can only return a maximum of 1000 S3 objects. This means that if you have 2,000,000 objects to process, Step Functions has to make at least 2000 API calls. This API is fast and it won't take too long, but if you have an S3 Inventory file that has all the objects listed in it that you need to process, you can use that as the input.

Using an S3 Inventory file as the input for a Distributed Map when processing large numbers of files is faster than S3 listObjectsV2. This is because, for S3 Inventory ItemReaders, there is a single S3 getObject call to get the manifest file and then one call for each Inventory file. If you know that your Distributed Map is going to run on a set schedule you can schedule the S3 Inventory to be created ahead of time.

