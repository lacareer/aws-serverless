import boto3
import json
import csv
from io import StringIO
import os
import time
from random import randint
from botocore.client import Config

# set a few variables we'll use to get our data
activity_arn = os.getenv('ACTIVITY_ARN')
worker_name = os.getenv('HOSTNAME')
region = os.getenv('REGION')

print('starting job...')

# setup our client
config = Config(
  connect_timeout=65,
  read_timeout=65,
  retries={'max_attempts': 0}
)
client = boto3.client('stepfunctions', region_name=region, config=config)
s3_client = boto3.client('s3', region_name=region)
s3 = boto3.resource('s3')

# now we start polling until we have nothing left to do. i realize this should
# be more functions and it's pretty gross but it works for a demo :) 
while True:
  response = client.get_activity_task(
    activityArn = activity_arn,
    workerName = worker_name
  )

  if 'input' not in response.keys() or 'taskToken' not in response.keys():
    print('no tasks to process...waiting 30 seconds to try again')
    time.sleep(30)
    continue
    # break

  token = response['taskToken']
  data = json.loads(response['input'])
  items = data['Items']
  other = data['BatchInput']
  rndbkt = other['dstbkt'] 
  success = True
  cause = ""
  error = ""
  results = ["NO", "NO", "NO", "NO", "YES", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO", "NO"]
  for item in items:
    try:
      source = s3_client.get_object(Bucket=other['srcbkt'], Key=item['Key'])
      content = source.get('Body').read().decode('utf-8')
      buf = StringIO(content)
      reader = csv.DictReader(buf)
      objects = list(reader)

      # just randomly assign a value with a theoretical ballpark of 5% of the values being 'YES'
      objects[0]['WillDefault'] = results[randint(0,19)]

      stream = StringIO()
      headers = list(objects[0].keys())
      writer = csv.DictWriter(stream, fieldnames=headers)
      writer.writeheader()
      writer.writerows(objects)
      body = stream.getvalue()

      dst = s3.Object(rndbkt, other['dstkey'] + '/' + item['Key'].split('/')[1])
      dst.put(Body=body)

    except Exception as e:
      cause = "failed to process object " + item['Key'],
      error = str(e)
      success = False
      break
  
  if success:
    client.send_task_success(
      taskToken = token,
      output = "{\"message\": \"success\"}"
    )
  else:
    client.send_task_failure(
      taskToken = token,
      cause = cause,
      error = error
    )
