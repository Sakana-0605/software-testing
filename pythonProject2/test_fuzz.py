import pickle
import hashlib
import random
import string
import random

# Utility: compute SHA256 hash
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

class RandomizedReduce:
    def __init__(self, x):
        self.x = x
    def __reduce__(self):
        # 故意在 reduce 中制造不稳定结构
        return (self.__class__, (self.x + random.randint(0, 5),))
    
def random_string(max_len=10):
    length = random.randint(1, max_len)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ----------------- Class Definitions -----------------
class NoReduce:
    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return isinstance(other, NoReduce) and self.x == other.x


class WithReduce:
    def __init__(self, y):
        self.y = y

    def __reduce__(self):
        return (self.__class__, (self.y,))

    def __eq__(self, other):
        return isinstance(other, WithReduce) and self.y == other.y


class WithGetState:
    def __init__(self, z):
        self.z = z

    def __getstate__(self):
        return {'z': self.z}

    def __setstate__(self, state):
        self.z = state['z']

    def __eq__(self, other):
        return isinstance(other, WithGetState) and self.z == other.z


class FuzzClass:
    def __init__(self, val):
        self.val = val

    def __reduce__(self):
        return (self.__class__, (self.val,))

    def __eq__(self, other):
        return isinstance(other, FuzzClass) and self.val == other.val



# ----------------- Fuzz Testing -----------------
def fuzz_data(depth=0, max_depth=3):
    if depth > max_depth:
        return random.choice([
            None,
            random.randint(-1000, 1000),
            random.random(),
            float('nan'),
            float('inf'),
            float('-inf'),
            random_string(),
            True,
            False,
            b"bytes",
            bytearray(b"bytes"),
        ])
    choice = random.randint(0, 14)
    if choice == 0:
        return None
    elif choice == 1:
        return random.randint(-10000, 10000)
    elif choice == 2:
        return random.choice([random.random(), float('nan'), float('inf'), float('-inf')])
    elif choice == 3:
        return random_string()
    elif choice == 4:
        return [fuzz_data(depth+1, max_depth) for _ in range(random.randint(0, 5))]
    elif choice == 5:
        return tuple(fuzz_data(depth+1, max_depth) for _ in range(random.randint(0, 5)))
    elif choice == 6:
        return {random_string(): fuzz_data(depth+1, max_depth) for _ in range(random.randint(0, 5))}
    elif choice == 7:
        elements = [fuzz_data(depth+1, max_depth) for _ in range(random.randint(0, 5))]
        hashable_elements = []
        for e in elements:
            try:
                hash(e)
                hashable_elements.append(e)
            except TypeError:
                continue
        return set(hashable_elements)
    elif choice == 8:
        return bytearray(random_string().encode('utf-8'))
    elif choice == 9:
        return frozenset([random_string() for _ in range(random.randint(1, 4))])
    elif choice == 10:
        return RandomizedReduce(random.randint(0, 100))
    elif choice == 11:
        return NoReduce(random.randint(0, 100))
    elif choice == 12:
        return WithReduce(random.randint(0, 100))
    elif choice == 13:
        return WithGetState(random.randint(0, 100))
    else:
        return FuzzClass(random_string())



def fuzz_test(iterations=100):
    print("=== Fuzz Testing ===")
    success = 0
    stable = 0
    unstable_by_design = 0

    for i in range(iterations):
        obj = fuzz_data()
        try:
            data1 = pickle.dumps(obj, protocol=4)
            data2 = pickle.dumps(obj, protocol=4)
            hash1 = sha256_bytes(data1)
            hash2 = sha256_bytes(data2)

            if isinstance(obj, RandomizedReduce):
                unstable_by_design += 1
                print(f"[Designed Unstable] Test case #{i+1} intentionally unstable (RandomizedReduce)")
                print()
            else:
                if hash1 == hash2:
                    stable += 1
                else:
                    print(f"[Unstable] Test case #{i+1} hash mismatch")
                    print(f"Object type: {type(obj)} Value: {repr(obj)}")
                    print(f"Hash1: {hash1}")
                    print(f"Hash2: {hash2}")
                    print()

            obj2 = pickle.loads(data1)
            if isinstance(obj, (int, float, str, type(None), bool)):
                if obj == obj2:
                    success += 1
                else:
                    print(f"[Mismatch] Test case #{i+1} value mismatch after deserialization\n")
            else:
                success += 1
        except Exception as e:
            print(f"[Exception] Test case #{i+1} raised an error: {e}")
            print(f"Object type: {type(obj)} Value: {repr(obj)}")
            print()

    print(f"Total tests: {iterations}")
    print(f"Successful round-trip: {success}")
    print(f"Stable serialization: {stable}")
    print(f"Skipped (intentional instability): {unstable_by_design}")
    print("=== Fuzz Testing Complete ===\n")


# ----------------- Entry Point -----------------
def main():
        random.seed(42)
        fuzz_test(100)

if __name__ == "__main__":
    main()
