# src/llm_analyzer.py
import requests
import os
from dotenv import load_dotenv
import textwrap
import json  # 确保导入 json

load_dotenv()

QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"


def analyze_code_with_qwen(code: str, relevant_rules: list) -> dict:
    try:
        rules_text = "\n".join([
            f"{r['rule_id']}: {r['title']} - {r['description']} "
            f"示例: {r['example_bad']} 建议: {r['suggestion']}"
            for r in relevant_rules
        ])

        prompt = textwrap.dedent(f"""
        你是一个资深Java代码审查专家，请根据以下编码规范检查代码：

        【编码规范】
        {rules_text}

        【待检测代码】
        <code>
        {code}
        </code>

        【任务要求】
        1. 判断是否存在违反上述规范的情况；
        2. 如果存在，指出具体问题、违反的规则ID和严重等级；
        3. 提供优化建议或修复代码示例；
        4. 输出格式为JSON：
        {{
          "issues": [
            {{
              "line": 2,
              "rule_id": "SEC-001",
              "message": "检测到硬编码数据库密码",
              "severity": "严重",
              "suggestion": "建议使用环境变量或配置中心管理密码..."
            }}
          ]
        }}
        不要输出其他内容。
        """).strip()

        headers = {
            "Authorization": f"Bearer {QWEN_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "qwen-turbo",
            "input": {
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            "parameters": {
                "result_format": "message"
            }
        }

        response = requests.post(QWEN_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if "output" in result and "choices" in result["output"]:
            content = result["output"]["choices"][0]["message"]["content"]
            return parse_json_response(content)  # ✅ 调用函数
        else:
            print("❌ API 响应格式异常:", result)
            return {"issues": []}

    except Exception as e:
        print(f"❌ 调用 Qwen API 失败: {e}")
        return {"issues": []}


# ✅ 确保这个函数定义在文件中，并且没有缩进错误
def parse_json_response(text: str) -> dict:
    """
    从大模型返回的文本中提取 JSON 结构
    """
    try:
        # 尝试直接解析
        if text.strip().startswith("{") and text.strip().endswith("}"):
            return json.loads(text.strip())

        # 尝试提取 { ... } 内容
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end != 0:
            json_str = text[start:end]
            return json.loads(json_str)
    except Exception as e:
        print(f"⚠️ JSON 解析失败: {e}")
        print(f"👉 原始输出:\n{text}")

    # 解析失败时返回空结果
    return {"issues": []}