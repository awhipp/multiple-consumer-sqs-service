# Multiple Consumer SQS Library

Library used to setup multiple queues to read messages from a single SNS topic. Work-in-progress.

Idea being you can setup multiple services with their own topics, and have multiple services dynamically subscribe to those unique topics.

## Testing

To run the tests, you need to have `pytest` installed. You can install it using the following command:

```bash
poetry install
poetry shell
pytest
```

Ensure localstack is running.