#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/7/2 14:16
@Author : liuxiaoyu
@File : 摘要混合记忆组件示例.py
"""
from operator import itemgetter

import dotenv
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.chat_models.baidu_qianfan_endpoint import QianfanChatEndpoint
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

memory = ConversationSummaryBufferMemory(
    max_token_limit=300,
    return_messages=True,
    input_key="query",
    llm=ChatOpenAI(
        model="kimi-k2.6",
        base_url="https://api.moonshot.cn/v1",
        # 仅用于让 LangChain 估算消息 token 数，不会改变实际调用的 Kimi 模型
        tiktoken_model_name="gpt-3.5-turbo",
    ),
)

# 2.创建大语言模型
llm = ChatOpenAI(
    model="kimi-k2.6",
    base_url="https://api.moonshot.cn/v1",
    # 仅用于让 LangChain 估算消息 token 数，不会改变实际调用的 Kimi 模型
    tiktoken_model_name="gpt-3.5-turbo",
)

# 3.构建链应用
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
