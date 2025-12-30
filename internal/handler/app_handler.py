#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time :2025/12/1910:48
@Author :liuxiaoyu
@File :app_handler.py.py
"""
import os

from openai import OpenAI

from internal.schema import CompletionReq


class AppHandler:
    """应用控制器"""

    def completion(self):
        """聊天接口"""
        # 1.提取从接口中获取的输入
        req = CompletionReq()
        if not req.validate():
            return req.errors
        # query = request.json.get("query")
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.moonshot.cn/v1",
        )
        # 2.构建0penAI客户端,并发起请求
        completion = client.chat.completions.create(
            model="kimi-k2-0905-preview",
            messages=[
                {"role": "system",
                 "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
                {"role": "user", "content": req.query.data},
            ]
        )
        # 3.得到请求响应,然后将0penAI的响应传递给前端
        content = completion.choices[0].message.content
        return content

    def ping(self):
        return {"ping": "pong"}
