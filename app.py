#!/usr/bin/env python3
"""
ai-test-generator Web UI (Flask)
"""

from flask import Flask, render_template_string, request, jsonify
from test_generator import generate_unit_tests, generate_test_plan, generate_edge_cases

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Test Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 30px; font-size: 2.5rem; }
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            margin-bottom: 20px;
        }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab {
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            background: #f0f0f0;
            border: none;
            font-size: 1rem;
            transition: all 0.3s;
        }
        .tab.active { background: #667eea; color: white; }
        textarea {
            width: 100%;
            min-height: 150px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            font-family: 'Courier New', monospace;
            resize: vertical;
            margin-bottom: 15px;
        }
        textarea:focus { outline: none; border-color: #667eea; }
        button.generate {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button.generate:hover { transform: translateY(-2px); }
        button.generate:disabled { opacity: 0.6; cursor: not-allowed; }
        .result {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            white-space: pre-wrap;
            display: none;
        }
        .result.show { display: block; }
        .loading { text-align: center; color: #667eea; display: none; }
        .loading.show { display: block; }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .lang-select { padding: 10px; border-radius: 8px; border: 2px solid #e0e0e0; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Test Generator</h1>
        
        <div class="card">
            <div class="tabs">
                <button class="tab active" onclick="switchTab('code')">代码转测试</button>
                <button class="tab" onclick="switchTab('requirement')">需求转用例</button>
                <button class="tab" onclick="switchTab('edge')">边界用例</button>
            </div>

            <div id="tab-code">
                <label>编程语言:</label>
                <select class="lang-select" id="language">
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="java">Java</option>
                    <option value="go">Go</option>
                </select>
                <textarea id="code-input" placeholder="粘贴你的函数代码...

def add(a, b):
    return a + b"></textarea>
                <button class="generate" onclick="generate('code')">生成单元测试</button>
            </div>

            <div id="tab-requirement" style="display:none">
                <textarea id="req-input" placeholder="描述你的需求...
例如：用户登录功能，支持账号密码登录，连续5次失败锁定账号30分钟"></textarea>
                <button class="generate" onclick="generate('requirement')">生成测试计划</button>
            </div>

            <div id="tab-edge" style="display:none">
                <textarea id="edge-input" placeholder="描述需要测试的输入或功能...
例如：用户注册时的手机号输入框"></textarea>
                <button class="generate" onclick="generate('edge')">生成边界用例</button>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AI 正在生成测试用例，请稍候...</p>
            </div>

            <div class="result" id="result"></div>
        </div>
    </div>

    <script>
        let currentTab = 'code';
        
        function switchTab(tab) {
            currentTab = tab;
            document.querySelectorAll('.tab').forEach((t, i) => {
                t.classList.remove('active');
            });
            event.target.classList.add('active');
            
            ['code', 'requirement', 'edge'].forEach(t => {
                document.getElementById('tab-' + t).style.display = t === tab ? 'block' : 'none';
            });
        }
        
        async function generate(type) {
            const inputMap = {
                code: document.getElementById('code-input').value,
                requirement: document.getElementById('req-input').value,
                edge: document.getElementById('edge-input').value
            };
            
            const input = inputMap[type];
            if (!input.trim()) {
                alert('请输入内容');
                return;
            }
            
            document.getElementById('loading').classList.add('show');
            document.getElementById('result').classList.remove('show');
            
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type, input, language: document.getElementById('language').value})
            });
            
            const data = await response.json();
            
            document.getElementById('loading').classList.remove('show');
            document.getElementById('result').textContent = data.result;
            document.getElementById('result').classList.add('show');
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json
    gen_type = data.get('type')
    user_input = data.get('input', '')
    language = data.get('language', 'python')
    
    if gen_type == 'code':
        result = generate_unit_tests(user_input, language)
    elif gen_type == 'requirement':
        result = generate_test_plan(user_input)
    elif gen_type == 'edge':
        result = generate_edge_cases(user_input)
    else:
        result = '未知的生成类型'
    
    return jsonify({'result': result})


if __name__ == '__main__':
    print("🚀 AI Test Generator 启动中...")
    print("📖 访问 http://localhost:5000")
    app.run(debug=True, port=5000)
