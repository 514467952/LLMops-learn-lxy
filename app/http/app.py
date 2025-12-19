#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time :2025/12/1911:00
@Author :liuxiaoyu
@File :app.py
"""
from injector import Injector

from internal.router import Router
from internal.server import Http

injector = Injector()

app = Http(__name__, router=injector.get(Router))

if __name__ == '__main__':
    app.run(debug=True)
