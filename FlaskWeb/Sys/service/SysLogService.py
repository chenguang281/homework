#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Base.application import db
from flask import jsonify, make_response
from Sys.model.sys_login_log import SysLoginLog
import Base.common.utils.List_Utils as list_utils
import datetime


class SysLogService():
    # 获得所有日志
    def getAllLog(request):
        req = request.json
        select_word = req['select_word'] if 'select_word' in req else ''
        select_create_time = req['select_create_time'] if 'select_create_time' in req else ['1970-01-01 00:00:01',
                                                                                            '2099-12-31 23:59:59']
        select_status = req['select_status'] if 'select_status' in req else ''
        nowPage = req['nowPage'] if 'nowPage' in req else 1
        pagesize = req['pagesize'] if 'pagesize' in req else 10

        sql = "select * FROM sys_login_log where 1 = 1 "

        if select_word is not None and select_word != "":
            select_word = '%' + select_word + '%'
            sql = sql + " and username like :username"
        condition = {
            "username": select_word,
            "status": select_status,
            "nowPage": (nowPage - 1) * pagesize,
            "pageSize": pagesize
        }
        if select_create_time is not None and select_create_time != "":
            sql = sql + " and create_time between :startTime and :endTime"
            condition.update(startTime=select_create_time[0] + ' 00:00:01')
            condition.update(endTime=select_create_time[1] + ' 23:59:59')
        if select_status is not None and select_status != "":
            sql = sql + " and status = :status"

        try:
            total = db.session.execute(sql, condition)
            if total.rowcount < pagesize * (nowPage - 1):  # 当查询结果的条数，少于（当前页-1）*分页单位时，把页码重置为第一页
                condition.update(nowPage=0)
                nowPage = 1
            if pagesize is not None and pagesize != "":
                sql = sql + " order by create_time desc limit :nowPage,:pageSize"
            data = db.session.execute(sql, condition)
            redata = list_utils.resultProxy_to_list(data)
            response = make_response(
                jsonify({'data': redata, 'total': total.rowcount, 'nowPage': nowPage, 'msg': '查询成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    def checkAuthorization(authorization, user_id, path):
        sysLoginLog = SysLoginLog.query.filter(SysLoginLog.userID == user_id).order_by(
            SysLoginLog.update_time.desc()).all()
        if sysLoginLog and sysLoginLog[0].token == authorization:
            # 账户还在,继续验证
            nowTime = datetime.datetime.now()  # 获得现在时间
            beforeTime = sysLoginLog[0].update_time  # 上次操作时间
            if (nowTime - beforeTime).total_seconds() > 1800:
                # 超时,重新登录吧~!
                return jsonify({'data': None, 'msg': '操作超时,请重新登录', 'code': 205})
            else:
                sql = "select 1 from sys_user_role sur LEFT JOIN sys_role r on sur.role_id = r.id LEFT JOIN sys_role_menu srm on srm.role_id = r.id " \
                      "LEFT JOIN sys_menu sm on srm.menu_id = sm.id where sur.user_id = :user_id and sm.url = :path"
                condition = {
                    "user_id": user_id,
                    "path": path
                }
                permissionList = db.session.execute(sql, condition).fetchall()
                if permissionList:
                    # 有权限操作,开始续时
                    sql = "update sys_login_log set update_time = :nowTime where id = :id "
                    condition = {
                        "nowTime": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 获得现在时间
                        "id": sysLoginLog[0].id
                    }
                    db.session.execute(sql, condition)
                    db.session.commit()
                    return None
                else:
                    return jsonify({'data': None, 'msg': '您没有权限操作该功能', 'code': 203})
        else:
            # 账户异地登录
            return jsonify({'data': None, 'msg': '该账号异地登录,请保证账号安全,建议您及时修改密码,或联系管理员', 'code': 204})
            pass
