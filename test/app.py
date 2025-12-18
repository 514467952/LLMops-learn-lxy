#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time :2025/12/1710:55
@Author :liuxiaoyu
@File :app.py.py
"""
from injector import inject, Injector


class A:
    name: str = "aaaa"


@inject
class B:
    def __init__(self, a: A):
        self.a = a

    def print_a(self):
        print(f"class A 的 name：{self.a}")


injector = Injector()
b = injector.get(B)
b.print_a()
