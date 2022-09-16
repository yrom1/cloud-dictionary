import pytest

from cloud_dictionary import Cloud


def test_put_get():
    mp = Cloud("test")
    mp["answer"] = 42
    assert mp["answer"] == 42
