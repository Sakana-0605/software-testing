# test_whitebox.py
import pytest
import pickle
from test_config import PROTOCOLS, pickle_and_hash

def test_circular_reference_memo():
    """测试 pickle 对循环引用的 memo 标记（白盒：验证内部 memo 机制）"""
    class Node:
        def __init__(self):
            self.parent = None

    # 构造深度循环引用：A -> B -> A
    a = Node()
    b = Node()
    a.parent = b
    b.parent = a

    for protocol in PROTOCOLS:
        hash1, data1 = pickle_and_hash(a, protocol)
        hash2, data2 = pickle_and_hash(a, protocol)
        assert hash1 == hash2, f"循环引用 memo 不一致（协议 {protocol}）"

def test_protocol0_text_format():
    """测试协议0的文本格式（白盒：验证协议0的文本序列化逻辑）"""
    if 0 not in PROTOCOLS:
        pytest.skip("协议0不可用")

    obj = "hello"
    data = pickle.dumps(obj, protocol=0)
    assert data.startswith(b"cos\ns\n")  # 协议0对字符串的序列化前缀（源码中对应 STRING 操作码）

def test_protocol5_frozenset():
    """测试协议5对 frozenset 的支持（白盒：验证协议5的 FROZENSET 操作码）"""
    if pickle.HIGHEST_PROTOCOL < 5:
        pytest.skip("协议5不可用")

    obj = frozenset([1, 2, 3])
    data = pickle.dumps(obj, protocol=5)
    assert b"FROZENSET" in data  # 协议5使用 FROZENSET 操作码（源码中定义）