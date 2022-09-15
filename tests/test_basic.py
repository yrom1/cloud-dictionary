import pytest

from magical_cloud_dictionary import Magic


def test_put_get():
    mp = Magic("test")
    mp["answer"] = 42
    assert mp["answer"] == 42
