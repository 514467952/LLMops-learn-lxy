#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time :2025/12/3010:44
@Author :liuxiaoyu
@File :config.py
"""


class Config:
    def __init__(self):
        # 关闭wtf的csrf保护
        self.WTF_CSRF_ENABLED = False
