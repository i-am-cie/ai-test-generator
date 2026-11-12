"""
test_generator.py 的单元测试。

大模型调用通过 unittest.mock 打桩，测试本身不依赖 Ollama 是否在线，
也不依赖 ollama Python 包是否安装（见 conftest.py）。
"""

import csv
import io
import json
from unittest.mock import MagicMock, patch

import test_generator as tg


def _fake_ollama(content: str) -> MagicMock:
    return MagicMock(return_value={"message": {"content": content}})


# ---------- generate_structured_test_cases ----------

def test_structured_parses_plain_json_array():
    payload = '[{"id": "TC001", "title": "登录成功", "priority": "P0"}]'
    with patch.object(tg.ollama, "chat", _fake_ollama(payload)):
        cases = tg.generate_structured_test_cases("用户登录")
    assert cases == [{"id": "TC001", "title": "登录成功", "priority": "P0"}]


def test_structured_strips_markdown_fence_and_surrounding_text():
    payload = '下面是用例：\n```json\n[{"id": "TC002", "title": "密码错误"}]\n```\n以上。'
    with patch.object(tg.ollama, "chat", _fake_ollama(payload)):
        cases = tg.generate_structured_test_cases("用户登录")
    assert cases == [{"id": "TC002", "title": "密码错误"}]


def test_structured_returns_empty_on_invalid_json():
    with patch.object(tg.ollama, "chat", _fake_ollama("这不是 JSON，也没有数组")):
        cases = tg.generate_structured_test_cases("需求")
    assert cases == []


def test_structured_returns_empty_on_empty_content():
    with patch.object(tg.ollama, "chat", _fake_ollama("")):
        cases = tg.generate_structured_test_cases("需求")
    assert cases == []


# ---------- export_to_json ----------

def test_export_json_writes_utf8_and_indent(tmp_path):
    cases = [{"id": "TC001", "title": "登录成功", "priority": "P0"}]
    out = tmp_path / "cases.json"
    tg.export_to_json(cases, str(out))

    data = json.loads(out.read_text(encoding="utf-8"))
    assert data == cases

    raw = out.read_text(encoding="utf-8")
    assert "登录成功" in raw          # 中文不被转义成 \uXXXX
    assert "\n  " in raw              # indent=2


def test_export_json_empty_list(tmp_path):
    out = tmp_path / "empty.json"
    tg.export_to_json([], str(out))
    assert json.loads(out.read_text(encoding="utf-8")) == []


# ---------- export_to_csv ----------

def test_export_csv_writes_bom_header_and_rows(tmp_path):
    cases = [
        {"id": "TC001", "title": "登录成功", "priority": "P0"},
        {"id": "TC002", "title": "密码错误", "priority": "P1"},
    ]
    out = tmp_path / "cases.csv"
    tg.export_to_csv(cases, str(out))

    raw = out.read_bytes()
    assert raw[:3] == b"\xef\xbb\xbf"  # utf-8-sig BOM，Excel 打开不乱码

    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    assert len(rows) == 2
    assert rows[0]["id"] == "TC001"
    assert rows[1]["priority"] == "P1"


def test_export_csv_empty_list_does_not_write_file(tmp_path, capsys):
    out = tmp_path / "empty.csv"
    tg.export_to_csv([], str(out))
    assert not out.exists()
    assert "没有可导出" in capsys.readouterr().out
