import pickle
import hashlib
import sys
import platform
import json
from datetime import datetime
from pathlib import Path
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def sha256_digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def collect_system_info():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "timestamp": datetime.now().isoformat()
    }

def test_pickle_consistency(obj, protocol=None):
    protocol = protocol or pickle.HIGHEST_PROTOCOL

    hashes = [sha256_digest(pickle.dumps(obj, protocol=protocol)) for _ in range(2)]
    consistent_across_runs = all(h == hashes[0] for h in hashes)

    try:
        unpickled = pickle.loads(pickle.dumps(obj, protocol=protocol))
        repickled = pickle.dumps(unpickled, protocol=protocol)
        final_hash = sha256_digest(repickled)
        consistent_with_repickle = final_hash == hashes[0]
    except Exception as e:
        return {
            "error": str(e),
            "consistent_across_runs": False,
            "consistent_with_repickle": False
        }

    return {
        "initial_hash": hashes[0],
        "consistent_across_runs": consistent_across_runs,
        "consistent_with_repickle": consistent_with_repickle
    }

def test_path_pickle_stability():
    test_paths = {
        "windows_style_path": Path(r"C:\Users\User\file.txt"),
        "unix_style_path": Path("/home/user/file.txt"),
        "relative_path": Path("some/relative/path"),
        "current_dir": Path("."),
    }

    results = {}

    for name, path_obj in test_paths.items():
        pickled = pickle.dumps(path_obj, protocol=pickle.HIGHEST_PROTOCOL)
        hash_val = sha256_digest(pickled)
        results[name] = {
            "path_str": str(path_obj),
            "pickle_hash": hash_val,
            "pickle_bytes_sample": pickled.hex()[:60] + "..."
        }

    return results

def test_set_pickle_variation():
    test_sets = {
        "set_ints": {1, 2, 3, 4, 5},
        "set_strs": {"apple", "banana", "cherry"},
        "set_mixed": {1, "two", 3.0, (4, 5)},
        "set_empty": set(),
    }

    results = {}

    for name, s in test_sets.items():
        hashes = []
        for _ in range(2):
            pickled = pickle.dumps(s, protocol=pickle.HIGHEST_PROTOCOL)
            hashes.append(sha256_digest(pickled))
        consistent = all(h == hashes[0] for h in hashes)

        results[name] = {
            "hashes": hashes,
            "consistent_across_runs": consistent,
            "pickle_bytes_sample": pickled.hex()[:60] + "..."
        }

    return results

def main():
    protocol = pickle.HIGHEST_PROTOCOL

    # 测试对象（你给的）
    obj = {"float": 3.14159265358979323846, "nested": [None, True, -0.0, float("inf")], "flag": "🚀"}

    system_info = collect_system_info()
    test_result = test_pickle_consistency(obj, protocol)

    path_results = test_path_pickle_stability()
    set_results = test_set_pickle_variation()

    result = {
        "system_info": system_info,
        "protocol": protocol,
        "pickle_consistency_test": {
            "test_object": repr(obj),
            "result": test_result
        },
        "path_pickle_stability_test": path_results,
        "set_pickle_variation_test": set_results,
    }

    print("\n==== Combined Pickle Tests ====")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 保存为 JSON 文件
    try:
        with open("combined_pickle_test_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print("\nResult saved to combined_pickle_test_result.json")
    except Exception as e:
        print(f"Failed to save result: {e}")

if __name__ == "__main__":
    main()
