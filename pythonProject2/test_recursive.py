# test_recursive.py
import pytest
from test_config import PROTOCOLS, pickle_and_hash

@pytest.mark.parametrize("protocol", PROTOCOLS)
def test_recursive_list(protocol):
    obj = []
    obj.append(obj)
    hash1, data1 = pickle_and_hash(obj, protocol)
    hash2, data2 = pickle_and_hash(obj, protocol)
    assert hash1 == hash2
    assert data1 == data2
