#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/4/13 20:17
@Author : liuxiaoyu
@File : StrOutput使用.py
"""
import  dotenv
from datetime import datetime

from langchain_core.output_parsers import StrOutputParser
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

# 创建字符串输出解析器
parser = StrOutputParser()

# 调用大语言模型生成结果并解析
content = parser.invoke(llm.invoke(prompt.invoke({"query":"你是，你好？"})))

print(content)