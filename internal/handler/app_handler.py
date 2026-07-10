#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time :2025/12/1910:48
@Author :liuxiaoyu
@File :app_handler.py.py
"""
import os
import uuid
from operator import itemgetter

from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI
from openai import OpenAI
from uuid import UUID

from internal.schema import CompletionReq
from internal.exception import FailException
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message

from dataclasses import dataclass
from injector import inject

@inject
@dataclass
class AppHandler:
    """应用控制器"""

    app_service: AppService

    def create_app(self):
        """调用服务创建新的APP记录"""
        app = self.app_service.create_app()
        return success_message(f"应用已经创建成功,id为{app.id}")

    def get_app(self,id:uuid.UUID):
        """调用服务获取数据库记录"""
        app =self.app_service.get_app(id)
        return success_message(f"应用已经获取成功,name为{app.name}")

    def update_app(self,id:uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"应用已经修改成功,name为{app.name}")

    def delete_app(self,id:uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"应用已经删除成功,id为{app.id}")

    def debug(self, app_id: UUID):
        """聊天接口"""
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.创建prompt与记忆
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个强大的聊天机器人，能根据用户的提问回复对应的问题"),
            MessagesPlaceholder("history"),
            ("human", "{query}"),
        ])
        memory = ConversationBufferWindowMemory(
            k=3,
            input_key="query",
            output_key="output",
            return_messages=True,
            chat_memory=FileChatMessageHistory("./storage/memory/chat_history.txt"),
        )

        # 3. 创建LLM
        llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.moonshot.cn/v1",
            model="kimi-k2.6",
        )

        # 4.创建链应用
        chain = RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        ) | prompt | llm | StrOutputParser()

        # 5.调用链生成内容
        chain_input = {"query": req.query.data}
        content = chain.invoke(chain_input)
        memory.save_context(chain_input, {"output": content})

        return success_json({"content": content})

    def completion(self):
        """聊天接口"""
        # 1.提取从接口中获取的输入
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2. 构建组件
        # 提示词模版
        prompt = ChatPromptTemplate.from_template("{query}")
        # 大语言模型
        llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.moonshot.cn/v1",
            model="kimi-k2.6",
        )
        # 输出解析器
        parser = StrOutputParser()

        # 3.构建链
        chain = prompt | llm | parser

        # 4. 调用链得到结果
        content = chain.invoke({"query":req.query.data})

        return success_json({"content": content})

    def ping(self):
        raise FailException("数据未找到")
