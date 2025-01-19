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
