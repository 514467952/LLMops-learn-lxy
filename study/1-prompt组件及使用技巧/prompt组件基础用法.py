#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/4/9 19:50
@Author : liuxiaoyu
@File : prompt组件基础用法.py
"""
from datetime import datetime

from langchain_core.messages import AIMessage
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
MessagesPlaceholder,
)


prompt = PromptTemplate.from_template("请讲一个关于{subject}的冷笑话")

print(prompt.format(subject="喜剧演员"))
prompt_value = prompt.invoke({
    "subject" : "喜剧演员"
})

print(prompt_value.to_string())
print(prompt_value.to_messages())


print("============================")
chat_prompt = ChatPromptTemplate.from_messages([
    ("system","你是openAI开发的聊天机器人，请根据用户的提问进行回复，当前时间为:{now}"),
    # 有时候可能还有其他消息，但是不确定，使用消息占位符
    MessagesPlaceholder("chat_history"),
    #
    HumanMessagePromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
]).partial(now=datetime.now)

chat_prompt_value = chat_prompt.invoke({
    "chat_history" : [
        ("human","11111"),
        AIMessage("你好，我是chatGPT，有什么可以帮到你的")

    ],
    "subject": "程序员",
})

print(chat_prompt_value)
print(chat_prompt_value.to_string())
