# test_custom_class.py
import pytest
from test_config import PROTOCOLS, pickle_and_hash

class MyClass:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, MyClass) and self.value == other.value

@pytest.mark.parametrize("protocol", PROTOCOLS)
def test_custom_object(protocol):
    obj = MyClass(42)
    hash1, data1 = pickle_and_hash(obj, protocol)
    hash2, data2 = pickle_and_hash(obj, protocol)
    assert hash1 == hash2
    assert data1 == data2
