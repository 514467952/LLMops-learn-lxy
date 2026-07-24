#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/7/24 14:25
@Author : liuxiaoyu
@File : bind函数使用技巧.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 加载.env文件里的环境变量，一般用于存储OPENAI_API_KEY等敏感配置
dotenv.load_dotenv()

# 构造聊天提示词模板
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "你正在执行一项测试，请重复用户传递的内容，除了重复其他均不要操作"
    ),
    # 预留query作为用户输入的占位符
    ("human", "{query}")
])

# 初始化GPT-4o模型实例
llm = ChatOpenAI(
    model="kimi-k2.6",
    base_url="https://api.moonshot.cn/v1",
    extra_body={
        "thinking": {
            "type": "disabled"
        }
    },
    timeout=60
)

# 编排调用链：提示词传入→绑定停止词"world"的大模型→输出转字符串
chain = prompt | llm.bind(stop="world") | StrOutputParser()

# 传入用户输入"Hello world"执行调用
content = chain.invoke({"query": "xxxxx，hello world"})

# 打印结果
print(content)