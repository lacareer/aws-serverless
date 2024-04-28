 <!-- Use Cases -->

# Monte Carlo Simulation
A Monte Carlo simulation is a mathematical technique that allows us to predict different outcomes for various changes to a given system. In financial portfolio analysis the technique can be used to predict likely outcomes for aggregate portfolio across a range of potential conditions such as aggregate rate of return or default rate in various market conditions. The technique is also valuable in scenarios where your business case requires predicting the likely outcome of individual portfolio assets such detailed portfolio analysis or stress tests.

For this fictitious use case we will be working with a portfolio of personal and commercial loans owned by our company. Each loan is represented by a subset of data housed in individual S3 objects. Our company has tasked us with trying to predict which loans will default in the event of a Federal Reserve rate increase.

Loan defaults occur when the borrower fails to repay the loan. Predicting which loans in a portfolio would default in various scenarios helps companies understand their risk and plan for future events.

# What is a Worker?
In this solution we are distributing the data using a Step Functions Activity (https://docs.aws.amazon.com/step-functions/latest/dg/concepts-activities.html). Activities are an AWS Step Functions feature that enables you to have a task in your state machine where the work is performed by a worker that can be hosted on Amazon Elastic Compute Cloud (Amazon EC2), Amazon Elastic Container Service (Amazon ECS), mobile devices—basically anywhere. Think of activity as a Step Functions managed internal queue. You use an activity state to send data to the queue, one or more workers will consume the data from the queue. For this solution we utilize Amazon ECS on Amazon Fargate to run our Activity Workers (Worker).

# Solution Overview
The solution uses AWS Step Functions  to provides end to end orchestration for processing billions of records with your simulation or transformation logic using AWS Step Functions Distributed Map  and Activity  features. At the start of the workflow, Step Functions will scale the number of workers to a (configurable) predefined number. It then reads in the dataset and distributes metadata about the dataset in batches  to the Activity. The workers are polling the Activity looking for data to process. Upon receiving a batch the worker will process the data and report back to Step Functions that the batch has been completed. This cycle continues until all records from the dataset have been processed. Upon completion, Step Functions will scale the workers back to zero.

The workers in this example are containers, running in Amazon Elastic Container Service (ECS)  with an Amazon Fargate  Capacity Provider . Though the workers could potentially run almost anywhere so long as they had access to poll the Step Functions Activity and report SUCCESS/FAILURE back to Step Functions.

# Module Goals
- Learn how Step Functions Distributed Map can use a Step Functions Activity to distribute work to workers almost anywhere
- Learn how Step Functions can manage workers through its built-in Amazon ECS integrations

<!-- Deploy SFW -->
# 1. Deploy the worksflow using dataGenerationStack.yaml using the stack name: "sfn-datagen" in us-east-1 region because the subnets where designed using the avalaibility in that region. Note that the certain resources are exported using this stack name and imported into the "dataProcessingStack.yaml" stack. Changing the names means importing certain resources will fail. In the "dataProcessingStack.yaml" the parameter "DataGenStackName" uses this stack name.

# 2. Deploy dataProcessingStack.yaml in same region with a stackname of "sfn-dataproc".


<!-- Updating the ECS Service - Part 1 -->
The solution uses Amazon ECS to run the workers that handle the actual data processing. In this example we have created an ECS Service that will run a variable number of ECS Tasks, controlled by our Step Functions workflow. The workers run asynchonously from the Distributed Map, which uses an Activity to distribute the dataset. In this step you will configure that ECS Service to use a Task Definition that was predefined in CloudFormation. Lets get started.

1. Navigate to the ECS Console Page 

2. Choose the ECS Cluster named "sfn-fargate-dataproc-xxxxxxxx" (note the similar Cluster named sfn-fargate-datagen-xxxxxxxx, please choose the one ending in dataproc)

3. Choose the ECS Service named "sfn-fargate-dataproc-xxxxxxxx"

4. Click the Update Service button in the top right of the ECS Service page

5. In the field "Family", click the DropDown menu and change the current Task Definition, sfn-fargate-dataproc-placeholder-xxxxxxxx, and choose the Task Definition named sfn-fargate-dataproc-small-xxxxxxxx

6. Leave all other fields default. Scroll to the bottom of the page and click Update.


<!-- Executing the Workflow -->
Let's go ahead and run the Step Function and then we will walk through each step as well as some optimizations for you to consider....

In your AWS Console navigate to the AWS Step Functions Console by using the search bar in the upper left corner of your screen, typing "step functions" and clicking the Step Functions icon.

Open the "sfn-fargate-dataproc-xxxxxxxxxxxx" Step Function by clicking on the Link and then click the "Start Execution" button in the upper right hand corner of the details screen.

Click the "Start execution" button to start the workflow.

3a. You will be prompted for JSON input, leave default and click "Start Execution"

We can then monitor the process of the Step Function State Machine process from the execution status screen. Processing of the 500,000 records in the simulated dataset takes just a few minutes.

<!-- Reviewing the Workflow -->

# Distributed Map
The Processing DMap step is an AWS Step Functions Distributed Map step that reads the S3 Inventory manifest provided by the Parent Map and processes the referenced S3 Inventory  files. For this use case each line of the S3 Inventory file contains metadata referencing an object is S3 containing a single customer loan. The Distributed Map feature creates batches of 400 loan files per our configuration for concurrent distribution to the Step Functions Activity step. Each Distributed Map step supports up to ten thousand concurrent workers. For this example the Runtime Concurrency is set to 1000. As Step Functions adds messages to the Activity, the workers are polling to pull batches for processing. Once complete, the worker reports back to Step Functions to acknowledge the batch has been completed. Step Functions removes that message from the Activity and adds a new batch, it will repeat this process until all batches have been completed.

As Step Functions Distributed Map can scale to massive concurrency very quickly it is advisable to configure back off and retry's within our process to allow downstream systems to scale to meet the processing needs. We utilize Step Functions Distributed Map retry feature to implement graceful back offs without any code. In this example we have configured retry logic for S3 bucket. Each new S3 bucket allocates a single throughput partition of 5,500 reads and 3,500 writes per second which auto-scales based on usage patterns. To allow S3 to auto-scale to meet our workloads write demands the we configure the base retry delay, maximum retires, and back-off within the step function.

# Amazon ECS Workers
The Amazon Elastic Container Service (ECS) Cluster is using a Fargate Spot Capacity Provider  to reduce costs and eliminate maintaining EC2 instances. Fargate provides us with AWS managed compute for scheduling our containers.

The Task Definition in the solution is where we define resources required for our containers to complete. Resources such as network requirements, number of vCPU's, amount of RAM, etc.. In this solution, to avoid building a container, we're simply using an unmodified Amazon Linux 2023 container but specifying a bootstrap sequence. Bootstrapping lets us give the container a series of commands to execute on start. When the container comes up, it will download a pre-generated python script from our S3 bucket and execute it. This python script has the sample logic we want to run against our dataset.

The tasks are managed with an ECS Service. A Service can allow for integration with other services such as Elastic Load Balancers, but in our case we're using it to manage how many tasks are running at any given time. In the "Scale Out Workers" step of the workflow we are using Step Functions built-in integration with ECS to scale out the Service to 50. This way, once Distributed Map begins filling the Activity with batches of work, the containers are already running and immediately begin picking up batches for processing.

# Data Processing
The Run Activity step consists of a single Step Functions Activity which accepts a JSON payload from Distributed Map containing a batch of Loan objects stored in S3. The Run Activity step will continuously add/remove batches of loans by reading the contents of the S3 object. These batches are picked up by our workers and processed. After the worker reports that a batch was successfully processed, Step Functions will remove the batch from the Activity and adds a new one in it's place, maintaining our concurrency limit of batches until all batches are processed. In this example the output files contain batched loans to facilitate more efficient reads for analytics and ML workloads.

Step Functions error handling features removes the need to implement catch and retry logic within the python code (see fargate.py file). If a batch fails processing or a worker fails to report the batch as complete, Step Functions will wait the allotted time and re-add the batch for another worker to pick up and process.

<!-- Updating the ECS Service - Part 2 -->
The update you made in the "Updating the ECS Service - part 1" step used a task definition with a relatively low resource setting, 0.25vcpu and 0.5GB of memory. In this step you will choose a Task Definition that uses the same container as the previous step, but with double the previous resources. Then you will re-run the State Machine and check the differences between the executions. Lets get started.

1. Navigate to the ECS Console Page 

2. Choose the ECS Cluster named "sfn-fargate-dataproc-xxxxxxxx" (note the similar Cluster named sfn-fargate-datagen-xxxxxxxx, please choose the one ending in dataproc)

3. Choose the ECS Service named "sfn-fargate-dataproc-xxxxxxxx"

4. Click the Update Service button in the top right of the ECS Service page

5. In the field "Family", click the DropDown menu and change the current Task Definition, sfn-fargate-dataproc-small-xxxxxxxx, and choose the Task Definition named sfn-fargate-dataproc-large-xxxxxxxx

6. Leave all other fields default. Scroll to the bottom of the page and click Update.

7. Now that you have updated the Service, lets run the State Machine again. If you need instructions please refer back to Execute The State Machine

<!-- Reviewing the Results -->
In the first execution you used a Task Definition that allocated .25 vCPU's and .5GB of RAM to each container. In the second execution you used a Task Definition that allocated .5 vCPU's and 1GB of RAM to each container. Lets check out the results and see how they differ.

1. Go to the Step Functions Console 

2. Choose the State Machine named "sfn-fargate-dataproc-xxxxxxxx"

3. On the State Machine Details page you will see 2 executions, open each in a separate tab. (right-click each link and choose "Open Link in New Tab")

4. On each tab view the details of the execution and find the Duration field to see how long each execution required.

Do they differ? For this simulated dataset, which would be considered small for a Monte Carlo Simulation, the difference is typically less than a minute but overall the increased vCPU/RAM will lead to ~25% time savings. However, to get this ~25% savings you had to double the resources for each container, effectively doubling your Fargate costs. If time is your most critical factor, this may be worth it. If cost is your most critical factor, perhaps not. The variation for both cost and time are minimal with a dataset this small, however if you extrapolate this to a dataset consisting of millions or even billions of objects, both time and cost variations are considerable. You will want to experiment with your actual workloads on what settings work best.