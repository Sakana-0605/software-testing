import pickle
import hashlib
import sys

# 模块级定义的可pickle类
class MyClass:
    def __init__(self):
        self.x = 123

    def __eq__(self, other):
        return isinstance(other, MyClass) and self.x == other.x

def add_one(x):
    return x + 1  # 模块级函数，可pickle（部分协议下）

def sha256_digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def test_pickle_stability(name, obj, protocol=None):
    print(f"\n====== Test Case: {name} ======")
    print(f"--- Testing with Python {sys.version} ---")
    print(f"Input object: {repr(obj)}")
    
    try:
        # 第一次序列化
        pickled1 = pickle.dumps(obj, protocol=protocol if protocol is not None else pickle.HIGHEST_PROTOCOL)
        pickled2 = pickle.dumps(obj, protocol=protocol if protocol is not None else pickle.HIGHEST_PROTOCOL)
        hash1 = sha256_digest(pickled1)
        print(f"SHA-256 Hash #1: {hash1}")
        hash2 = sha256_digest(pickled2)
        print(f"SHA-256 Hash #2: {hash2}")

        # 判断是否稳定（哈希是否相同）
        hash_equal = (hash1 == hash2)
        print(f"Stable Serialization (Hash Match): {hash_equal}")
        
        # 反序列化
        unpickled = pickle.loads(pickled1)

        # 其他对比
        print(f"Unpickled == Original: {unpickled == obj}")
        print(f"Unpickled is Original: {unpickled is obj}")
        
    except Exception as e:
        print("Exception occurred during pickling or unpickling:")
        print(f"{type(e).__name__}: {e}")


def run_tests():
    test_cases = {
        "simple_dict": {"a": 1, "b": 2},
        "float_nan": {"x": float('nan')},
        "custom_class": MyClass(),
        "nested_list": [[i for i in range(5)] for _ in range(5)],
        "module_func": add_one,  # 可pickle（部分协议）
    }

    for name, obj in test_cases.items():
        test_pickle_stability(name, obj, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    run_tests()

