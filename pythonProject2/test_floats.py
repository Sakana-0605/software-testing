# test_floats.py
import pickle
import hashlib
import sys

def sha256_digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def test_float_case(name, obj, protocol=None):
    print(f"\n====== Test Case: {name} ======")
    print(f"Input object: {obj}")

    try:

        # 第一次序列化
        pickled1 = pickle.dumps(obj, protocol=protocol)
        pickled2 = pickle.dumps(obj, protocol=protocol)
        hash1 = sha256_digest(pickled1)
        hash2 = sha256_digest(pickled2)
        print(f"SHA-256 Hash #1: {hash1}")
        print(f"SHA-256 Hash #2: {hash2}")

        # 判断是否稳定（哈希是否相同）
        hash_equal = (hash1 == hash2)
        print(f"Stable Serialization (Hash Match): {hash_equal}")

        # 反序列化
        unpickled = pickle.loads(pickled1)
        print("Unpickling succeeded.")

        # 直接比较反序列化对象和原对象是否相等
        print(f"Unpickled == Original: {unpickled == obj}")

    except Exception as e:
        print("Exception occurred during pickling or unpickling:")
        print(f"{type(e).__name__}: {e}")

def run_float_precision_tests():
    test_cases = {
        "positive_zero": 0.0,
        "negative_zero": -0.0,
        "positive_inf": float('inf'),
        "negative_inf": float('-inf'),
        "large_float": 1.79e308,
        "small_float": 5e-324,
        "mid_precision": 3.1415926535897932384626,
        "nan": float('nan')  # 不做特殊处理
    }

    for name, val in test_cases.items():
        test_float_case(name, {"value": val})

if __name__ == "__main__":
    run_float_precision_tests()
