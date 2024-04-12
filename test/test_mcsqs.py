"""End to end MCSQS tests."""

import uuid

from mcsqs.sqs_manager import (
    create_sns_consumer,
    receive_message_from_queue
)

from mcsqs.sns_manager import (
    publish_message_to_topic,
)

def test_source_and_multiple_consumers():
    """Creates a single source, SNS topic, and multiple destination queues."""

    # ARRANGE
    create_sns_consumer(queue_name='consumer1', topic_name='topic')
    create_sns_consumer(queue_name='consumer2', topic_name='topic')
    create_sns_consumer(queue_name='consumer3', topic_name='topic')

    # ACT
    message = str(uuid.uuid4())
    publish_message_to_topic('topic', message)

    # ASSERT    
    assert receive_message_from_queue('consumer1') == message
    assert receive_message_from_queue('consumer2') == message
    assert receive_message_from_queue('consumer3') == message

    assert receive_message_from_queue('consumer1') is None
    assert receive_message_from_queue('consumer2') is None
    assert receive_message_from_queue('consumer3') is None

