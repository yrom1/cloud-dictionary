# magical-cloud-dictionary

A DynamoDB implementation of `collections.abc.MutableMapping`.

## Install

```bash
pip install magical-cloud-dictionary
```

## About

The idea for this project is to provide a Python dictionary-like experience for interacting with DynamoDB. To abstract away all the details and boilerplate of `boto3` and just have this magical dictionary-like object that you can call from anywhere in any repository and get your answer from the clouds.

The goal is not to implement all the features of `boto3`'s DynamoDB SDK with this interface. The goal is to make simple interactions with DynamoDB simple. A magic dictionary with usage restrictions, is still a magic dictionary!

One advantage of using DynamoDB as the backend is the ['Free 25 GB of storage and up to 200 million read/write requests per month with the AWS Free Tier'](https://aws.amazon.com/dynamodb/), which is available to everyone.

## Setup

The normal setup for `boto3` is required. Either a `~/.aws/credentials` and a `~/.aws/config` with the default region:

`~/.aws/credentials`
```
[default]
aws_access_key_id = ...
aws_secret_access_key = ...
```

`~/.aws/config`
```
[default]
region= ...
```

Or, the following ENV variables can be set: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_DEFAULT_REGION`.

One can feel safe as no code in `magical-cloud-dictionary` touches these credentials, they are all handled by `boto3` internally.

## Example

```py
>>> from magical_cloud_dictionary import Magic
>>> mp = Magic('test') # `test` is the name of an existing DynamoDB table
>>> mp['answer']
Decimal('42')
>>> mp['evil']
Decimal('666')
>>> del mp['evil']
>>> mp['evil']
...
magical_cloud_dictionary.main.MagicalCloudDictionaryError: Cannot find evil in test!
```
