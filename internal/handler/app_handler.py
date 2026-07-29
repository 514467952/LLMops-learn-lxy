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
from typing import Dict, Any

from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.memory import BaseMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig
from langchain_core.tracers.schemas import Run
from langchain_openai import ChatOpenAI
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

    @classmethod
    def _load_memory_variables(cls, input: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        """加载记忆变量信息"""
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            return configurable_memory.load_memory_variables(input)
        return {"history": []}

    @classmethod
    def _save_context(cls, run_obj: Run, config: RunnableConfig) -> None:
        """存储对应的上下文信息到记忆实体中"""
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            configurable_memory.save_context(run_obj.inputs, run_obj.outputs)

    def debug(self, app_id: UUID):
        """聊天接口"""
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.创建prompt与记忆
        system_prompt = "你是一个强大的聊天机器人，能根据对应的上下文和历史对话信息回复用户问题。\n\n<context>{context}</context>"
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
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
        chain = (
            RunnablePassthrough.assign(
                history=RunnableLambda(self._load_memory_variables) | itemgetter("history")
            )
            | prompt
            | llm
            | StrOutputParser()
        ).with_listeners(on_end=self._save_context)

        # 5.调用链生成内容
        chain_input = {"query": req.query.data, "context": ""}
        content = chain.invoke(chain_input, config={"configurable": {"memory": memory}})

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
