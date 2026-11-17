#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/11/17 17:31
@Author : liuxiaoyu
@File : 2.Pinecone删除数据.py
"""
from pathlib import Path

import dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
INDEX_NAME = "llmops-siliconflow"
NAMESPACE = "dataset"
DOCUMENT_ID = "siliconflow-example-page-3"

env_config = dotenv.dotenv_values(ENV_FILE)
siliconflow_api_key = env_config.get("SILICONFLOW_API_KEY")
pinecone_api_key = env_config.get("PINECONE_API_KEY")

if not siliconflow_api_key:
    raise ValueError(f"未找到 SILICONFLOW_API_KEY，请在 {ENV_FILE} 中完成配置")

if not pinecone_api_key:
    raise ValueError(f"未找到 PINECONE_API_KEY，请在 {ENV_FILE} 中完成配置")

# 与写入示例使用相同的模型、索引和命名空间。
embedding = OpenAIEmbeddings(
    model="Qwen/Qwen3-Embedding-4B",
    api_key=siliconflow_api_key,
    base_url="https://api.siliconflow.cn/v1",
    dimensions=1536,
    check_embedding_ctx_length=False,
)
db = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embedding,
    namespace=NAMESPACE,
    pinecone_api_key=pinecone_api_key,
)

if __name__ == "__main__":
    # db.delete(ids=[DOCUMENT_ID], namespace=NAMESPACE)
    # print(f"已提交删除请求，索引: {INDEX_NAME}，命名空间: {NAMESPACE}，ID: {DOCUMENT_ID}")
    new_text = "我的狗喜欢唱歌，看起来非常开心"
    llmops_index = db.index
    # 更新向量时同步更新正文，set_metadata 会保留原有的 page 等其他字段。
    llmops_index.update(
        id="siliconflow-example-page-10",
        values=embedding.embed_documents([new_text])[0],
        set_metadata={"text": new_text},
        namespace=NAMESPACE,
    )
    print("已提交 siliconflow-example-page-10 的更新请求")
