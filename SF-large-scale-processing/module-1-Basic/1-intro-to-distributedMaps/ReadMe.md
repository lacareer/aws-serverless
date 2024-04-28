# Introduction to Distributed Map
Welcome to the introduction to distributed map module!

<!-- What is Distributed Map? -->
Distibuted map is a map state that executes the same processing steps for multiple entries in a dataset at 10,000 concurrency. This means you can run a large scale parallel data processing workload without worrying about how to parallelize the executions, workers, and data. Distributed map can iterate over millions of objects such as logs, images or records inside .csv or json files stored in Amazon S3. It can launch upto 10,000 parallel child workflows to process the data. You can include any combination of AWS services like AWS Lambda functions, Amazon ECS tasks, or AWS SDK calls in the child workflow.

Distributed map is the new addition to the two types of maps available in Step Functions. Primary difference between the inline map and distributed map are -

1. Distributed map has higher concurrency compared to inline map's 40 concurrency
2. Distributed map can directly iterate on the data from Amazon S3.
3. Each sub workflow of Distributed map runs as a separate child workflow that avoids 25K execution history limit of Step Functions.

<!-- What you will accomplish -->
- Navigate to Workflow Studio
- Review Distributed Map Amazon States Language (ASL) definition
- Run a Hello distributed map workflow

<!-- deploy template.yaml -->

Deploy the template.yaml using cloudformation

<!-- Reviewing the Workflow -->

# You define it as DISTRIBUTED to tell Step Functions to run the map state in distributed mode.
    Map":{
            "Type": "Map",
            "ItemProcessor": {
                "ProcessorConfig": {
                "Mode": "DISTRIBUTED",
                "ExecutionType": "EXPRESS"
            .....
            .....
            .....
            }
        }

# ItemReader in the definition
This is how you tell distributed map to process a csv or JSON file. Notice that the reader uses the s3.getObject ( because we are reading jsut a singlr s3 object/file. To read multiple files use: arn:aws:states:::s3:listObjectsV2 ) API to read the object. Yes! It reads the content of the csv file and distributes the data to child workflows in batches, running at a concurrency of 10,000!

                "MaxConcurrency": 10000,
                "ItemReader": {
                  "Resource": "arn:aws:states:::s3:getObject",
                  "ReaderConfig": {
                    "InputType": "CSV",
                    "CSVHeaderLocation": "FIRST_ROW"
                  },
                  "Parameters": {
                    "Bucket": "${Databucket}",
                    "Key.$": "$.key"
                  }
                },

# Batching. 
Do you see MaxItemsPerBatch set as 1000

    "ItemBatcher": {
        "MaxItemsPerBatch": 1000
    },

You can not only run 10,000 (10K) workflows, you can also batch the data to each workflow which means, in a single iteration, you can process 10K * 1K = 10M records from the csv file! And you can write the output of the distributed map or the child workflow execution results to an S3 location in an aggregated fashion

# Fault tolerance
You don't want to run 100M records when half of them are bad data. It is a waste of time and money to process those records. By default, the failure toleration is set to 0. Any single child workflow failure will result in the failure of the workflow.

    ....
    ....
    "ToleratedFailurePercentage": 1,
        "End": true
        }
# States
Next, you can see what is inside of the distributed map. In this introduction module, we did not use any compute services like Lambda to process the records. You can see a pass state filtering highly rated reviews. Pass state is really useful to transform and filter input. It is simple and easy to demonstrate the 10K concurrency, without worrying about the scale of a downstream service. However, in a real world scenario, you include any combination of AWS services like AWS Lambda functions, Amazon ECS tasks, or AWS SDK calls in the child workflow.
The states inside the distributed map are run as separate child workflows. The number of child workflows is dependant on the concurrency setting and the volume of the records to process. For example, you might set the concurrency to 1000 and batch size to 100, but if the total number of records in the file is just 20K, Step Functions only needs 200 child workflows (20,000 / 100 = 200). On the other hand, if the file has 200K records, Step Functions will spin up 1000 child workflows to reach the max concurrency and as child workflows complete, Step Functions will spin up child workflows until all 2000 (200,000 /100 = 2000) child workflows are completed.”


<!-- Prepare data set -->
You are going to download the data file to the local computer and upload to S3.

Run the following command in your local machine.

# Linux
    curl https://raw.githubusercontent.com/MengtingWan/marketBias/master/data/df_electronics.csv --output df_electronics.csv

# Windows
    Invoke-WebRequest https://raw.githubusercontent.com/MengtingWan/marketBias/master/data/df_electronics.csv -OutFile df_electronics.csv

# OR clone the repo in  a seperate directory and copy the df_electroninc.csv into the module-1-Basic root directory
    git clone https://github.com/MengtingWan/marketBias.git

<!-- Run the workflow -->
- Open the Step Functions Console , select and open the state machine containing HelloDmapStateMachine in its name.

- Choose Start execution in the top right corner.

- In the popup, enter the following input:

    {
        "key":"df_electronics.csv",
        "output":"results"
    }

    You are providing the name of the file and S3 prefix where you want the results of the distributed map to be stored.

- Click Start execution.

    In a few seconds, you will see the execution start to run. It takes a few minutes to complete the processing.

