"""
@Time : 2026/11/17 17:02
@Author : liuxiaoyu
@File : 1.Pinecone向量数据库使用示例.py
"""
import time
from pathlib import Path

import dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# 根据脚本位置找到项目根目录的 .env，避免运行目录不同导致找不到密钥。
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
# 使用接收外部向量的索引；原 llmops 索引绑定了 Pinecone 内置的嵌入模型。
INDEX_NAME = "llmops-siliconflow"
# namespace 隔离同一索引中的数据，写入和搜索时应使用同一个值。
NAMESPACE = "dataset"
EMBEDDING_DIMENSIONS = 1536
env_config = dotenv.dotenv_values(ENV_FILE)
siliconflow_api_key = env_config.get("SILICONFLOW_API_KEY")
pinecone_api_key = env_config.get("PINECONE_API_KEY")

if not siliconflow_api_key:
    raise ValueError(f"未找到 SILICONFLOW_API_KEY，请在 {ENV_FILE} 中完成配置")

if not pinecone_api_key:
    raise ValueError(f"未找到 PINECONE_API_KEY，请在 {ENV_FILE} 中完成配置")

# 硅基流动提供 OpenAI 兼容接口，因此可以继续使用 OpenAIEmbeddings。
# 文档和查询必须使用相同模型，输出维度也必须与 Pinecone 索引一致。
embedding = OpenAIEmbeddings(
    model="Qwen/Qwen3-Embedding-4B",
    api_key=siliconflow_api_key,
    base_url="https://api.siliconflow.cn/v1",
    dimensions=EMBEDDING_DIMENSIONS,
    # 直接发送文本，避免按 OpenAI 模型的分词规则预处理 Qwen 的输入。
    check_embedding_ctx_length=False,
)

# 每条文本与下方同一位置的 metadata 对应，两个列表的长度必须一致。
texts: list = [
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
# 元数据随文档保存，可在检索时通过 page、account_id 等字段过滤。
metadatas: list = [
    {"page": 1},
    {"page": 2},
    {"page": 3},
    {"page": 4},
    {"page": 5},
    {"page": 6, "account_id": 1},
    {"page": 7},
    {"page": 8},
    {"page": 9},
    {"page": 10},
]
# 首次运行创建云端索引，后续运行复用；最多等待 60 秒直到新索引就绪。
pc = Pinecone(api_key=pinecone_api_key)
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=EMBEDDING_DIMENSIONS,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        timeout=60,
    )

# 写入前检查已有索引的配置，提前发现向量维度或相似度算法不匹配的问题。
index_info = pc.describe_index(INDEX_NAME)
if index_info.dimension != EMBEDDING_DIMENSIONS or index_info.metric != "cosine":
    raise ValueError(f"索引 {INDEX_NAME} 必须使用 {EMBEDDING_DIMENSIONS} 维和 cosine 度量")

# 通过索引地址连接数据接口，再由 LangChain 组织向量化、写入和搜索。
index = pc.Index(host=index_info.host)
db = PineconeVectorStore(index=index, embedding=embedding, namespace=NAMESPACE)
# 固定 ID 让重复运行更新同一批文档；修改文本或元数据时也会覆盖原记录。
ids = [f"siliconflow-example-page-{metadata['page']}" for metadata in metadatas]

# 首次使用空索引时，取消下方写入代码的注释；已有数据时可以保持注释，只做查询。
# add_texts 先调用硅基流动生成向量，再把向量、文本和元数据写入 Pinecone。
# async_req=False 等待写入请求返回，但不代表数据已经能被查询到。
# db.add_texts(
#     texts,
#     metadatas=metadatas,
#     ids=ids,
#     async_req=False,
# )
# print(f"已写入 {len(ids)} 条数据，索引: {INDEX_NAME}，命名空间: {NAMESPACE}")

# Pinecone 的数据可见性存在延迟，轮询确认这批 ID 都能被读取。
# monotonic 不受系统时间调整影响；若未执行过写入，这里会等待 30 秒后报错。
deadline = time.monotonic() + 30
while len(index.fetch(ids=ids, namespace=NAMESPACE).vectors) < len(ids):
    if time.monotonic() >= deadline:
        raise TimeoutError("Pinecone 已接受写入，但数据在 30 秒内仍未全部可见")
    time.sleep(1)

# 查询文本也由硅基流动生成向量，默认返回最相关的 4 条文档。
# 结果是 (Document, 相关度分数)，分数映射到 0～1，越大越相关。
query = "我养了一只猫，叫笨笨"
print(db.similarity_search_with_relevance_scores(query, filter={"$or": [{"page": 5},{"account_id": 1}]}))
