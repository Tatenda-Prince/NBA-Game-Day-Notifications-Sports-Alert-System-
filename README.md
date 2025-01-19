# NBA-Game-Day-Notifications-Sports-Alert-System

"Live Scores"

# Technical Architecture 
![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/4deb303efb10b5eba0dbe684a62ed412956b7b66/images/Screenshot%202025-01-18%20190853.png)

# Introduction

## Project Overview 

This project is an alert system that sends real-time NBA game day score notifications to subscribed users via SMS/Email. It leverages Amazon SNS, AWS Lambda and Python, Amazon EvenBridge and NBA APIs to provide sports fans with up-to-date game information. The project demonstrates cloud computing principles and efficient notification mechanisms.

# Background

## Amazon SNS 

Amazon SNS (Simple Notification Service) is a fully managed messaging service offered by Amazon Web Services (AWS). It facilitates communication between distributed systems, microservices, and event-driven serverless applications by enabling message delivery across multiple channels.

## AWS Lambda 

AWS Lambda is a serverless computing service provided by Amazon Web Services (AWS). It allows you to run code without provisioning or managing servers. With Lambda, you simply upload your code, and AWS takes care of the underlying infrastructure, scaling, and maintenance.

## Amazon EventBridge 

Amazon EventBridge is a serverless event bus service provided by AWS that helps you integrate applications using events. It enables you to connect applications across AWS services, third-party SaaS applications, and your custom applications. EventBridge simplifies building event-driven architectures by routing events based on pre-defined rules to targets such as AWS Lambda, Step Functions, Amazon SQS.

## Amazon CloudWatch 

Amazon CloudWatch is a monitoring and observability service provided by Amazon Web Services (AWS). It is designed to help you collect, analyze, and act on data and metrics from your AWS resources, applications, and services in real-time. 

## PythonBoto3 

Boto3 is the Amazon Web Services (AWS) SDK for Python. It enables Python developers to interact programmatically with AWS services, making it easier to build, manage, and automate cloud-based applications and resources. 

## NBA API

NBA APIs (Application Programming Interfaces) are services that provide access to basketball-related data and functionalities from the National Basketball Association (NBA). These APIs are widely used by developers to build applications, websites, or data analysis tools centered around NBA content. Such as Live game scores and updates and Game schedules and results.

# Prerequisites

1.Free account with subscription and API Key at sportsdata.io

2.Personal AWS account with basic understanding of AWS and Pythonboto3 installed 

3.Visual Code Studio

## Technologies Used

1.Cloud Provider: AWS

2.Core Services: SNS, Lambda, EventBridge

3.External API: NBA Game API (SportsData.io)

4.Programming Language: Python 3.x

5.IAM Security:
Least privilege policies for Lambda, SNS, and EventBridge.

# Objectives

1.Fetches live NBA game scores using an external API.

2.Sends formatted score updates to subscribers via SMS/Email using Amazon SNS.

3.Scheduled automation for regular updates using Amazon EventBridge.

4.Designed with security in mind, following the principle of least privilege for IAM roles.

## Step 1: Create an SNS Topic using pythonboto3 

1.Open the your Visual Code Studio and create a new file sns.py  copy and paste the code below.


```python
import boto3

def create_sns_topic(topic_name):
    # Create an SNS client
    sns_client = boto3.client('sns', region_name='us-east-1')  # Replace with your region

    try:
        # Create a topic
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response['TopicArn']
        print(f"Topic created successfully! ARN: {topic_arn}")
        return topic_arn
    except Exception as e:
        print(f"Error creating topic: {e}")
        return None

if __name__ == "__main__":
    topic_name = "gameday_topic"  # Replace with your desired topic name
    create_sns_topic(topic_name)
```

To run this python file simply type:

`python sns.py`

After you run the file you should be able to see the same message as below

![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/49632a24960d7fa4b445dfcb4875703a1a08e91b/images/Screenshot%202025-01-19%20094642.png)

Now that our SNS Topic was successfully created navigate to your aws management console to view your SNS Topic.

![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/73442e88ff280ba0a7bb52c16676c37e100d4b74/images/Screenshot%202025-01-19%20094742.png)


## Step 2: Add Subscriptions to the SNS Topic

1.After creating the topic, click on the topic name from the list.

2.Navigate to the Subscriptions tab and click Create subscription

3.Select a Protocol:

   ~ Choose Email.
   
  ~ Enter a valid email address.

![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/ddcd1099c7cea634b1ba2beadc20e8c2fd4975bc/images/Screenshot%202025-01-19%20094902.png)

Now click Create Subscription

4.If you added an Email subscription:

~ Check the inbox of the provided email address.

~ Confirm the subscription by clicking the confirmation link in the email.

Now head back to your console to check that pending confirmation if it was successfully.

![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/2fb9b12882547272a7eaa4d0e2ba310bfd154376/images/Screenshot%202025-01-19%20095007.png)


## Step 3: Create the SNS Publish Policy

1.Open the IAM service in the AWS Management Console.

2.Navigate to Policies → Create Policy.

![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/81180047352432c79adff2d344f559b6cece564f/images/Screenshot%202025-01-19%20095442.png)

