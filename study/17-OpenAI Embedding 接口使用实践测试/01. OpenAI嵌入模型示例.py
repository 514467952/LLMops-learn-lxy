#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/8/7 10:48
@Author : liuxiaoyu
@File : 01. OpenAI嵌入模型示例.py

使用硅基流动提供的 OpenAI 兼容接口调用 BGE-M3 嵌入模型。
嵌入模型会把文本转换成数值向量，语义越接近的文本，其向量越相似。
"""
from pathlib import Path

import dotenv
import numpy as np
from langchain_openai import OpenAIEmbeddings
from numpy.linalg import norm


# 当前脚本位于 study/课程目录/ 下，向上两级就是项目根目录。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

# 密钥只保存在项目根目录的 .env 中，避免把真实密钥提交到代码仓库。
# 请先在 .env 中增加一行：
# SILICONFLOW_API_KEY=你的硅基流动_API_Key
env_config = dotenv.dotenv_values(ENV_FILE)
siliconflow_api_key = env_config.get("SILICONFLOW_API_KEY")

if not siliconflow_api_key:
    raise ValueError(
        f"未找到 SILICONFLOW_API_KEY，请在 {ENV_FILE} 中完成配置"
    )


# 硅基流动提供与 OpenAI SDK 兼容的 Embeddings 接口，所以仍然可以使用
# LangChain 的 OpenAIEmbeddings 类，只需替换 API 地址、密钥和模型名称。
SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1"
EMBEDDING_MODEL = "BAAI/bge-m3"


def cosine_similarity(vec1: list, vec2: list) -> float:
    """计算两个向量的余弦相似度，结果越接近 1 表示语义越相似。"""
    # 1. 计算两个向量的点积。
    dot_product = np.dot(vec1, vec2)

    # 2. 计算两个向量各自的长度（L2 范数）。
    vec1_norm = norm(vec1)
    vec2_norm = norm(vec2)

    # 3. 点积除以两个向量长度的乘积，得到余弦相似度。
    return float(dot_product / (vec1_norm * vec2_norm))


# 1. 创建文本嵌入客户端。
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    api_key=siliconflow_api_key,
    base_url=SILICONFLOW_BASE_URL,
    # 关闭 OpenAI 专用的 tiktoken 长度检查，避免它按 OpenAI 模型规则
    # 预处理 BGE-M3 的输入；输入长度限制交给硅基流动接口处理。
    check_embedding_ctx_length=False,
)

# 2. 把一条查询文本转换成向量。
query_vector = embeddings.embed_query("我叫慕小课，我喜欢打篮球")

# 完整向量很长，这里只展示前 5 个数值以及总维度。
print("查询向量前5项:", query_vector[:5])
print("查询向量维度:", len(query_vector))

# 3. 批量把文档列表转换成向量；返回结果与输入文本顺序一一对应。
documents_vector = embeddings.embed_documents([
    "我叫慕小课，我喜欢打篮球",
    "这个喜欢打篮球的人叫慕小课",
    "求知若渴，虚心若愚"
])
print("文档向量数量:", len(documents_vector))

# 4. 比较文档之间的语义相似度。
# 前两句话表达的含义接近，理论上相似度会高于第一句和第三句。
print("向量1和向量2的相似度:", cosine_similarity(documents_vector[0], documents_vector[1]))
print("向量1和向量3的相似度:", cosine_similarity(documents_vector[0], documents_vector[2]))
