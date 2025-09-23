# src/rule_loader.py
import re
from typing import List, Dict

def load_rules_from_md(file_path: str) -> List[Dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    rules = []
    sections = re.split(r'^## ', content, flags=re.MULTILINE)[1:]

    for sec in sections:
        lines = sec.strip().split('\n')
        title_line = lines[0].strip()
        rule_id = title_line.split(':')[0].strip()
        title = title_line.split(':', 1)[1].strip()

        description = ""
        example_bad = ""
        suggestion = ""

        for line in lines[1:]:
            if line.startswith("- **描述**"):
                description = line.split(":", 1)[1].strip()
            elif line.startswith("- **示例（错误）**"):
                example_bad = line.split(":", 1)[1].strip()
            elif line.startswith("- **建议**"):
                suggestion = line.split(":", 1)[1].strip()

        rules.append({
            "rule_id": rule_id,
            "title": title,
            "description": description,
            "example_bad": example_bad,
            "suggestion": suggestion
        })

    return rules