#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time : 2026/7/24 15:03
@Author : liuxiaoyu
@File : 1.configurable_fields使用技巧.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1. 创建提示模板
prompt = PromptTemplate.from_template("请生成一个小于{x}的随机整数，只输出整数")

# 2. 创建 LLM，并把 temperature 声明为运行时可配置字段
#
# 注意：
# kimi-k2.6 的 temperature 不能任意修改：
#   - 思考模式固定为 1.0
#   - 非思考模式固定为 0.6
# 如果给 kimi-k2.6 传入 temperature=0，Moonshot API 会返回 HTTP 400。
# 因此这里使用支持动态 temperature 的 moonshot-v1-8k 来演示。
llm = ChatOpenAI(
    model="moonshot-v1-8k",
    base_url="https://api.moonshot.cn/v1",
    temperature=0.7,  # 默认温度；没有传入运行时配置时使用该值
    timeout=60,
).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",  # 运行时通过这个配置键修改 temperature
        name="大语言模型的温度",
        description="温度越低，模型输出越确定；温度越高，模型输出越随机",
    )
)

# 3. 构建链：提示模板 -> 大语言模型 -> 字符串输出解析器
chain = prompt | llm | StrOutputParser()

# 4. 正常调用，没有传入运行时配置，因此使用默认 temperature=0.7
content = chain.invoke({"x": 1000})
print(content)

print("===========================")

# 5. 调用方式一：使用 with_config() 创建一条 temperature=0 的新链
# with_config() 不会修改原来的 chain，而是返回绑定了新配置的 Runnable。
with_config_chain = chain.with_config(configurable={"llm_temperature": 0})
content = with_config_chain.invoke({"x": 1000})

# 调用方式二：也可以在 invoke() 时临时传入同样的配置。
# content = chain.invoke(
#     {"x": 1000},
#     config={"configurable": {"llm_temperature": 0}}
# )
print(content)
