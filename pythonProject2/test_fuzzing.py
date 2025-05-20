# test_fuzzing.py
import pickle
import random
import string
import hashlib
from test_config import PROTOCOLS, pickle_and_hash


def random_primitive():
    return random.choice([
        random.randint(-1000, 1000),
        random.uniform(-1e5, 1e5),
        ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        bytes(random.getrandbits(8) for _ in range(10)),
        True, False, None
    ])


def random_object(depth=0):
    """递归构造随机结构，避免过深递归"""
    if depth > 2:
        return random_primitive()

    typ = random.choice(['list', 'dict', 'primitive'])
    if typ == 'primitive':
        return random_primitive()
    elif typ == 'list':
        return [random_object(depth + 1) for _ in range(random.randint(0, 5))]
    else:  # dict
        return {
            ''.join(random.choices(string.ascii_letters, k=5)): random_object(depth + 1)
            for _ in range(random.randint(0, 5))
        }


def test_manual_fuzzing():
    """运行 100 个随机对象，每个对象测试所有协议是否稳定"""
    for i in range(100):
        obj = random_object()
        for protocol in PROTOCOLS:
            hash1, data1 = pickle_and_hash(obj, protocol)
            hash2, data2 = pickle_and_hash(obj, protocol)
            assert hash1 == hash2, f"Hash mismatch at iteration {i}, protocol {protocol}"
            assert data1 == data2, f"Data mismatch at iteration {i}, protocol {protocol}"
