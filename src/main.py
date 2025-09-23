
## ▶️ 5. `src/main.py` - 主程序

# src/main.py
from src.rag_retriever import RuleRetriever
from src.llm_analyzer import analyze_code_with_qwen
import os

def read_code_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    # 初始化
    retriever = RuleRetriever("../config/coding_standards.md")
    code = read_code_file("../test_code.java")
    print("🔍 正在检测代码...\n")

    # RAG 检索相关规则
    relevant_rules = retriever.retrieve(code, k=3)
    print(f"📌 检索到 {len(relevant_rules)} 条相关规范:")
    for r in relevant_rules:
        print(f"   - {r['rule_id']}: {r['title']}")
    print()
  
    # 调用大模型分析
    result = analyze_code_with_qwen(code, relevant_rules)

    # 输出结果
    print("✅ 检测完成，发现的问题：")
    if not result["issues"]:
        print("   没有发现违反规范的问题！")
    else:
        for issue in result["issues"]:
            print(f"   🔴 [{issue.get('rule_id', 'N/A')}] {issue['message']}")
            print(f"      建议: {issue['suggestion']}")
            print(f"      严重等级: {issue['severity']}")

if __name__ == "__main__":
    main()