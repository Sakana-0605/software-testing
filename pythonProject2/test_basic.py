# test_basic.py
import pytest
from test_config import PROTOCOLS, pickle_and_hash

@pytest.mark.parametrize("obj", [123, -456, 3.14, True, False, None, "hello", b"bytes"])
@pytest.mark.parametrize("protocol", PROTOCOLS)
def test_basic_types(obj, protocol):
    hash1, data1 = pickle_and_hash(obj, protocol)
    hash2, data2 = pickle_and_hash(obj, protocol)
    assert hash1 == hash2
    assert data1 == data2
