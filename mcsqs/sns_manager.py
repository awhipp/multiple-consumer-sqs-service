"""Manages SNS Topics and Subscriptions"""

from mcsqs.utils.boto_helper import get_client

def get_or_create_topic(topic_name: str):
    """Get or create a SNS topic.
    
    Args:
        topic_name (str): The name of the topic.
    
    Returns:
        str: The ARN of the topic.
    """

    # Check if it exists
    sns = get_client('sns')
    response = sns.list_topics()
    if 'Topics' in response:
        topics = response['Topics']
        for topic in topics:
            if topic_name in topic['TopicArn']:
                return topic['TopicArn']
        
    # Create the topic
    response = sns.create_topic(Name=topic_name)
    return response['TopicArn']

def publish_message_to_topic(topic_name: str, message: str):
    """Publish a message to a SNS topic.
    
    Args:
        topic_name (str): The name of the topic.
        message (str): The message to publish.
    """
    topic_arn = get_or_create_topic(topic_name)
    
    sns = get_client('sns')
    response = sns.publish(
        TopicArn=topic_arn,
        Message=message,
    )
    
    # Raise exception on failure
    if 'MessageId' not in response:
        raise Exception('Failed to publish message to topic')