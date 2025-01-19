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


Step 3: Create the SNS Publish Policy

1.Open the IAM service in the AWS Management Console.

2.Navigate to Policies → Create Policy.

![image_alt]()

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

![image_alt](https://github.com/Tatenda-Prince/NBA-Game-Day-Notifications-Sports-Alert-System-/blob/81180047352432c79adff2d344f559b6cece564f/images/Screenshot%202025-01-19%20095442.png)

5.Click Next: Tags (you can skip adding tags).


6.Click Next: Review.


7.Enter a name for the policy (e.g., gd_sns_policy).

![image_alt]()





8.Review and click Create Policy.



















   


 



