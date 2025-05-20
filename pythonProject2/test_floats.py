# test_floats.py
import pytest
import math
from test_config import PROTOCOLS, pickle_and_hash

special_floats = [float('nan'), float('inf'), float('-inf'), 1e308, -1e308]

@pytest.mark.parametrize("protocol", PROTOCOLS)
@pytest.mark.parametrize("value", special_floats)
def test_special_floats(protocol, value):
    hash1, data1 = pickle_and_hash(value, protocol)
    hash2, data2 = pickle_and_hash(value, protocol)
    assert hash1 == hash2
    assert data1 == data2
