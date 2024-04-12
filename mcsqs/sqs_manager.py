"""Manages SQS Queues and Messages"""

import json

from mcsqs.utils.boto_helper import get_client
from mcsqs.sns_manager import get_or_create_topic

def get_or_create_queue(queue_name: str):
    """Get or create a SQS queue.
    
    Args:
        queue_name (str): The name of the queue.
    
    Returns:
        str: The URL of the queue.
    """

    # Check if it exists
    sqs = get_client('sqs')
    response = sqs.list_queues()
    if 'QueueUrls' in response:
        queues = response['QueueUrls']
        for queue in queues:
            if queue_name in queue:
                return queue
        
    # Create the queue
    response = sqs.create_queue(QueueName=queue_name)
    return response['QueueUrl']

def get_queue_arn(queue_name: str):
    """Get the ARN of a SQS queue.
    
    Args:
        queue_name (str): The name of the queue.
    
    Returns:
        str: The ARN of the queue.
    """
    sqs = get_client('sqs')
    queue_url = get_or_create_queue(queue_name)
    response = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['QueueArn']
    )
    return response['Attributes']['QueueArn']

def create_sns_consumer(queue_name: str, topic_name: str):
    """Connects a destination queue from an SNS topic.
    
    Args:
        queue_name (str): The name of the queue.
        topic_name (str): The name of the topic.
    """
    queue_url = get_or_create_queue(queue_name)
    queue_arn = get_queue_arn(queue_name)
    topic_arn = get_or_create_topic(topic_name)
    
    # Subscribe the queue to the topic
    sns = get_client('sns')
    sns.subscribe(
        TopicArn=topic_arn,
        Protocol='sqs',
        Endpoint=queue_arn
    )
    
    # Authorize the topic to send messages to the queue
    sqs = get_client('sqs')
    sqs.set_queue_attributes(
        QueueUrl=queue_url,
        Attributes={
            'Policy': f"""{{
                "Version": "2012-10-17",
                "Statement": [
                    {{
                        "Effect": "Allow",
                        "Principal": {{"AWS": "*"}},
                        "Action": "sqs:SendMessage",
                        "Resource": "{queue_url}",
                        "Condition": {{
                            "ArnEquals": {{
                                "aws:SourceArn": "{topic_arn}"
                            }}
                        }}
                    }}
                ]
            }}"""
        }
    )

def send_message_to_queue(queue_name: str, message: str):
    """Sends a message to a queue.
    
    Args:
        queue_name (str): The name of the queue.
        message (str): The message to send.
    """
    sqs = get_client('sqs')
    queue_url = get_or_create_queue(queue_name)
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message
    )

def receive_message_from_queue(queue_name: str, wait_time: int = 1):
    """Receives a message from a queue.
    
    Args:
        queue_name (str): The name of the queue.
    
    Returns:
        str: The message.
    """
    sqs = get_client('sqs')
    queue_url = get_or_create_queue(queue_name)
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=wait_time
    )
    messages = response.get('Messages', [])
    if len(messages) == 0:
        return None
    message = messages[0]
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=message['ReceiptHandle']
    )
    return json.loads(message['Body'])['Message']