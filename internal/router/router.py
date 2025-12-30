#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time :2025/12/1910:50
@Author :liuxiaoyu
@File :router.py
"""
# 导入dataclass，不用写构造函数也可以依赖注入
from dataclasses import dataclass

from flask import Flask, Blueprint
from injector import inject

from internal.handler import AppHandler


@inject
@dataclass
class Router:
    """路由"""
    app_handler = AppHandler()

    # 构造函数依赖注入
    # def __init__(self, app_handler: AppHandler):
    #     self.app_handler = app_handler

    def register_router(self, app: Flask):
        """注册路由"""
        # 1.创建一个蓝图（一组路由的集合）
        bp = Blueprint("llmops", __name__, url_prefix="")

        # 2.将url与对应的控制器方法绑定
        bp.add_url_rule("ping", view_func=self.app_handler.ping)
        bp.add_url_rule("app/completion", methods=["POST"], view_func=self.app_handler.completion)

        # 3.在应用上注册蓝图
        app.register_blueprint(bp)
