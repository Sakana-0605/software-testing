# test_equivalent_inputs.py
import pytest
from test_config import PROTOCOLS, pickle_and_hash

# 语义等价但语法不同的输入对（值相同但生成方式不同）
equivalent_pairs = [
    (2 + 3, 5),
    (3.14, 3.0 + 0.14),
    ("hello", "hel" + "lo"),
    (b"bytes", b"by" + b"tes"),
    ((1, 2, 3), tuple([1, 2, 3])),
    ({1, 2, 3}, set([3, 2, 1])),  # 集合无序，值相同
]

@pytest.mark.parametrize("protocol", PROTOCOLS)
@pytest.mark.parametrize("a, b", equivalent_pairs)
def test_equivalent_inputs(a, b, protocol):
    """验证等价输入的序列化结果是否一致"""
    hash_a, data_a = pickle_and_hash(a, protocol)
    hash_b, data_b = pickle_and_hash(b, protocol)
    assert hash_a == hash_b, f"等价输入序列化结果不一致（{a} vs {b}）"