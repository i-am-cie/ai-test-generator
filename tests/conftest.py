"""Pytest 共享配置：把项目根目录加入导入路径，并在未安装 ollama 包时注入占位模块。"""

import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# 未安装 ollama Python 包时，注入一个占位模块，保证 test_generator 可被导入；
# 具体测试用例通过 unittest.mock 替换 ollama.chat，不会发起真实请求。
if "ollama" not in sys.modules:
    _fake = types.ModuleType("ollama")
    _fake.chat = lambda **kwargs: {"message": {"content": ""}}
    sys.modules["ollama"] = _fake
