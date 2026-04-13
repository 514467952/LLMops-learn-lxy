#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/4/13 19:48
@Author : liuxiaoyu
@File : Model批处理.py
"""
import  dotenv
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


# 1. 编排prompt
prompt = ChatPromptTemplate.from_messages([
    ("system","你是OpenAI开发的聊天机器人，请回答用户的问题"),
    ("human","{query}")
]).partial(now=datetime.now())

# 2.创建大语言模型
llm = ChatOpenAI(
    model="kimi-k2-0905-preview",
    base_url="https://api.moonshot.cn/v1"
)

ai_message = llm.invoke(prompt.invoke({"query":"现在是几点，请讲一个程序员的冷笑话"}))

print(ai_message.type)
print("====================")
print(ai_message.content)
print("====================")
print(ai_message.name)

# 批处理是每一条单独处理
ai_messages = llm.batch([
    prompt.invoke({"query":"你好，你是?"}),
    prompt.invoke({"query":"请讲一个程序员的冷笑话"})
])

for ai_message in ai_messages:
    print(ai_message.content)
    print("===============")