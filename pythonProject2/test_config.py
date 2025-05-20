# test_config.py
import pickle
import hashlib

PROTOCOLS = list(range(0, pickle.HIGHEST_PROTOCOL + 1))


def pickle_and_hash(obj, protocol):
    try:
        data = pickle.dumps(obj, protocol=protocol)
        return hashlib.sha256(data).hexdigest(), data
    except Exception as e:
        return str(e), None
