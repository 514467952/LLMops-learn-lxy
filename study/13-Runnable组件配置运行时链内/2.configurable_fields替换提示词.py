#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/7/27 11:43
@Author : liuxiaoyu
@File : 2.configurable_fields替换提示词.py
"""
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField, Runnable

# 1. 创建提示模板，并将 template 字段声明为运行时可配置字段
#
# configurable_fields() 中的参数名必须是 PromptTemplate 的真实字段名，
# 因此这里必须写 template，不能写成自定义名称（例如 template_demo）。
#
# ConfigurableField 的 id 是调用时使用的配置键，可以根据需要自定义。
# 这里设置为 prompt_template，所以运行时通过该键传入新的提示词模板。
prompt = PromptTemplate.from_template("请写一篇关于{subject}主题的冷笑话").configurable_fields(
    template=ConfigurableField(
        id="prompt_template",
        name="提示词模板",
        description="运行时用于替换默认提示词的模板",
    ),
)
# 2. 在本次调用中临时替换提示词模板
#
# configurable 中的 prompt_template 与上面 ConfigurableField 的 id 对应。
# 新旧模板都包含 {subject}，因此仍然可以使用同一份输入数据。
content = prompt.invoke(
    {"subject": "程序员"},
    config={
        "configurable": {
            "prompt_template": "请写一篇关于{subject}主题的藏头诗",
        }
    },
).to_string()

# prompt.invoke() 只负责格式化提示词，不会调用大语言模型。
# 此处输出：请写一篇关于程序员主题的藏头诗
print(content)
