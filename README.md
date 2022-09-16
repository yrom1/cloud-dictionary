# magical-cloud-dictionary

A DynamoDB implementation of `collections.abc.MutableMapping`.

## About

The idea for this project is to provide a Python dictionary like experience for interacting with DynamoDB. To abstract away all the details and boilerplate of `boto3` and just have this magical dictionary-like object that you can call from anywhere in any repository and get your answer from the clouds.

The goal is not to implement all the features of `boto3`'s DynamoDB SDK with this interface. The goal is to make simple interactions with DynamoDB simple. A magic dictionary with usage restrictions, is still a magic dictionary!

One advantage of using DynamoDB as the backend is the ['Free 25 GB of storage and up to 200 million read/write requests per month with the AWS Free Tier'](https://aws.amazon.com/dynamodb/), which is available to everyone.
