#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/3/25 21:37
@Author : liuxiaoyu
@File : default_config.py
"""
# 应用默认配置项
DEFAULT_CONFIG = {
    # Flask配置
    "SECRET_KEY": "a-default-secret-key-for-dev",
    # wft配置
    "WTF_CSRF_ENABLED": "False",
    # SQLAlchemy数据库配置
    "SQLALCHEMY_DATABASE_URI": "",
    "SQLALCHEMY_POOL_SIZE": 30,
    "SQLALCHEMY_POOL_RECYCLE": 3600,
    "SQLALCHEMY_ECHO": "True",
}