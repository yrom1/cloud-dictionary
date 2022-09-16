from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any

import boto3

# Okay here's the plan bucko:
# https://realpython.com/inherit-python-dict/
# Building a Dictionary-Like Class From an Abstract Base Class
# This strategy for creating dictionary-like classes requires that you inherit
# from an abstract base class (ABC), like MutableMapping. This class provides
# concrete generic implementations of all the dictionary methods except for
# .__getitem__(), .__setitem__(), .__delitem__(), .__iter__(), and .__len__(),
# which you’ll have to implement by yourself.

# Additionally, suppose you need to customize the functionality of any other
# standard dictionary method. In that case, you’ll have to override the method
# at hand and provide a suitable implementation that fulfills your needs.

# This process implies a fair amount of work. It’s also error-prone and
# requires advanced knowledge of Python and its data model. It can also imply
# performance issues because you’ll be writing the class in pure Python.

# The main advantage of this strategy is that the parent ABC will alert you
# if you miss any method in your custom implementation.

# For these reasons, you should embrace this strategy only if you need a
# dictionary-like class that’s fundamentally different from the built-in
# dictionary.

# Referenced materials:
# https://docs.python.org/3/reference/datamodel.html
# https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping


class CloudDictionaryError(Exception):
    pass


KEY_TYPE = str
VALUE_TYPE = Any  # TODO type of value, it's not Any


class Cloud(MutableMapping):
    def __init__(self, table: KEY_TYPE) -> None:
        # TODO in the future, allow no name provided, just make tables:
        # __CLOUD_KEY_STR__, __CLOUD_KEY_NUMBER__, ...
        # so I can support all valid keys
        # NOTE I assume you have a ~/.aws/credentials and ~/.aws/config
        # or equivalent ENV variables
        # TODO create table if not exists logic
        self.table = table

    def _check_response(self, response):
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    def _put(self, key: KEY_TYPE, value: VALUE_TYPE) -> None:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table)
        response = table.put_item(
            Item={
                "key": key,
                "value": value,
            }
        )
        self._check_response(response)

    def _get(self, key: KEY_TYPE) -> VALUE_TYPE:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table)
        response = table.get_item(
            Key={
                "key": key,
            }
        )
        self._check_response(response)
        return response["Item"]["value"]

    def _test_valid_key(self, key: KEY_TYPE) -> None:
        try:
            assert type(key) == str
        except AssertionError:
            CloudDictionaryError("Only string keys are supported currently!")

    def __getitem__(self, key: KEY_TYPE):
        self._test_valid_key(key)
        try:
            return self._get(key)
        except KeyError:
            raise CloudDictionaryError(f"Cannot find {key} in {self.table}!")

    def __setitem__(self, key: KEY_TYPE, value: VALUE_TYPE):
        self._test_valid_key(key)
        self._put(key, value)

    def __delitem__(self, key):
        # TODO currently deleting a key that doesn't exist is not an error!
        #      this differs from the built in:
        """
        >>> mp = Cloud('test')
        >>> mp['answer']
        Decimal('42')
        >>> del mp['answer']
        >>> del mp['answer']
        >>> d = {0:1}
        >>> d[0]
        1
        >>> del d[0]
        >>> del d[0]
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        KeyError: 0
        """
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table)
        response = table.delete_item(
            Key={
                "key": key,
            },
        )
        self._check_response(response)

    def __iter__(self):
        raise NotImplementedError

    def __len__(self):
        # NOTE this is only updated every 6 hours by AWS
        #      I could do a table scan for exact result
        #      maybe offer an 'exact' flag
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table)
        return table.item_count
