# cloud-dictionary

A DynamoDB implementation of `collections.abc.MutableMapping`.

## Install

Currently available on [PyPI](https://pypi.org/project/cloud-dictionary/), to install:
```
pip install cloud-dictionary
```

## About

The idea for this project is to provide a Python dictionary-like experience for interacting with DynamoDB. To abstract away all the details and boilerplate of `boto3` and just have this dictionary-like object that you can call from anywhere in any repository and get your answer from the clouds.

The goal is not to implement all the features of `boto3`'s DynamoDB SDK with this interface. The goal is to make simple interactions with DynamoDB simple.

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

One can feel safe knowing no code touches these credentials, they are handled by `boto3` internally.

## Example

```py
>>> from cloud_dictionary import Cloud
>>> mp = Cloud('test') # `test` is the name of an existing DynamoDB table
>>> mp['answer']
Decimal('42')
>>> mp['evil']
Decimal('666')
>>> del mp['evil']
>>> mp['evil']
...
cloud_dictionary.main.CloudDictionaryError: Cannot find evil in test!
>>> mp['json'] = {'seven': 7}
>>> mp['json']
{'seven': Decimal('7')}
```
