# AI Test Generator

AI 驱动的测试用例生成工具，基于本地大模型（Ollama），完全离线运行，无需 API Key。

## ✨ 功能特性

- **代码转测试**：粘贴函数代码，自动生成单元测试用例
- **需求转用例**：输入功能描述，生成完整测试计划
- **多测试类型**：正常场景、边界值、异常输入、并发场景
- **结构化导出**：一键导出 JSON / CSV 格式，可直接导入测试管理工具
- **Web 界面**：简洁的浏览器操作界面
- **完全本地**：所有数据都在你的电脑上，隐私安全

## 🚀 快速开始

### 前置要求

1. 安装 [Ollama](https://ollama.com/)
2. 拉取模型：
   ```bash
   ollama pull qwen2.5:7b
   ```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动 Web 界面

```bash
python app.py
```

打开浏览器访问 http://localhost:5000

### 命令行模式

```bash
# 从代码生成测试
python test_generator.py --code "def add(a, b): return a + b"

# 从需求生成测试用例
python test_generator.py --requirement "用户登录功能：支持账号密码登录"

# 生成结构化用例并导出为CSV
python test_generator.py --export-json "用户登录功能" --format csv --output login_cases.csv
```

## 📦 项目结构

```
ai-test-generator/
├── app.py              # Flask Web 界面
├── test_generator.py   # 核心测试生成逻辑
├── requirements.txt    # Python 依赖
└── README.md
```

## 📤 导出格式

### JSON 格式
```json
[
  {
    "id": "TC001",
    "title": "正确账号密码登录",
    "priority": "P0",
    "precondition": "用户已注册",
    "steps": "输入正确账号;输入正确密码;点击登录",
    "expected": "登录成功，跳转到首页",
    "type": "正常"
  }
]
```

### CSV 格式
可直接用 Excel 打开，导入禅道、Jira 等测试管理工具。

## 🛠️ 技术栈

- **后端**：Python + Flask
- **LLM**：Ollama (Qwen2.5)
- **前端**：HTML + 原生 JS

## 📝 License

MIT
