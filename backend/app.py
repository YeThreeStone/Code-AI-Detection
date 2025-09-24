# backend/app.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import json

# 添加项目根目录到路径
import sys
sys.path.append(".")

from src.llm_analyzer import analyze_code_with_qwen
from src.rag_retriever import RuleRetriever

app = FastAPI(title="代码规范智能检测 API")

# 允许前端跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请改为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化规则检索器（启动时加载）
retriever = RuleRetriever("../config/coding_standards.md")

@app.post("/api/detect")
async def detect_code_issues(
    file: UploadFile = File(None),
    code: str = Form(None)
):
    # 读取代码
    if file:
        content = await file.read()
        code_text = content.decode("utf-8")
    elif code:
        code_text = code.strip()
    else:
        return {"error": "请提供代码文件或粘贴代码"}

    # 检索相关规则
    relevant_rules = retriever.retrieve(code_text, k=3)

    # 调用大模型分析
    result = analyze_code_with_qwen(code_text, relevant_rules)

    return {
        "success": True,
        "data": result
    }