#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/4/13 20:22
@Author : liuxiaoyu
@File : JsonOutput使用.py
"""
from dataclasses import Field

import  dotenv
from datetime import datetime

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 创建一个json的数据结构，用于高速大模型这个json长什么样
class Joke(BaseModel):
    # 冷笑话
    joke: str = Field(description="回答用户的冷笑话")
    # 冷笑话的笑点
    punchline: str = Field(description="这个冷笑话的笑点")

parser = JsonOutputParser(pydantic_object=Joke)

# 2.构建一个提示模版，使用 partial_variables 预先绑定 format_instructions
prompt = ChatPromptTemplate.from_template(
    "回答用户的问题。\n{format_instructions}\n{query}\n",
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# 3. 构建一个大语言模型
llm = ChatOpenAI(
    model="kimi-k2-0905-preview",
    base_url="https://api.moonshot.cn/v1"
)

# 4.构建提示词并进行解析
joke = parser.invoke(
    llm.invoke(
        prompt.invoke({"query":"请讲一个关于程序员的冷笑话"})
    )
)

print(joke)

