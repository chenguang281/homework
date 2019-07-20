#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Sys.model.sys_user import SysUser
from Sys.model.sys_user_role import SysUserRole
from Sys.model.sys_login_log import SysLoginLog
from Base.application import db
import datetime, hashlib
from flask import jsonify, make_response
from Base.common.utils.UUIDUtils import *
import Base.common.utils.List_Utils as list_utils


class SysUserService(Exception):
    # 登录
    def login(request):
        try:
            req = request.json
            username = req['username'] if 'username' in req else ''  # 用户名
            password = req['password'] if 'password' in req else ''  # 密码（未加密）
            query = SysUser.query
            user = query.filter_by(username=username).first()

            # 开始创建登陆日志实体
            loginLog = SysLoginLog()
            loginLog.ip = request.remote_addr  # 得到登陆的ip地址
            loginLog.username = username
            loginLog.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            loginLog.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 直接给予修改时间。也就是后期做为操作时间的基准。
            from Sys.model.sys_login_log import db as logDB
            if user is None or user == '':
                loginLog.status = 0
                logDB.session.add(loginLog)
                logDB.session.commit()
                return jsonify({'data': '', 'msg': '登录失败！账号密码错误', 'code': 403})
            else:
                if user.status == 1:
                    passwordMD5 = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
                    if passwordMD5 == user.password:
                        # 生成一个随机串，带入前端用来做OSS
                        onlyLogin = UUIDUtils.gen_id()
                        tokenVal = "%s-%s-%s-%s" % (user.id, user.username, user.password, onlyLogin)  # token生成
                        token = hashlib.md5(tokenVal.encode(encoding='UTF-8')).hexdigest()
                        loginLog.status = 1
                        loginLog.token = token
                        loginLog.userID = user.id
                        logDB.session.add(loginLog)
                        logDB.session.commit()

                        response = make_response(jsonify({'data': user.id, 'msg': '登录成功！', 'code': 200}))
                        response.headers['authorization'] = token
                        response.headers['user_id'] = user.id
                        response.headers['user_name'] = username
                        return response
                    else:
                        loginLog.status = 0
                        logDB.session.add(loginLog)
                        logDB.session.commit()
                        return jsonify({'data': '', 'msg': '登录失败！账号密码错误', 'code': 403})
                else:
                    loginLog.status = 0
                    logDB.session.add(loginLog)
                    logDB.session.commit()
                    return jsonify({'data': '', 'msg': '登录失败！该账号已经注销', 'code': 403})
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 登录获取权限,获得所有菜单
    def getPermission(request):
        try:
            req = request.json
            user_id = req['user_id'] if 'user_id' in req else ''
            sql = "select m.* from sys_menu m LEFT JOIN sys_role_menu rm on m.id = rm.menu_id LEFT JOIN sys_role r on r.id = rm.role_id  " \
                  "LEFT JOIN sys_user_role  ur  on ur.role_id =  r.id where ur.user_id =:user_id ORDER BY M.ORDER ASC"
            menu_data = db.session.execute(sql, {"user_id": user_id}).fetchall()
            redata = list_utils.resultProxy_to_list(menu_data)
            response = make_response(jsonify({'data': redata, 'msg': '获得登录后权限成功！', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 只拿URL地址，为前端校验权限使用。
    def getPermissionURL(request):
        try:
            req = request.json
            user_id = req['user_id'] if 'user_id' in req else ''
            sql = "select m.url as 'url' from sys_menu m LEFT JOIN sys_role_menu rm on m.id = rm.menu_id LEFT JOIN sys_role r on r.id = rm.role_id  " \
                  "LEFT JOIN sys_user_role  ur  on ur.role_id =  r.id where ur.user_id =:user_id "
            menu_data = db.session.execute(sql, {"user_id": user_id}).fetchall()
            redata = []
            for i in menu_data:
                redata.append("/" + i.url)
            return jsonify({'data': redata, 'msg': '登录成功！', 'code': 200})
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 得到用户列表
    def getUserList(request):
        req = request.json
        user_name = req['user_name'] if 'user_name' in req else ''  # 查询条件 用户名模糊查询
        nowPage = req['nowPage'] if 'nowPage' in req else 1
        pagesize = req['pagesize'] if 'pagesize' in req else 10
        sql = "SELECT su.*,sr.id as role_id,sr.role_name FROM sys_user su " \
              "LEFT JOIN sys_user_role sur ON su.id = sur.user_id " \
              "LEFT JOIN sys_role sr ON sur.role_id = sr.id where su.status = 1 "
        if user_name is not None and user_name != "":
            user_name = '%' + user_name + '%'
            sql = sql + " and su.username like :username "

        condition = {
            "username": user_name,
            "nowPage": (nowPage - 1) * pagesize,
            "pageSize": pagesize
        }
        total = db.session.execute(sql, condition)
        if total.rowcount < pagesize * (nowPage - 1):  # 当查询结果的条数，少于（当前页-1）*分页单位时，把页码重置为第一页
            condition.update(nowPage=0)
            nowPage = 1
        sql = sql + " GROUP BY su.id order by su.create_time desc limit :nowPage,:pageSize"
        user_data = db.session.execute(sql, condition).fetchall()
        redata = list_utils.resultProxy_to_list(user_data)
        return jsonify({'data': redata, 'total': total.rowcount, 'nowPage': nowPage, 'msg': '查询成功', 'code': 200})

    # 逻辑删除用户，清除关联关系。
    def delUser(request):
        try:
            req = request.json
            user_id = req['user_id'] if 'user_id' in req else ''  # 查询条件 用户名模糊查询
            condition = {
                "userId": user_id
            }
            sql = "UPDATE SYS_USER SET STATUS = 0 WHERE ID = :userId"
            db.session.execute(sql, condition)
            db.session.commit()

            # 开始清空关联表
            from Sys.model.sys_user_role import db as userRoleDB
            sql = "DELETE from sys_user_role where user_id = :userId"
            userRoleDB.session.execute(sql, condition)
            userRoleDB.session.commit()

            return jsonify({'data': user_id, 'msg': '删除成功', 'code': 200})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'data': user_id, 'msg': '删除失败', 'code': 500})

    # 检查用户名是否可用
    def checkUser(request):
        try:
            req = request.json
            username = req['username'] if 'username' in req else ''
            query = SysUser.query
            user = query.filter(SysUser.username == username and SysUser.status == 1).all()
            if len(user) > 0:
                return jsonify({'data': '', 'msg': '账户已存在', 'code': 202})
            else:
                return jsonify({'data': '', 'msg': '账户可以使用', 'code': 200})
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 添加用户
    def addUser(request):
        try:
            req = request.json
            username = req['username'] if 'username' in req else ''
            password = req['password'] if 'password' in req else ''
            passwordCheck = req['passwordCheck'] if 'passwordCheck' in req else ''
            email = req['email'] if 'email' in req else ''
            mobile = req['mobile'] if 'mobile' in req else ''
            role_id = req['role_id'] if 'role_id' in req else ''
            if username is None or username == "":
                return jsonify({'data': '', 'msg': '用户名不能为空', 'code': 206})
            if password != passwordCheck:
                return jsonify({'data': '', 'msg': '两次密码不一致', 'code': 206})
            # 开始检测用户名是否重复   and SysUser.status == 1
            query = SysUser.query
            check = query.filter(SysUser.username == username).filter(SysUser.status == 1).all()
            if len(check) > 0:
                return jsonify({'data': '', 'msg': '用户名已存在', 'code': 206})
            user = SysUser()
            user.username = username
            user.password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
            user.email = email
            user.mobile = mobile
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获得现在时间
            user.create_time = nowTime
            db.session.add(user)
            db.session.flush()

            userRole = SysUserRole()
            userRole.user_id = user.id
            userRole.role_id = role_id
            db.session.add(userRole)
            db.session.commit()

            return jsonify({'data': '', 'msg': '保存成功', 'code': 200})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'data': e, 'msg': '系统错误', 'code': 500})

    # 修改用户信息，不包含密码。
    def updateUser(request):
        try:
            req = request.json
            id = req['id'] if 'id' in req else ''
            email = req['email'] if 'email' in req else ''
            mobile = req['mobile'] if 'mobile' in req else ''
            role_id = req['role_id'] if 'role_id' in req else ''
            user = SysUser.query.filter_by(id=id).first()
            user.email = email
            user.mobile = mobile
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获得现在时间
            user.update_time = nowTime
            db.session.add(user)

            from Sys.model.sys_user_role import db as userRoleDB
            userRole = SysUserRole.query.filter_by(user_id=id).first() if (
                    SysUserRole.query.filter_by(user_id=id).first() is not None) else SysUserRole()
            userRole.user_id = id
            userRole.role_id = role_id
            userRoleDB.session.add(userRole)
            userRoleDB.session.commit()

            return jsonify({'data': '', 'msg': '修改成功', 'code': 200})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'data': e, 'msg': '系统错误', 'code': 500})

    # 退出登录
    def logOut(token):
        response = make_response(jsonify({'data': '', 'msg': '安全退出！', 'code': 200}))
        response.headers['authorization'] = "-1"
        response.headers['user_id'] = "-1"
        # 开始清空OSS登录设置
        from Sys.model.sys_login_log import db as logDB
        sysLoginLog = SysLoginLog.query.filter_by(token=token).first()
        sysLoginLog.update_time = datetime.datetime(1970, 1, 1, 00, 00, 00).strftime('%Y-%m-%d %H:%M:%S')
        logDB.session.add(sysLoginLog)
        logDB.session.commit()
        return response
