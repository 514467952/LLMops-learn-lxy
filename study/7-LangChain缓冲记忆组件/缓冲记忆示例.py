#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/7/2 11:24
@Author : liuxiaoyu
@File : 缓冲记忆示例.py
"""
from operator import itemgetter

import dotenv
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.创建提示模板&记忆
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAI开发的聊天机器人，请根据对应的上下文回复用户问题"),
    MessagesPlaceholder("history"),  # 需要的history其实是一个列表
    ("human", "{query}"),
])

# input_key 表示输入字典中哪个字段是用户输入，保存记忆时会用它作为 Human 消息
memory = ConversationBufferWindowMemory(
    return_messages=True,
    input_key="query",
    k=2
)

# 2.创建大语言模型
llm = ChatOpenAI(
    model="kimi-k2.6",
    base_url="https://api.moonshot.cn/v1"
)

# 3.构建链应用
# RunnablePassthrough.assign 会保留原始输入，并额外添加 history 字段
# RunnableLambda 将 memory.load_memory_variables 包装成可运行对象
# memory.load_memory_variables 会返回类似 {"history": [...]} 的字典
# itemgetter("history") 用来从字典中取出 history 对话历史
chain = RunnablePassthrough.assign(
    history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
) | prompt | llm | StrOutputParser()

# 4.死循环构建对话命令行
while True:
    query = input("Human: ")

    if query == "q":
        exit(0)

    chain_input = {"query": query, "language": "中文"}

    response = chain.stream(chain_input)
    print("AI: ", flush=True, end="")
    output = ""
    for chunk in response:
        output += chunk
        print(chunk, flush=True, end="")
    memory.save_context(chain_input, {"output": output})
    print("")
    print("history: ", memory.load_memory_variables({}))
