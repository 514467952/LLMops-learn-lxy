#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/4/22 10:20
@Author : liuxiaoyu
@File : LCEL简化表达.py
"""
from typing import Any
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(
    model="kimi-k2-0905-preview",
    base_url="https://api.moonshot.cn/v1"
)
parser = StrOutputParser()

# LCEL表达式构建链
chain = prompt | llm | parser

print(chain.invoke({"query": "你好，你是？"}))