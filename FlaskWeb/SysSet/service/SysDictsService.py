#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Base.application import db
from flask import jsonify, make_response
from SysSet.model.SetDictionary import SetDictionary


class SysDictsService():
    # 得到所有页签信息
    def getTab(self):
        sql = "select s.table_code,t.table_comment FROM set_dictionary  s LEFT JOIN INFORMATION_SCHEMA.Tables t on s.table_code = t.TABLE_NAME  GROUP  by table_code"
        try:
            data = db.session.execute(sql)
            redata = []
            for i in data:
                dicts_tab_bo = {}
                dicts_tab_bo.update(table_code=i.table_code)
                dicts_tab_bo.update(table_comment=i.table_comment)
                redata.append(dicts_tab_bo)
            response = make_response(
                jsonify({'data': redata, 'msg': '查询成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 获得单独页签信息
    def getTabColumn(request):
        req = request.json
        table_name = req['table_name'] if 'table_name' in req else ''
        nowPage = req['nowPage'] if 'nowPage' in req else ''
        pagesize = req['pagesize'] if 'pagesize' in req else ''
        select_word = req['select_name'] if 'select_name' in req else ''
        sql = "select s.*,i.column_comment FROM set_dictionary s LEFT JOIN  INFORMATION_SCHEMA.Columns i on s.column_code = i.COLUMN_NAME AND table_name=:table_name" \
              " where s.table_code = :table_name and s.status <> -1 "

        if select_word is not None and select_word != "":
            select_word = '%' + select_word + '%'
            sql = sql + " and (s.column_code like :select_word or s.name like :select_word or i.column_comment like :select_word ) "

        condition = {
            "select_word": select_word,
            "nowPage": (nowPage - 1) * pagesize,
            "pageSize": pagesize,
            "table_name": table_name
        }
        total = db.session.execute(sql, condition)
        if total.rowcount < pagesize * (nowPage - 1):  # 当查询结果的条数，少于（当前页-1）*分页单位时，把页码重置为第一页
            condition.update(nowPage=0)
            nowPage = 1
        sql = sql + " order by s.column_code,s.num asc limit :nowPage,:pageSize"
        try:
            data = db.session.execute(sql, condition)
            redata = []
            for i in data:
                dicts_tab_bo = {}
                dicts_tab_bo.update(id=i.id)
                dicts_tab_bo.update(column_code=i.column_code)
                dicts_tab_bo.update(column_comment=i.column_comment)
                dicts_tab_bo.update(num=i.num)
                dicts_tab_bo.update(name=i.name)
                dicts_tab_bo.update(value=i.value)
                redata.append(dicts_tab_bo)
            response = make_response(
                jsonify({'data': redata, 'total': total.rowcount, 'nowPage': nowPage, 'msg': '查询成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 获得所有表信息，带汉字名
    def getTables(request):
        req = request.json
        select_name = req['select_name'] if 'select_name' in req else ''  # 查询条件 用户名模糊查询
        nowPage = req['nowPage'] if 'nowPage' in req else 1
        pagesize = req['pagesize'] if 'pagesize' in req else 10

        sql = "SELECT t.TABLE_NAME as tableName ,t.TABLE_COMMENT as realName from INFORMATION_SCHEMA.Tables t WHERE t.table_schema = (SELECT DATABASE()) "
        if select_name != "" and select_name is not None:
            select_name = '%' + select_name + '%'
            sql = sql + " and (t.TABLE_NAME like :select_name or t.TABLE_COMMENT like :select_name)"
        condition = {
            "select_name": select_name,
            "nowPage": (nowPage - 1) * pagesize,
            "pageSize": pagesize
        }
        total = db.session.execute(sql, condition)
        if total.rowcount < pagesize * (nowPage - 1):  # 当查询结果的条数，少于（当前页-1）*分页单位时，把页码重置为第一页
            condition.update(nowPage=0)
            nowPage = 1

        sql = sql + " ORDER BY t.TABLE_NAME limit :nowPage,:pageSize"

        try:
            data = db.session.execute(sql, condition)
            redata = []
            for i in data:
                dicts_tab_bo = {}
                dicts_tab_bo.update(tableName=i.tableName)
                dicts_tab_bo.update(realName=i.realName)
                redata.append(dicts_tab_bo)
            response = make_response(
                jsonify({'data': redata, 'total': total.rowcount, 'nowPage': nowPage, 'msg': '查询成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 获得所有列信息，带汉字名，除去ID，仅查询int相关类型
    def getColumn(request):
        req = request.json
        table_name = req['table_name'] if 'table_name' in req else ''  # 查询条件 用户名模糊查询
        sql = "SELECT column_name,column_comment FROM INFORMATION_SCHEMA.Columns WHERE table_name=:table_name  and COLUMN_TYPE like '%int%' and binary COLUMN_NAME  <>  'id' "
        condition = {
            "table_name": table_name
        }
        try:
            data = db.session.execute(sql, condition)
            redata = []
            for i in data:
                dicts_tab_bo = {}
                dicts_tab_bo.update(column_name=i.column_name)
                dicts_tab_bo.update(column_comment=i.column_name + "-" + i.column_comment)
                redata.append(dicts_tab_bo)
            response = make_response(
                jsonify({'data': redata, 'msg': '查询成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 保存字典
    def saveDicts(request):
        req = request.json
        dicts = req['column_add'] if 'column_add' in req else ''
        table = req['table_code'] if 'table_code' in req else ''

        dictionary = SetDictionary()
        dictionary.status = 1
        dictionary.num = dicts['save_value']
        dictionary.column_code = dicts['column_code']
        dictionary.name = dicts['callback_value']
        dictionary.value = dicts['real_value']
        dictionary.table_code = table
        db.session.add(dictionary)
        db.session.commit()
        return jsonify({'data': '', 'msg': '新增成功', 'code': 200})
