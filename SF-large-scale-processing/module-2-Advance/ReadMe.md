<!-- Optimization -->

# Introduction
In this module, we use the same example workflow from earlier sub module Building a distributed map workflow. 
But we pre-created the workflow, using the template, to make it easier for you

# What you do in the module
- Using the precreated Step Functions workflow, you will tune some attributes/fields of distributed map and understand the performance and cost impact of the change.

# What you accomplish in the module
- what workflow type best suits to be run as child workflow
- how to balance the cost and speed by changing batching and concurrency

<!-- Deploy SF -->
Deploy the SF using the template.yaml


<!-- Choosing the Workflow Type -->

# Workflow types
Step Functions offers two types of workflows - Standard and Express. Standard workflows are ideal for long running workflow; it can run for 365 day whereas express workflows can run only for 5 minutes. Another important distinction is how pricing works. Standard workflows are priced by state transition while express workflows are priced by number of request and the duration. To learn more about the difference, click here .

When you use distributed map, Step Functions spins up child workflows to run the states inside the distribtued map. The number of child workflows to spin up is dependant on the number of objects or records to process, batch size and concurrency. You can define the child workflow to run as either standard or express based on your use case.

In the following sections, you will learn how to change workflow type of distributed map child workflows, try out a technique to find if express workflow suits your use case, and the cost impact of running standard vs express.

