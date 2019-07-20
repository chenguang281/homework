#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Base.application import db

"""
v_iterative,需要转换的查询结果
table_name,对应转换的字典表
column_name,对应转换的字典列
"""


def resultProxy_to_list_dicts(v_iterative, table_name, column_name):
    li = []
    sql = 'select * from set_dictionary where 1 = 1'
    if table_name is not None and table_name != '':
        sql = sql + ' and table_code = :table_code and column_code in :column_code'
        condition = {
            "table_code": table_name,
            "column_code": column_name
        }
        # 开始查询字典表
        dicts = db.session.execute(sql, condition)  # 得到字典结果
        # for i in dicts:
        #     print(i.name)
        #     print(i.num)
        # print(1111)

        for i in v_iterative:
            bo = {}
            for k, v in zip(i.keys(), i):
                bo[k] = v
                if k in column_name:
                    for d in dicts:
                        if v == d.num:
                            bo[k] = d.name
                if 'time' in k:
                    bo[k] = str(v if (v is not None) else "")
            li.append(bo)
        return li
    return "参数错误"


def resultProxy_to_list(v_iterative):
    li = []
    for i in v_iterative:
        bo = {}
        for k, v in zip(i.keys(), i):
            bo[k] = v
            if 'time' in k:
                bo[k] = str(v if (v is not None) else "")
        li.append(bo)
    return li
