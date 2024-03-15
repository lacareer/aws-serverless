# Herein are the instructions for this module 

# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-reference.html

<!-- Module goals -->
Understand the local SAM development workflow
Run unit tests for a SAM application: sam-app
Use SAM local to run Lambda functions in a local environment for testing our sam-app

<!-- install dependencies -->

cd ~/PATH-TO/sam-app/hello_world
pip3 install -r requirements.txt  (run if not installed)

<!-- Run locally -->
1.
cd ~/PATH-TO/sam-app
sam local invoke --event events/event.json

2.
cd ~/PATH-TO/sam-app
sam local start-api --port 8080

3.
Run on terminal to test lambda: curl localhost:8080/hello
        OR
Go to: localhost:8080/hello, on your brower(did not work for me)

<!-- make changes to python code and repeat 'Run locally" step 3 -->
<!-- new lambda return statement -->
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello my friend",
            # "location": ip.text.replace("\n", "")
        }),
    }


<!-- Run unit test -->
d ~/PATH-TO/sam-app
pip3 install pytest pytest-mock (run if not installed)

python3 -m pytest tests/unit (runs pytest/unit test on ~/PATH-TO/sam-app/tests/unit)

The Pytest should fail because it finds "hello my friend" and not "hello world"

<!-- Change the unit test in test_handler.py to include the below -->
    assert data["message"] == "hello my friend"

    <!-- re-run the below -->
    python3 -m pytest tests/unit