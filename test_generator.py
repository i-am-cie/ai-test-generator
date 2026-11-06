#!/usr/bin/env python3
"""
ai-test-generator: Generate test cases using local LLMs via Ollama.

Usage:
    python test_generator.py --code "def add(a, b): return a + b"
    python test_generator.py --requirement "用户登录功能"
"""

import argparse
import ollama

MODEL = "qwen2.5:7b"


def generate_unit_tests(code: str, language: str = "python") -> str:
    """Generate unit tests for given code."""
    prompt = f"""你是一个资深软件测试工程师。请为以下{language}代码生成完整的单元测试用例。

代码：
```{language}
{code}
```

请生成包含以下内容的测试用例：
1. 正常输入场景（至少3个用例）
2. 边界值测试（空值、最大值、最小值等）
3. 异常输入测试（错误类型、非法参数等）
4. 性能相关测试点（如适用）

输出格式：
- 用Markdown格式，每个测试用例包含：编号、标题、前置条件、测试步骤、预期结果
- 同时给出可直接运行的测试代码（使用pytest）
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def generate_test_plan(requirement: str, test_type: str = "功能测试") -> str:
    """Generate a test plan from a requirement description."""
    prompt = f"""你是一个资深软件测试工程师。请为以下需求生成完整的{test_type}测试计划。

需求描述：
{requirement}

请生成：
1. 测试范围和目标
2. 测试场景列表（至少10个），包括：
   - 正向场景
   - 反向/异常场景
   - 边界场景
   - 兼容性场景
3. 每个场景的具体测试用例（前置条件、步骤、预期结果）
4. 优先级划分（P0/P1/P2）
5. 风险点和注意事项

用清晰的Markdown格式输出。
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def generate_edge_cases(input_desc: str) -> str:
    """Generate edge cases for a given input field or function."""
    prompt = f"""你是一个测试专家。请为以下输入/功能生成边界值测试用例。

描述：
{input_desc}

请列出所有可能的边界情况，包括：
- 最小值、最大值、空值
- 特殊字符、超长字符串
- 类型错误、格式错误
- 并发、重复提交
- 网络异常、超时

用表格形式输出：用例编号 | 测试场景 | 输入数据 | 预期结果 | 优先级
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def main():
    parser = argparse.ArgumentParser(description="AI Test Generator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--code", type=str, help="代码片段，生成单元测试")
    group.add_argument("--requirement", type=str, help="需求描述，生成测试计划")
    group.add_argument("--edge", type=str, help="输入描述，生成边界用例")
    
    parser.add_argument("--language", type=str, default="python", help="编程语言（默认python）")
    
    args = parser.parse_args()
    
    if args.code:
        print("生成单元测试中...\n")
        print(generate_unit_tests(args.code, args.language))
    elif args.requirement:
        print("生成测试计划中...\n")
        print(generate_test_plan(args.requirement))
    elif args.edge:
        print("生成边界用例中...\n")
        print(generate_edge_cases(args.edge))


if __name__ == "__main__":
    main()