3.Click JSON and paste the JSON policy from gd_sns_policy.json file below

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "arn:aws:sns:REGION:ACCOUNT_ID:gd_topic"
        }
    ]
}
```

4.Replace REGION and ACCOUNT_ID with your AWS region and account ID.


![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/8ee4b446403f16d807972965be5162d71f0982ac/images/Screenshot%202025-01-19%20095927.png)


5.Click Next: Tags (you can skip adding tags).


6.Click Next: Review.


7.Enter a name for the policy (e.g., gd_sns_policy).

![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/b12025a7d372cdc229e6b63af02d591a69a3da49/images/Screenshot%202025-01-19%20100005.png)


8.Review and click Create Policy.


## Step 4: Create an IAM Role for Lambda

1.Open the IAM service in the AWS Management Console.


2.Click Roles → Create Role.

![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/63d073df33ad28d7920b357f001d4e15b8e51f7b/images/Screenshot%202025-01-19%20100118.png)



3.Select AWS Service and choose Lambda.

![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/de7a4900b9a475936ab3a65b93de1fea234e5797/images/Screenshot%202025-01-19%20100131.png) 

4.Attach the following policies:

~SNS Publish Policy (gd_sns_policy) (created in the previous step).

~Lambda Basic Execution Role (AWSLambdaBasicExecutionRole) (an AWS managed policy).

![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/becfa634c7e5444b301a14222de7a4d1b07b8d1e/images/Screenshot%202025-01-19%20100338.png)


5.Click Next: Tags (you can skip adding tags).

6.Click Next: Review.

7.Enter a name for the role (e.g., gd_role).

![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/8ee1718151d57afa90e3c9d5bfde15ebc2f8ef5f/images/Screenshot%202025-01-19%20100428.png)


8.Review and click Create Role.

9.Copy and save the ARN of the role for use in the Lambda function.


Step 5: Deploy the Lambda Function

1.Open the AWS Management Console and navigate to the Lambda service.


2.Click Create Function.

![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/16e292a69379287223a07de908934dd09960d55e/images/Screenshot%202025-01-19%20100554.png)

3.Select Author from Scratch.

5.Enter a function name (e.g., gameday_lambdafuction_notifications).

6.Choose Python 3.x as the runtime.

![image_alt]()

7.Assign the IAM role created earlier (gameday_role) to the function.

![image_alt]()

~ Under the Function Code section:

~Copy the content of the gd_notifications.py file from the repository.

```python
import os
import json
import urllib.request
import boto3
from datetime import datetime, timedelta, timezone

def format_game_data(game):
    status = game.get("Status", "Unknown")
    away_team = game.get("AwayTeam", "Unknown")
    home_team = game.get("HomeTeam", "Unknown")
    final_score = f"{game.get('AwayTeamScore', 'N/A')}-{game.get('HomeTeamScore', 'N/A')}"
    start_time = game.get("DateTime", "Unknown")
    channel = game.get("Channel", "Unknown")
    
    # Format quarters
    quarters = game.get("Quarters", [])
    quarter_scores = ', '.join([f"Q{q['Number']}: {q.get('AwayScore', 'N/A')}-{q.get('HomeScore', 'N/A')}" for q in quarters])
    
    if status == "Final":
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Final Score: {final_score}\n"
            f"Start Time: {start_time}\n"
            f"Channel: {channel}\n"
            f"Quarter Scores: {quarter_scores}\n"
        )
    elif status == "InProgress":
        last_play = game.get("LastPlay", "N/A")
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Current Score: {final_score}\n"
            f"Last Play: {last_play}\n"
            f"Channel: {channel}\n"
        )
    elif status == "Scheduled":
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Start Time: {start_time}\n"
            f"Channel: {channel}\n"
        )
    else:
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Details are unavailable at the moment.\n"
        )

def lambda_handler(event, context):
    # Get environment variables
    api_key = os.getenv("NBA_API_KEY")
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns_client = boto3.client("sns")
    
    # Adjust for Central Time (UTC-6)
    utc_now = datetime.now(timezone.utc)
    south_africa_time= utc_now - timedelta(hours=2)  # Central Time is UTC-6
    today_date = south_africa_time.strftime("%Y-%m-%d")
    
    print(f"Fetching games for date: {today_date}")
    
    # Fetch data from the API
    api_url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{today_date}?key={api_key}"
    print(today_date)
     
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            print(json.dumps(data, indent=4))  # Debugging: log the raw data
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return {"statusCode": 500, "body": "Error fetching data"}
    
    # Include all games (final, in-progress, and scheduled)
    messages = [format_game_data(game) for game in data]
    final_message = "\n---\n".join(messages) if messages else "No games available for today."
    
    # Publish to SNS
    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=final_message,
            Subject="NBA Game Updates"
        )
        print("Message published to SNS successfully.")
    except Exception as e:
        print(f"Error publishing to SNS: {e}")
        return {"statusCode": 500, "body": "Error publishing to SNS"}
    
    return {"statusCode": 200, "body": "Data processed and sent to SNS"}

```

Paste it into the inline code editor.

8.Under the Environment Variables section, add the following:

~NBA_API_KEY: your NBA API key.
~SNS_TOPIC_ARN: the ARN of the SNS topic created earlier.

![image_alt]()

9.Click Create Function.




















   


 



