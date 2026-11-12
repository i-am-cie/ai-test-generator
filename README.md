# AI Test Generator

A local web tool that turns source code or plain-language requirements into software test cases using an LLM served by [Ollama](https://ollama.com/) — fully offline, no API key.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![LLM](https://img.shields.io/badge/LLM-Ollama-black)
![Offline](https://img.shields.io/badge/Offline-100%25-success)
![Tests](https://img.shields.io/badge/tests-8%20passed-success)

## What it does

- **Code → unit tests**: paste a function in Python, JavaScript, Java or Go and get a pytest-oriented unit test suite with normal, boundary and exception cases.
- **Requirement → test plan**: describe a feature (e.g. a login flow) and get a structured test plan with scenarios, cases and P0/P1/P2 priorities.
- **Edge cases**: describe an input field or feature and get a table of boundary, special-character and concurrency cases.
- **Structured export (CLI)**: generate a JSON array of test cases and save it as JSON or CSV for import into a test management tool.
- **Local only**: prompts and results stay on your machine; the browser UI talks only to your local Flask server and your local Ollama instance.

## Requirements

- [Ollama](https://ollama.com/) installed and running locally.
- A chat model, default `qwen2.5:7b` (see [Configuration](#configuration)). Any instruction-following model that fits your hardware should work, e.g. `qwen2.5:3b` on small machines.
- Python 3.9 or newer.

## Install

```bash
git clone https://github.com/i-am-cie/ai-test-generator.git
cd ai-test-generator
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open <http://localhost:5000> in your browser. The Flask development server listens on port `5000`.

## Run tests

The repository ships with a pytest suite under `tests/` that covers the structured-case JSON parsing and the JSON/CSV export. The Ollama call is mocked, so the suite does **not** require Ollama to be running or the `ollama` package to be installed.

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

## Usage

1. Make sure Ollama is running and the model is pulled: `ollama pull qwen2.5:7b`.
2. Open <http://localhost:5000>.
3. Pick a tab:
   - **代码转测试 / Code → tests** — choose the language, paste a function, click **生成单元测试**.
   - **需求转用例 / Requirement → cases** — paste a feature description, click **生成测试计划**.
   - **边界用例 / Edge cases** — describe an input or feature, click **生成边界用例**.
4. Wait for the spinner to finish; the generated Markdown is shown in the result panel.
5. To get an importable file instead, use the command-line mode:

```bash
# unit tests for a snippet
python test_generator.py --code "def add(a, b): return a + b" --language python

# test plan from a requirement
python test_generator.py --requirement "用户登录功能：支持账号密码登录"

# structured cases exported as CSV
python test_generator.py --export-json "用户登录功能" --format csv --output login_cases.csv
```

> Note: the JSON/CSV export exists only in the command-line interface; the web page shows text results.

## Configuration

There is no configuration file; settings live in the source:

| Setting | Where | Default | Meaning |
| --- | --- | --- | --- |
| Model | `MODEL` in `test_generator.py` | `qwen2.5:7b` | Ollama model used for every prompt. |
| Ollama endpoint | `OLLAMA_HOST` environment variable | `http://127.0.0.1:11434` | Read automatically by the `ollama` Python client; set it if Ollama runs on another host or port. |
| Web port | `app.run(..., port=5000)` in `app.py` | `5000` | Port of the Flask development server. |

Examples:

```bash
# use a smaller model: edit MODEL in test_generator.py
# point the client at a remote Ollama instance
export OLLAMA_HOST=http://192.168.1.20:11434   # Windows PowerShell: $env:OLLAMA_HOST="..."
```

## How it works

1. The browser posts the input, the generation type and the language to `POST /api/generate`.
2. `app.py` dispatches to one of the prompt builders in `test_generator.py` (`generate_unit_tests`, `generate_test_plan`, `generate_edge_cases`).
3. Each builder fills a Chinese prompt template and calls `ollama.chat(model=MODEL, ...)`.
4. The raw Markdown returned by the model is passed back to the page and displayed as text.
5. For structured export, `generate_structured_test_cases` asks the model for a JSON array, extracts the first `[ ... ]` block and writes it to disk as JSON or CSV.

The repository's own pytest suite covers only this parsing/export code; it does **not** execute or validate the tests that the model generates.

## Limitations

- **Quality depends on the model.** A 7B model can produce incomplete, duplicated or non-compiling test code; always review and run the output yourself.
- **Hallucination is possible.** Generated cases, steps and expected results may look plausible but not match your actual system.
- **No verification.** The tool never executes the generated tests and cannot tell whether they pass.
- **Text only.** Inputs are plain text pasted into the UI/CLI; there is no repository scanning, file upload or IDE integration.
- **Single user, no authentication.** The Flask app runs with `debug=True` and is meant for `localhost` use only.
- **Chinese prompts.** Prompts are written in Chinese, so output is usually Chinese even though this README is English.

## License

MIT © 2026 i-am-cie — see [LICENSE](LICENSE).

## 中文说明

本项目是一个基于本地 Ollama 大模型的测试用例生成工具，支持「代码转单元测试」「需求转测试计划」「边界用例生成」三种模式，并提供命令行 JSON/CSV 结构化导出。所有数据都留在本机，无需 API Key。使用前请先安装并启动 Ollama、拉取默认模型 `qwen2.5:7b`，然后 `pip install -r requirements.txt` 并 `python app.py`，浏览器打开 http://localhost:5000 即可。仓库自带 pytest 单元测试（`tests/` 目录），覆盖结构化用例解析与 JSON/CSV 导出逻辑，大模型调用已打桩，运行测试无需启动 Ollama：`pip install -r requirements-dev.txt` 后 `python -m pytest tests/ -v`。注意：模型生成结果需要人工复核，工具本身不执行测试。
