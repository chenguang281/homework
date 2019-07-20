#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Sys.model.sys_user_role import SysUserRole
from Sys.model.sys_role import SysRole
from Sys.model.sys_role_menu import SysRoleMenu
from Sys.model.sys_menu import SysMenu
from Base.application import db
import datetime
from flask import jsonify, make_response
import Base.common.utils.List_Utils as list_utils


class SysRoleService():
    # 获得所有角色
    def getRoleList(request):
        try:
            req = request.json
            role_name = req['role_name'] if 'role_name' in req else ''  # 查询条件 用户名模糊查询
            nowPage = req['nowPage'] if 'nowPage' in req else 1
            pagesize = req['pagesize'] if 'pagesize' in req else 10

            sql = "select * from sys_role where status=1"

            if role_name != "" and role_name is not None:
                role_name = '%' + role_name + '%'
                sql = sql + " and role_name like :role"
            condition = {
                "role": role_name,
                "nowPage": (nowPage - 1) * pagesize,
                "pageSize": pagesize
            }
            total = db.session.execute(sql, condition)
            if total.rowcount < pagesize * (nowPage - 1):  # 当查询结果的条数，少于（当前页-1）*分页单位时，把页码重置为第一页
                condition.update(nowPage=0)
                nowPage = 1

            sql = sql + " order by update_time desc limit :nowPage,:pageSize"
            role = db.session.execute(sql, condition)
            redata = list_utils.resultProxy_to_list(role)
            response = make_response(
                jsonify({'data': redata, 'total': total.rowcount, 'nowPage': nowPage, 'msg': '查询成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 新增角色--带权限
    def addRole(request):
        try:
            req = request.json
            role_name = req['role_name'] if 'role_name' in req else ''
            describe = req['describe'] if 'describe' in req else ''
            menu_id = req['menu_id'] if 'menu_id' in req else ''
            menu_id_half = req['menu_id_half'] if 'menu_id_half' in req else ''

            # 开始新增角色
            # 开始检查选中的下级菜单
            menu_new_list = []
            if len(menu_id) > 0:
                menu_new_list = SysRoleService.getNextMenuAll(menu_id, [])
            menu_id_half.extend(menu_new_list)
            role = SysRole()
            role.role_name = role_name
            role.describe = describe
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获得现在时间
            role.create_time = nowTime
            db.session.add(role)
            db.session.flush()
            # 角色新增完成,开始给予权限
            if len(menu_id_half) > 0:
                for j in menu_id_half:
                    roleMenu = SysRoleMenu()
                    roleMenu.role_id = role.id
                    roleMenu.menu_id = j
                    db.session.add(roleMenu)
            db.session.commit()
            response = make_response(jsonify({'data': '', 'msg': '新增成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 修改角色--带权限
    def updateRole(request):
        try:
            req = request.json
            update_id = req['update_id'] if 'update_id' in req else ''
            role_name = req['role_name'] if 'role_name' in req else ''
            describe = req['describe'] if 'describe' in req else ''
            menu_id = req['menu_id'] if 'menu_id' in req else ''
            menu_id_half = req['menu_id_half'] if 'menu_id_half' in req else ''
            # 开始修改角色
            from Sys.model.sys_role import db as roleDB
            role = SysRole.query.filter_by(id=update_id).first()
            role.role_name = role_name
            role.describe = describe
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获得现在时间
            role.update_time = nowTime
            roleDB.session.add(role)
            # 角色修改完成,开始处理权限
            from Sys.model.sys_role_menu import db as roleMenuDB
            SysRoleMenu.query.filter_by(role_id=update_id).delete()
            menu_id_half.extend(menu_id)
            for j in menu_id_half:
                roleMenu = SysRoleMenu()
                roleMenu.role_id = role.id
                roleMenu.menu_id = j
                db.session.add(roleMenu)
            db.session.commit()
            return jsonify({'data': '', 'msg': '修改成功', 'code': 200})
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 得到角色权限
    def getRolePermission(request):
        try:
            req = request.json
            update_id = req['update_id'] if 'update_id' in req else ''
            sql = "SELECT sm.pid,sm.id from sys_role_menu srm LEFT JOIN sys_menu sm on sm.id = srm.menu_id " \
                  "where srm.role_id = :user_id"
            permissionList = db.session.execute(sql, {"user_id": update_id}).fetchall()

            redata = []
            for i in permissionList:
                menu_bool = True
                for j in permissionList:
                    if i.id == j.pid:
                        menu_bool = False
                        break
                if menu_bool:
                    redata.append(i.id)
            response = make_response(jsonify({'data': redata, 'msg': '得到权限成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()

    # 逻辑删除角色
    def deleteRole(request):
        try:
            req = request.json
            role_id = req['role_id'] if 'role_id' in req else ''
            # 判断是否有用户属于该角色
            user = SysUserRole.query.filter_by(role_id=role_id).all()
            if len(user) > 0:
                return jsonify({'data': role_id, 'msg': '该角色下还有用户,禁止删除', 'code': 203})

            sql = "UPDATE SYS_ROLE SET STATUS = 0 WHERE ID = :role_id"
            db.session.execute(sql, {"role_id": role_id})
            # 开始物理删除关联表
            sql = "DELETE from sys_role_menu where role_id = :role_id"
            db.session.execute(sql, {"role_id": role_id})
            db.session.commit()
            response = make_response(jsonify({'data': role_id, 'msg': '删除成功', 'code': 200}))
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'data': role_id, 'msg': '删除失败', 'code': 500})

    # 得到下级所有菜单
    def getNextMenuAll(menu_id, menu_new):
        menu_list = SysMenu.query.filter(SysMenu.pid.in_(menu_id)).all()
        if len(menu_list) > 1:
            menu_new.append(menu_id)
            return SysRoleService.getNextMenuAll(menu_list, menu_new)
        menu_new.append(menu_id)
        return menu_new

    # def getLastMenuList(menu_list):
    #     newList = menu_list
    #     for i in menu_list:
    #         for j in menu_list:
    #             if i.pid == j.id:
    #                 newList.remove(j)
    #                 break
    #     return newList
