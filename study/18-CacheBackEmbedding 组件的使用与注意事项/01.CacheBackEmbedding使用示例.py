#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/8/10 11:04
@Author : liuxiaoyu
@File : 01.CacheBackEmbedding使用示例.py

使用硅基流动的 BAAI/bge-m3 模型演示 CacheBackedEmbeddings 本地缓存。
第一次处理某段文本时会请求远程 Embedding 接口；以后再次处理完全相同的
文本时会优先读取本地缓存，从而减少 API 调用次数、费用和等待时间。
"""
from pathlib import Path

import dotenv
import numpy as np
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_openai import OpenAIEmbeddings
from numpy.linalg import norm


# --------------------------- 基础配置 ---------------------------

# 当前文件位于 study/课程目录/ 下，向上两级得到项目根目录。
# 使用绝对路径定位配置和缓存，可避免从不同工作目录启动脚本时找错文件。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"
CACHE_DIR = Path(__file__).resolve().parent / "cache"

# 从被 Git 忽略的 .env 文件读取密钥，不要在 Python 文件中硬编码真实 Key。
# .env 中需要包含：SILICONFLOW_API_KEY=你的硅基流动_API_Key
env_config = dotenv.dotenv_values(ENV_FILE)
siliconflow_api_key = env_config.get("SILICONFLOW_API_KEY")

if not siliconflow_api_key:
    raise ValueError(
        f"未找到 SILICONFLOW_API_KEY，请在 {ENV_FILE} 中完成配置"
    )


SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1"
EMBEDDING_MODEL = "BAAI/bge-m3"

# 缓存命名空间必须随“服务商或模型”变化而变化。
# 如果以后更换模型却沿用同一个命名空间，可能错误地读到旧模型生成的向量。
# 这里不用原始模型名中的斜杠，避免 LocalFileStore 将其解释成子目录。
CACHE_NAMESPACE = "siliconflow-bge-m3-"


def cosine_similarity(vector1: list, vector2: list) -> float:
    """计算两个向量的余弦相似度，结果越接近 1 表示语义越相似。"""
    # 1. 计算两个向量的内积（点积）。
    dot_product = np.dot(vector1, vector2)

    # 2. 计算两个向量各自的长度（L2 范数）。
    norm_vec1 = norm(vector1)
    norm_vec2 = norm(vector2)

    # 3. 点积除以两个向量长度的乘积，得到余弦相似度。
    return float(dot_product / (norm_vec1 * norm_vec2))


def main() -> None:
    """创建嵌入客户端和本地缓存，并演示查询、文档向量化。"""
    # 硅基流动兼容 OpenAI 的 Embeddings 接口，因此可以继续使用
    # LangChain 的 OpenAIEmbeddings，只需替换模型、密钥和 base_url。
    underlying_embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=siliconflow_api_key,
        base_url=SILICONFLOW_BASE_URL,
        # BGE-M3 不是 OpenAI 官方模型，关闭 OpenAI 专用的 tiktoken
        # 长度检查，避免按错误的模型规则预处理输入。
        check_embedding_ctx_length=False,
    )

    # LocalFileStore 会把序列化后的向量保存在当前课程目录的 cache/ 中。
    # 该目录属于运行缓存，已加入 .gitignore，不需要提交到 Git。
    cache_store = LocalFileStore(CACHE_DIR)

    # CacheBackedEmbeddings 是 underlying_embeddings 的缓存包装器：
    # - 文档向量默认写入并读取 document_embedding_cache；
    # - query_embedding_cache=True 表示查询向量也复用同一个缓存；
    # - namespace 隔离不同服务商或模型产生的缓存；
    # - sha256 把原始文本转换成固定长度的安全文件名。
    embeddings_with_cache = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings=underlying_embeddings,
        document_embedding_cache=cache_store,
        namespace=CACHE_NAMESPACE,
        query_embedding_cache=True,
        key_encoder="sha256",
    )

    # 第一次运行会请求硅基流动；再次运行相同文本时会读取本地缓存。
    query_vector = embeddings_with_cache.embed_query(
        "你好，我是慕小课，我喜欢打篮球"
    )

    # 批量生成文档向量。只有尚未缓存的文本才会调用远程接口。
    documents_vector = embeddings_with_cache.embed_documents([
        "你好，我是慕小课，我喜欢打篮球",
        "这个喜欢打篮球的人叫慕小课",
        "求知若渴，虚心若愚",
    ])

    # 完整向量较长，只显示前 5 项、向量维度和文档数量。
    print("查询向量前5项:", query_vector[:5])
    print("查询向量维度:", len(query_vector))
    print("文档向量数量:", len(documents_vector))
    print("缓存目录:", CACHE_DIR)

    # 前两句话语义接近，理论上相似度高于第一句和第三句。
    print(
        "vector1与vector2的余弦相似度:",
        cosine_similarity(documents_vector[0], documents_vector[1]),
    )
    print(
        "vector1与vector3的余弦相似度:",
        cosine_similarity(documents_vector[0], documents_vector[2]),
    )


if __name__ == "__main__":
    main()