Check the child workflow ExecutionType. It is set as STANDARD.

    "ItemProcessor": {
    "ProcessorConfig": {
        "Mode": "DISTRIBUTED",
        "ExecutionType": "STANDARD"
    },

Also, explore the batch setting. Each child workflow receives a batch of 100 objects.

      "ItemBatcher": {
        "MaxItemsPerBatch": 100
      },

# Execute SF with below input
Open the S3 console  then copy the full name of the bucket containing MultiFileDataBucket in its name.

Return to the Start execution popup and enter the following json as input, replacing the bucket logical name, not ARN, with your bucket name from S3:

    {
    "bucket": "bucket-logical_name",
    "prefix":"csv/by_station"
    }

# Identify if workflow can be Express
Child workflow can be run either STANDARD or EXPRESS. Express workflows are generally less expensive and run faster than Standard workflows.

Sometimes, you may not be sure if your workflow runs within 5 minutes. In this section, You are going to use a feature of distributed map that allows you to test your data with small number of items. This technique is helpful in couple of ways

-To determine the duration of the child workflow

-To gain confidence that the child workflow logic will run fine when running with full data set.

Start making the changes

-Toggle Definition button to edit the configuration.

-Expand Additional configuration and select Limit number of items.

-Type 1 in Max Items textbox.

- Save and execute with default input.

- Select Map Run from the execution page.

- Observe the duration for single item. It is around 3 seconds.

Continue:

Repeat the above steps with 100 items.

Explore the Map Run page to find the duration for 100 items. It is less than 30 seconds (mine was around 6 seconds).

Now you know it takes 3 seconds to run 1 item and 26 seconds for 100 items, you can even run all the 1000 items in a single child workflow with 1 concurrency. But, you don't utilize any parallelism to speed up the process.

*** This simple test is really handy in finding the right batch size and choosing the workflow type without running the entire dataset!!!

# Change workflow to express
- Return to workflow studio.

- Change the workflow type to EXPRESS.

- Remove additional configuration to limit number of items. Yes! we are running with all the items.

- Save the workflow and run.

- Explore the Map Run page and note down the duration.

- Repeat the above steps with STANDARD.

What did you observe? Yes! Express workflows are faster compared to Standard, 2 and 5 seconds for 1 and 100 items respectively.

<!-- Review Cost impact -->
Consider you are processing 500K objects and set the batch size to 500.

500k objects / 500 objects per workflow = 1000 child workflows

Distributed map runs a total of 1000 child workflows to process 500K objects.

# Standard child workflow execution cost
In the example we used in this module, we have one Lambda function inside the child workflow. so, the number of state transition per child workflow is 2:- one transition for starting the child workflow and one for Lambda function.

Total cost = (number of transitions per execution x number of executions) x $0.000025

Total cost = (2 * 1000) x $0.000025 = $0.05

Let's assume you have 5 steps inside your child workflow, the number of state transitions per child workflow is 6.

Total cost = (number of transitions per execution x number of executions) x $0.000025

Total cost = (6 * 1000) x $0.000025 = $0.15

Let's take another scenario. You have 2 steps inside your child workflow, the number of state transitions per child workflow is 3. Let's assume you can not utilize batching, the number of child workflows to complete the work = 500K

Total cost = (number of transitions per execution x number of executions) x $0.000025

Total cost = (3 * 500K) x $0.000025 = $37.4

# Express child workflow execution cost
With Express worklfows, you pay for the number of requests for your workflow and the duration. With scenario outlined earlier under Review cost impact, we need addional dimension of how long workflow runs to calculate the express workflow cost. Let's assume express child workflow runs for an average of 100sec to process 500 objects using 64-MB memory.

Duration cost = (Avg billed duration ms / 100) * 0.0000001042

Duration cost = (100,000 MS /100) * $ 0.0000001042 = $0.0001042

Express request cost = $0.000001 per request ($1.00 per 1M requests)

workflow cost = (Express request cost + Duration cost) x Number of Requests

workflow cost = ($0.000001 + $0.0001042) x 1000 = $0.10

Express child workflow introduces 1 state transition per child workflow regardless of how many states you have inside the workflow. This is to start each child execution.

Transition cost = (1 * 1000) x $0.000025 = $0.025

Total cost = $0.10 + $0.025 = $0.125

If we repeat the calculation for an express workflow that runs for 30 seconds, the total cost = $0.057

If we repeat the calculation for an express workflow that runs for 1 second to process 1 object because you can not utilize batching, the total cost = $13.42


# What did you observe?
Express workflows are cheaper when the duration is lesser. They are also cost effective if there are more steps in the child workflow or your distributed map can not make use of batching. Remember, Standard workflows are priced by state transitions meaning when number of steps and number of child workflow executions increase, cost increases.

You can look at from the below chart how express workflow duration affect the cost.

<!-- Balancing Cost and Performance Using Concurrency and Batching -->
Higher parallelism generally means you can run the workflows faster. Higher parallelism with no or sub optimal batching results in higher cost for couple of reasons;

- There is more state transitions for standard workflows and request cost for express workflows

- Services you use inside the child workflow might have cost for requests.

Higher parallelism also causes scaling bottlenecks for downstream services inside the child workflow. You can use distributed map concurrency control to control the number of parallel worflow. If you have multiple workflows and need to manage downstream scaling then you can use techniques such as queueing  and activities .

In the following sections, you will run a few experiments with batch size and understand the performance and cost impact of batch size between standard and express workflows

NB: From the SF definition, each child workflow receives a batch of 100 objects. The concurrency or the parallelism of workflow is set as 1000.

# Run the workflow
- Execute the workflow with default input.

- Select Map Run from the Execution page

- Examine the map run results.

- Note down the duration. You can see there is 10 child workflow executions. As there are only 1000 objects, with the batch setting of 100, only 10 parallel workflows are triggered.

- Close all the tabs

# Change batch setting
- Navigate to Step Functions Console , select State machines from the right menu.

- Select the workflow that starts with OptimizationStateMachine.

- Choose edit to edit the workflow in workflow studio.

- Highlight the Distributed map high precipitation step and view the configurations

- Modify the MaxItemsPerBatch to 1

- Save and Execute the workflow with default input

- Explore the map run results. You can see 1000 child workflow executions.

- All the child workflows are completed in little under 25 seconds

- Repeat the exercise with differnt batch settings. What did you observe? 

*** Yes, The total duration increases when you increase the batch size. So, you must find the sweet spot between the batch number of your MAP and the speed of each child execution need.

<!-- Review the cost impact -->
You are now going to review the impact of cost with different batch sizes. Assume your workflow is processing 50M S3 objects. Now, let's look at the cost of distributed map if you define the execution type as standard against express.

# Standard child workflow
Assume you need to process 50M objects. You have 2 steps inside your child workflow. Each child workflow processes 100 objects in a batch. The number of state transition per child workflow is 3. Total number of child workflows to process 50M objects is 500,000.

Total cost = (number of transitions per execution x number of executions) x $0.000025

Total number of child workflows to process 50M objects = 500,000

Total cost = (3 * 500000) x $0.000025 = $37.5

# Express vs Standard vs Batch size Table

Batchsize	child workflows	    Child workflow Duration(ms)	    Standard cost	    Express cost

100	        500,000	            28,000	                        $37.5	            $27.59

200	        250,000	            32,000	                        $18.75	            $14.84

400	        125,000	            62,000	                        $9.38	            $11.33

500	        100,000	            74,000	                        $7.5	            $10.31

600	        83,333	            90,000	                        $6.25	            $9.98

800	        62,500	            120,000	                        $4.69	            $9.44

1000	    50,000	            150,000	                        $3.75	            $9.12


# Important
The degree of parallelism is determined by the Concurrency setting in Distributed Map, which determines the maximum number of parallel child workflows you want to execute at once. A key consideration here is the service quotas of the AWS services called in your child workflow. For example AWS Lambda in most large regions has a default concurrency quota of 1500 and a default burst limit of 3000, other services such as AWS Rekognition or AWS Textract have much lower default quotas.

The other thing to keep in mind is any performance limitations of other systems that your child workflow interacts with. An example here would be an on-prem relational database that Lambda within a child workflow connects to. This database might have a limit to the number of connections it can support, so you would need to limit your concurrency accordingly. Once you identify all of the AWS Service quotas and any additional concurrency limitation you'll want to test various combinations of batch size and concurrency to find the best performance within your concurrency constraints

