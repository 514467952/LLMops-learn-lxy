#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/4/22 10:07
@Author : liuxiaoyu
@File : 手写chain实现简单版本.py
"""
from typing import Any
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1. 构建组件
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(
    model="kimi-k2-0905-preview",
    base_url="https://api.moonshot.cn/v1"
)
parser = StrOutputParser()

# 2. 定义链
class Chain:
    steps: list = []

    def __init__(self, steps: list):
        self.steps = steps

    def invoke(self, input: Any) -> Any:
        for step in self.steps:
            input = step.invoke(input)
            print("步骤",step)
            print("输出",input)
            print("=============")
        return input

# 3. 编排链
chain = Chain([prompt, llm,parser])

# 4. 执行链并获取结果
print(chain.invoke({"query" : "你好，你是？"}))
