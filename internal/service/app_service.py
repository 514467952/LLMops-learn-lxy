#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/3/30 20:45
@Author : liuxiaoyu
@File : app_service.py
"""
import uuid

from flask import Flask
from pkg.sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from injector import inject

from internal.model import App

@inject
@dataclass
class AppService:
    """应用服务器"""
    db: SQLAlchemy

    def create_app(self) -> App :
        with self.db.auto_commit():
            #1. 创建模型实体表
            app = App(name="测试机器人", account_id=uuid.uuid4(), icon="", description="这是一个简单的聊天机器人")
            #2.将实体类添加到session会话中
            self.db.session.add(app)
        #3.提交session会话
        return app

    def get_app(self,id: uuid.UUID) -> App :
        app = self.db.session.query(App).get(id)
        return app

    def update_app(self,id: uuid.UUID) -> App :
        with self.db.auto_commit():
            app = self.get_app(id)
            app.name = "幕课聊天机器人"
        return app

    def delete_app(self,id: uuid.UUID) -> App :
        with self.db.auto_commit():
            app = self.get_app(id)
            self.db.session.delete(app)
        return app
