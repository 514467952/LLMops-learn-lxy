#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/11/16 16:08
@Author : liuxiaoyu
@File : 1.faiss向量数据库使用示例.py
"""
from pathlib import Path

import dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
VECTOR_STORE_DIR = Path(__file__).resolve().parent / "vector-store"
env_config = dotenv.dotenv_values(ENV_FILE)
siliconflow_api_key = env_config.get("SILICONFLOW_API_KEY")

if not siliconflow_api_key:
    raise ValueError(f"未找到 SILICONFLOW_API_KEY，请在 {ENV_FILE} 中完成配置")

embedding = OpenAIEmbeddings(
    model="BAAI/bge-m3",
    api_key=siliconflow_api_key,
    base_url="https://api.siliconflow.cn/v1",
    check_embedding_ctx_length=False,
)

# db = FAISS.from_texts([
#     "笨笨是一只很喜欢睡觉的猫咪",
#     "我喜欢在夜晚听音乐,这让我感到放松.",
#     "猫咪在窗台上打盹,看起来非常可爱.",
#     "学习新技能是每个人都应该追求的目标.",
#     "我最喜欢的食物是意大利面,尤其是番茄酱的那种.",
#     "昨晚我做了一个奇怪的梦,梦见自己在太空飞行.",
#     "我的手机突然关机了,让我有些焦虑.",
#     "阅读是我每天都会做的事情,我觉得很充实.",
#     "他们一起计划了一次周末的野餐,希望天气能好.",
#     "我的狗喜欢追逐球,看起来非常开心."],
#     embedding,
#     relevance_score_fn=lambda distance: 1.0 / (1.0 + distance),
# )
#
# print(db.index.ntotal)
# print(db.similarity_search_with_relevance_scores("我养了一只猫,叫笨笨"))


# 过滤相似性搜索
texts: list[str] = [
    "笨笨是一只很喜欢睡觉的猫咪",
    "我喜欢在夜晚听音乐，这让我感到放松。",
    "猫咪在窗台上打盹，看起来非常可爱。",
    "学习新技能是每个人都应该追求的目标。",
    "我最喜欢的食物是意大利面，尤其是番茄酱的那种。",
    "昨晚我做了一个奇怪的梦，梦见自己在太空飞行。",
    "我的手机突然关机了，让我有些焦虑。",
    "阅读是我每天都会做的事情，我觉得很充实。",
    "他们一起计划了一次周末的野餐，希望天气能好。",
    "我的狗喜欢追逐球，看起来非常开心。",
]
metadatas: list[dict[str, int]] = [
    {"page": 1},
    {"page": 2},
    {"page": 3},
    {"page": 4},
    {"page": 5},
    {"page": 6},
    {"page": 7},
    {"page": 8},
    {"page": 9},
    {"page": 10},
]
db = FAISS.from_texts(texts, embedding, metadatas=metadatas)
# print(db.similarity_search_with_score(
#     "我养了一只猫,叫笨笨",
#     filter=lambda metadata: metadata["page"] > 5,
#     fetch_k=len(texts),
# ))

# 存储到本地文件
db.save_local(str(VECTOR_STORE_DIR))
new_db = FAISS.load_local(
    str(VECTOR_STORE_DIR),
    embedding,
    allow_dangerous_deserialization=True,
)
docs = new_db.similarity_search("我养了一只猫,叫笨笨")
print("保存目录:", VECTOR_STORE_DIR)
print("重新加载后的数量:", new_db.index.ntotal)
print("搜索结果:", docs)


# 删除指定数据
# print("删除前数量:", db.index.ntotal)
# delete_id = db.index_to_docstore_id[0]
# print("待删除数据:", db.get_by_ids([delete_id])[0].page_content)
# db.delete(ids=[delete_id])
# print("删除后数量:", db.index.ntotal)
# print("删除后按 ID 查询:", db.get_by_ids([delete_id]))
