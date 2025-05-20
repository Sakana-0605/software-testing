# test_exceptions.py
import pytest
import pickle
from test_config import PROTOCOLS, pickle_and_hash

class TrulyUnpicklable:
    """强制不可序列化的类（含 __slots__ 且显式阻止序列化）"""
    __slots__ = ("value",)  # 模拟含 __slots__ 的类

    def __init__(self, value):
        self.value = value

    def __getstate__(self):
        # 显式抛出 PicklingError 并设置自定义消息
        raise pickle.PicklingError("含 __slots__ 但强制不可序列化的类")

@pytest.mark.parametrize("protocol", PROTOCOLS)
def test_truly_unpicklable(protocol):
    """测试强制不可序列化的类（所有协议下均应抛出 PicklingError）"""
    obj = TrulyUnpicklable(42)
    hash_str, data = pickle_and_hash(obj, protocol)
    # 断言 1：序列化结果应为 None（不可序列化）
    assert data is None, f"协议 {protocol} 下应不可序列化"
    # 断言 2：异常消息应包含预期内容
    assert "含 __slots__ 但强制不可序列化的类" in hash_str, f"协议 {protocol} 未抛出预期的 PicklingError"