#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Time :2025/12/3010:37
@Author :liuxiaoyu
@File :app_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CompletionReq(FlaskForm):
    """基础聊天接口校验"""
    # 必填，长度最大是2000
    query = StringField("query", validators=[
        DataRequired(message="用户的提问是必填"),
        Length(max=2000, message="用户的提问最大长度是2000")
    ])
