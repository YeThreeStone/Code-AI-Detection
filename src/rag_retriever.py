# src/rag_retriever.py
from typing import List, Dict

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

from src.rule_loader import load_rules_from_md
import os
import dashscope
from dashscope import TextEmbedding
from dotenv import load_dotenv

load_dotenv()

dashscope.api_key = os.getenv("QWEN_API_KEY")

class QwenEmbedding:
    def embed_text(self, text: str) -> list:
        response = TextEmbedding.call(
            model='text-embedding-v1',
            input=text
        )
        if response.status_code == 200:
            return response.output['embeddings'][0]['embedding']
        else:
            raise Exception(f"Embedding 调用失败: {response.message}")

class RuleRetriever:
    def __init__(self, standard_file: str):
        self.rules = load_rules_from_md(standard_file)
        self.embedding_model = QwenEmbedding()
        self.rule_embeddings = []
        self._build_embeddings()

    def _build_embeddings(self):
        for rule in self.rules:
            text = f"{rule['title']}: {rule['description']} 示例: {rule['example_bad']}"
            emb = self.embedding_model.embed_text(text)
            self.rule_embeddings.append(emb)

    def retrieve(self, query: str, k: int = 2) -> list:
        query_emb = self.embedding_model.embed_text(query)
        sims = []
        for i, emb in enumerate(self.rule_embeddings):
            sim = cosine_similarity([query_emb], [emb])[0][0]
            sims.append((sim, i))
        sims.sort(reverse=True, key=lambda x: x[0])
        top_k = sims[:k]
        return [self.rules[i] for _, i in top_k]