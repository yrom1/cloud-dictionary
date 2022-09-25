from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any

import boto3


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
        self._iter = False
        self._exact = False
        self._table_scan = None
        self._table = table

    def _check_response(self, response):
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    def _put(self, key: KEY_TYPE, value: VALUE_TYPE) -> None:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self._table)
        response = table.put_item(
            Item={
                "key": key,
                "value": value,
            }
        )
        self._check_response(response)

    def _get(self, key: KEY_TYPE) -> VALUE_TYPE:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self._table)
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
            raise CloudDictionaryError(f"Cannot find {key} in {self._table}!")

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
        table = dynamodb.Table(self._table)
        response = table.delete_item(
            Key={
                "key": key,
            },
        )
        self._check_response(response)

    def _scan(self):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self._table)
        response = table.scan()
        self._check_response(response)
        result = response["Items"]
        # TODO if scan is > 1MB
        # found_more = False
        # while "LastEvaluatedKey" in response:
        #     found_more = True
        #     response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        # if found_more:
        #     result.extend(response["Items"])
        self._table_scan = result

    def __iter__(self):
        self._iter = True
        self._scan()
        self._position = 0
        return self

    def __next__(self):
        # handle forgot to iter() case
        if not self._iter:
            raise TypeError(f"'{type(self)}' object is not an iterator")
        if self._position >= len(self):
            raise StopIteration
        ans = self._table_scan[self._position]["key"]
        self._position += 1
        return ans

    def __len__(self):
        # if scan has been performed, more accurate result is given
        if self._table_scan is not None:
            length = len(self._table_scan)
            self._length = length
            self._exact = True
            return length
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self._table)
        length = table.item_count  # updated every 6 hours by aws
        self._length = table.item_count
        return length
