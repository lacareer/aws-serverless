# Herein are the instructions for this module 

# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-reference.html

<!-- Module goals -->
Use the SAM CLI to initialize a project
Understand the structure of a SAM application
Review the code for the initial skeleton of the application

<!-- instructions  -->
1. sam init

<!--  -->
Which template source would you like to use?
        1 - AWS Quick Start Templates
        2 - Custom Template Location
Choice: 1

<!--  -->
Choose an AWS Quick Start application template
        1 - Hello World Example
        2 - Multi-step workflow
        3 - Serverless API
        4 - Scheduled task
        5 - Standalone function
        6 - Data processing
        7 - Infrastructure event management
        8 - Serverless Connector Hello World Example
        9 - Multi-step workflow with Connectors
        10 - Lambda EFS example
        11 - Machine Learning
Template: 1

<!--  -->
Use the most popular runtime and package type? (Python and zip) [y/N]: n

<!--  -->
(Next, select your preferred runtime and version. Make sure to select the correct version as shown below.)
(In my case, Python3.10, i.e option 20)

    1 - aot.dotnet7 (provided.al2)
    2 - dotnet6
    3 - dotnet5.0
    4 - dotnetcore3.1
    5 - go1.x
    6 - go (provided.al2)
    7 - graalvm.java11 (provided.al2)
    8 - graalvm.java17 (provided.al2)
    9 - java17
    10 - java11
    11 - java8.al2
    12 - java8
    13 - nodejs18.x
    14 - nodejs16.x
    15 - nodejs14.x
    16 - nodejs12.x
    17 - python3.9
    18 - python3.8
    19 - python3.7
    20 - python3.10
    21 - ruby2.7
    22 - rust (provided.al2)

<!--  -->
(You can enable x-ray tracing, cloudwatch, and change the app name to something other than sam-app if preferred)

What package type would you like to use?
        1 - Zip
        2 - Image
Package type: 1

Based on your selections, the only dependency manager available is pip.
We will proceed copying the template using pip.

Would you like to enable X-Ray tracing on the function(s) in your application?  [y/N]: n

Would you like to enable monitoring using CloudWatch Application Insights?
For more info, please view https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-application-insights.html [y/N]: n

Project name [sam-app]:

# sam init options to pass to CLI


--app-template TEXT
        The identifier of the managed application template that you want to use. If you're not sure, call sam init without options for an interactive workflow.

        This parameter is required if --no-interactive is specified and --location is not provided.

        This parameter is available only in AWS SAM CLI version 0.30.0 and later. Specifying this parameter with an earlier version results in an error.

--application-insights | --no-application-insights
        Activate Amazon CloudWatch Application Insights monitoring for your application. To learn more, see Monitor your serverless applications with CloudWatch Application Insights.

        The default option is --no-application-insights.

--architecture, -a [ x86_64 | arm64 ]
        The instruction set architecture for your application's Lambda functions. Specify one of x86_64 or arm64.

--base-image [ amazon/nodejs20.x-base | amazon/nodejs18.x-base | amazon/nodejs16.x-base | amazon/nodejs14.x-base | amazon/nodejs12.x-base | amazon/python3.12-base | amazon/python3.11-base | amazon/python3.10-base | amazon/python3.9-base | amazon/python3.8-base | amazon/python3.7-base | amazon/ruby3.2-base | amazon/ruby2.7-base | amazon/go1.x-base | amazon/java21-base | amazon/java17-base | amazon/java11-base | amazon/java8.al2-base | amazon/java8-base | amazon/dotnet6-base | amazon/dotnet5.0-base | amazon/dotnetcore3.1-base ]

        The base image of your application. This option applies only when the package type is Image.

        This parameter is required if --no-interactive is specified, --package-type is specified as Image, and --location is not specified.

--config-env TEXT
        The environment name specifying the default parameter values in the configuration file to use. The default value is "default". For more information about configuration files, see AWS SAM CLI configuration file.

--config-file PATH
        The path and file name of the configuration file containing default parameter values to use. The default value is "samconfig.toml" in the root of the project directory. For more information about configuration files, see AWS SAM CLI configuration file.

--debug
        Turns on debug logging to print debug messages that the AWS SAM CLI generates, and to display timestamps.

--dependency-manager, -d [ gradle | mod | maven | bundler | npm | cli-package | pip ]
        The dependency manager of your Lambda runtime.

--extra-content
        Override any custom parameters in the template's cookiecutter.json configuration, for example, {"customParam1": "customValue1", "customParam2":"customValue2"}.

--help, -h
        Shows this message and exits.

--location, -l TEXT
        The template or application location (Git, Mercurial, HTTP/HTTPS, .zip file, path).

        This parameter is required if --no-interactive is specified and --runtime, --name, and --app-template are not provided.

        For Git repositories, you must use the location of the root of the repository.

        For local paths, the template must be in either .zip file or Cookiecutter format.

--name, -n TEXT
        The name of your project to be generated as a directory.

        This parameter is required if --no-interactive is specified and --location is not provided.

--no-input
        Disables Cookiecutter prompting and accepts the vcfdefault values that are defined in the template configuration.

--no-interactive
        Disable interactive prompting for init parameters, and fail if any required values are missing.

--output-dir, -o PATH
        The location where the initialized application is output.

--package-type [ Zip | Image ]
        The package type of the example application. Zip creates a .zip file archive, and Image creates a container image.

--runtime, -r [ ruby2.7 | ruby3.2 | java8 | java8.al2 | java21 | java17 | java11 | nodejs12.x | nodejs14.x | nodejs16.x | nodejs18.x | nodejs20.x | dotnet6 | dotnet5.0 | dotnetcore3.1 | python3.12 | python3.11 | python3.10 | python3.9 | python3.8 | python3.7 | go1.x ]

        The Lambda runtime of your application. This option applies only when the package type is Zip.

        This parameter is required if --no-interactive is specified, --package-type is specified as Zip, and --location is not specified.

--save-params
        Save the parameters that you provide at the command line to the AWS SAM configuration file.

--tracing | --no-tracing
        Activate AWS X-Ray tracing for your Lambda functions.