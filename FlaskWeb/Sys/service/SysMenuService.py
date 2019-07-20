#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Sys.model.sys_role_menu import SysRoleMenu
from Sys.model.sys_menu import SysMenu
from Base.application import db
import datetime
import Base.common.utils.List_Utils as list_utils

from flask import jsonify, make_response


class SysMenuService():
    # 获得所有一级菜单
    def getMenuList(request):
        try:
            req = request.json
            # user_name = req['user_name'] if 'user_name' in req else ''  # 查询条件 用户名模糊查询
            sql = "SELECT MM.*,AA.PID AS 'hasChildren' FROM SYS_MENU MM LEFT JOIN (" \
                  " SELECT PID FROM SYS_MENU AA WHERE AA.PID IN  " \
                  " (SELECT ID FROM SYS_MENU SM WHERE SM.PID ='' AND SM.STATUS =1 group  by sm.id)" \
                  " ) AA ON MM.ID = AA.PID WHERE MM.PID = '' AND MM.STATUS =1 group by mm.id order by mm.order"
            # sql直接验证是否有下级菜单，不然不会写成这样的sql
            menu_data = db.session.execute(sql).fetchall()
            redata = list_utils.resultProxy_to_list_dicts(menu_data, 'sys_menu', ['hasChildren'])
            redata = []
            for j in menu_data:
                menu_bo = {}
                menu_bo.update(id=j.id)
                menu_bo.update(menu_name=j.menu_name)
                menu_bo.update(url=j.url)
                menu_bo.update(icon=j.icon)
                menu_bo.update(order=j.order)
                menu_bo.update(type=j.type)
                menu_bo.update(status=j.status)
                menu_bo.update(create_time=str(j.create_time if (j.create_time != None) else ""))
                menu_bo.update(update_time=str(j.update_time if (j.update_time != None) else ""))
                menu_bo.update(hasChildren=True if (j.hasChildren != None) else False)  # 是否有下级菜单
                redata.append(menu_bo)
            response = make_response(jsonify({'data': redata, 'msg': '查询成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 得到下级菜单，并判断下级菜单还是否含有下级菜单
    def getNextMenuList(request):
        try:
            req = request.json
            menu_id = req['menu_id'] if 'menu_id' in req else ''  # 查询条件 用户名模糊查询
            sql = "SELECT MM.*,AA.PID AS 'hasChildren' FROM SYS_MENU MM LEFT JOIN (" \
                  " SELECT PID FROM SYS_MENU AA WHERE AA.PID IN  " \
                  " (SELECT ID FROM SYS_MENU SM WHERE SM.PID = :menu_id AND SM.STATUS = 1 group  by sm.id)" \
                  " ) AA ON MM.ID = AA.PID WHERE MM.PID = :menuId AND MM.STATUS = 1 GROUP BY MM.ID"
            condition = {
                "menu_id": menu_id,
                "menuId": menu_id
            }

            menu_data = db.session.execute(sql, condition).fetchall()
            redata = []
            for j in menu_data:
                menu_bo = {}
                menu_bo.update(id=j.id)
                menu_bo.update(menu_name=j.menu_name)
                menu_bo.update(url=j.url)
                menu_bo.update(icon=j.icon)
                menu_bo.update(order=j.order)
                menu_bo.update(type=j.type)
                menu_bo.update(status=j.status)
                menu_bo.update(create_time=str(j.create_time if (j.create_time != None) else ""))
                menu_bo.update(update_time=str(j.update_time if (j.update_time != None) else ""))
                menu_bo.update(hasChildren=True if (j.hasChildren != None) else False)
                redata.append(menu_bo)
            response = make_response(jsonify({'data': redata, 'msg': '查询成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 只获取可用状态的菜单,支持角色菜单tree
    def getMenuListRole(self):
        try:
            sql = "SELECT MM.*,AA.PID AS 'next_bol' FROM SYS_MENU MM LEFT JOIN (" \
                  " SELECT PID FROM SYS_MENU AA WHERE AA.PID IN  " \
                  " (SELECT ID FROM SYS_MENU SM WHERE SM.PID ='' group by SM.id)" \
                  " ) AA ON MM.ID = AA.PID WHERE MM.PID = '' group  by mm.id"
            menu_data = db.session.execute(sql).fetchall()
            redata = []
            for j in menu_data:
                menu_bo = {}
                menu_bo.update(id=j.id)
                menu_bo.update(menu_name=j.menu_name)
                menu_bo.update(status=j.status)
                menu_bo.update(leaf=True if (j.next_bol == None) else False)
                redata.append(menu_bo)
            response = make_response(jsonify({'data': redata, 'msg': '查询成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    def getNextMenuListRole(request):
        try:
            req = request.json
            menu_id = req['menu_id'] if 'menu_id' in req else ''  # 查询条件 用户名模糊查询
            sql = "SELECT MM.*,AA.PID AS 'next_bol' FROM SYS_MENU MM LEFT JOIN (" \
                  " SELECT PID FROM SYS_MENU AA WHERE AA.PID IN  " \
                  " (SELECT ID FROM SYS_MENU SM WHERE SM.PID = :menu_id GROUP BY SM.ID)" \
                  " ) AA ON MM.ID = AA.PID WHERE MM.PID = :menuId GROUP BY MM.ID"
            condition = {
                "menu_id": menu_id,
                "menuId": menu_id
            }
            menu_data = db.session.execute(sql, condition).fetchall()
            redata = []
            for j in menu_data:
                menu_bo = {}
                menu_bo.update(id=j.id)
                menu_bo.update(menu_name=j.menu_name)
                menu_bo.update(status=j.status)
                menu_bo.update(leaf=False if (j.next_bol != None) else True)
                redata.append(menu_bo)
            response = make_response(jsonify({'data': redata, 'msg': '查询成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 新增菜单,包含父类,形成层级关系
    def addMenu(request):
        try:
            req = request.json
            add_name = req['add_name'] if 'add_name' in req else ''
            add_url = req['add_url'] if 'add_url' in req else ''
            add_icon = req['add_icon'] if 'add_icon' in req else ''
            add_order = req['add_order'] if 'add_order' in req else ''
            add_type = req['add_type'] if 'add_type' in req else ''
            pid = req['pid'] if 'pid' in req else ''

            if add_name == None or add_name == "":
                return jsonify({'data': "", 'msg': '菜单名不能为空', 'code': 203})

            if add_type == None or add_type == "":
                return jsonify({'data': "", 'msg': '类别不能为空', 'code': 203})

            if add_url == None or add_url == "":
                return jsonify({'data': "", 'msg': '访问地址不能为空', 'code': 203})

            if pid != None and pid != "":
                menu = SysMenu.query.filter_by(id=pid).first()
                if menu.type == 2:
                    response = make_response(jsonify({'data': "", 'msg': '按钮下,不允许再添加任何子(菜单/按钮)', 'code': 203}))
                    return response

            menu = SysMenu()
            menu.menu_name = add_name
            menu.url = add_url
            menu.icon = add_icon
            menu.order = add_order
            menu.type = add_type
            menu.pid = pid
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获得现在时间
            menu.create_time = nowTime
            db.session.add(menu)
            db.session.flush()
            return jsonify({'data': "", 'msg': '新增菜单成功', 'code': 200})
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 同时清空父ID
    def delMenu(request):
        try:
            req = request.json
            menu_id = req['menu_id'] if 'menu_id' in req else ''
            # 开始验证是否可以删除
            query = SysMenu.query
            menu = query.filter_by(pid=menu_id).all()
            if len(menu) > 0:
                return jsonify({'data': menu_id, 'msg': '存在下级菜单,不允许删除', 'code': 203})

            query = SysRoleMenu.query
            rolemenu = query.filter_by(menu_id=menu_id).all()
            if len(rolemenu) > 0:
                return jsonify({'data': menu_id, 'msg': '该菜单包含角色挂载,不允许删除', 'code': 203})

            sql = "UPDATE SYS_MENU SET STATUS = 0 , pid='' WHERE ID = :menu_id"
            db.session.execute(sql, {"menu_id": menu_id})
            db.session.commit()

            return jsonify({'data': menu_id, 'msg': '删除成功', 'code': 200})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'data': menu_id, 'msg': '删除失败', 'code': 500})

    # 得到全部菜单
    def getAllMenu(self):
        try:
            sql = "SELECT * FROM sys_menu sm WHERE sm.status =1 ORDER BY sm.order"
            menu = db.session.execute(sql)
            returnData = []
            for j in menu:
                menu_bo = {}
                menu_bo.update(id=j.id)
                menu_bo.update(menu_name=j.menu_name)
                menu_bo.update(url=j.url)
                menu_bo.update(icon=j.icon)
                menu_bo.update(order=j.order)
                menu_bo.update(type=j.type)
                menu_bo.update(status=j.status)
                menu_bo.update(pid=j.pid)
                returnData.append(menu_bo)
            response = make_response(jsonify({'data': returnData, 'msg': '查询成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'data': e, 'msg': '获取失败', 'code': 500})
