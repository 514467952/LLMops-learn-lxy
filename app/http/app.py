#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time :2025/12/1911:00
@Author :liuxiaoyu
@File :app.py
"""
import dotenv
from injector import Injector

from config import Config
from internal.router import Router
from internal.server import Http

# 将env加到环境变量中
dotenv.load_dotenv()

injector = Injector()

conf = Config()

app = Http(__name__, router=injector.get(Router), conf=conf)

if __name__ == '__main__':
    app.run(debug=True)
