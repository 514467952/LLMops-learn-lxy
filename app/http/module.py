#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/3/25 21:47
@Author : liuxiaoyu
@File : module.py
"""
from pkg.sqlalchemy import SQLAlchemy
from injector import Module, Binder
from internal.extension.database_extension import db
from flask_migrate import Migrate
from internal.extension.migrate_extension import migrate


class ExtensionModule(Module):
    """扩展模块的依赖注入"""

    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, to=db)
        binder.bind(Migrate, to=migrate)
