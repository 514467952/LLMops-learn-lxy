#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/7/29 09:47
@Author : liuxiaoyu
@File : 1.多LLM链选择示例.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.创建提示模板，并定义默认模型及可切换的模型
# 三个模型共用同一个 Moonshot API 地址和 API Key，只需修改 model 参数。
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(
    model="moonshot-v1-8k",
    base_url="https://api.moonshot.cn/v1",
    temperature=0.7,  # 默认温度；没有传入运行时配置时使用该值
    timeout=60,
).configurable_alternatives(
    ConfigurableField(id="llm"),
    default_key="moonshot_8k",
    moonshot_32k=ChatOpenAI(
        model="moonshot-v1-32k",
        base_url="https://api.moonshot.cn/v1",
        temperature=0.7,
        timeout=60,
    ),
    moonshot_128k=ChatOpenAI(
        model="moonshot-v1-128k",
        base_url="https://api.moonshot.cn/v1",
        temperature=0.7,
        timeout=60,
    ),
)

# 2.构建链应用
chain = prompt | llm | StrOutputParser()

# 3.调用链并传递配置信息
# 可选值：
# - moonshot_8k（默认）
# - moonshot_32k
# - moonshot_128k
content = chain.invoke(
    {"query": "你好，你是什么模型呢?"},
    config={"configurable": {"llm": "moonshot_32k"}},
)
print(content)
