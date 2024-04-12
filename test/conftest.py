"""Test configuration file for pytest."""

import pytest

from mcsqs.utils.boto_helper import get_client

from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(autouse=True)
def clear_all_queues():
    """Clears all queues before each test."""
    sqs = get_client('sqs')
    response = sqs.list_queues()
    if 'QueueUrls' in response:
        queues = response['QueueUrls']
        for queue in queues:
            sqs.delete_queue(QueueUrl=queue)

@pytest.fixture(autouse=True)
def clear_all_topics():
    """Clears all topics before each test."""
    sns = get_client('sns')
    response = sns.list_topics()
    if 'Topics' in response:
        topics = response['Topics']
        for topic in topics:
            sns.delete_topic(TopicArn=topic['TopicArn'])