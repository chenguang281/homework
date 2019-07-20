#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from Sys.service.SysRoleService import SysRoleService

route_sys_role = Blueprint("sys_role", __name__)


# 获得角色列表
@route_sys_role.route("/get_role_list", methods=["POST"])
def getUserList():
    return SysRoleService.getRoleList(request)


# 新增角色,带权限
@route_sys_role.route("/add_role", methods=["POST"])
def addRole():
    return SysRoleService.addRole(request)


# 根据角色ID取得权限ID集合
@route_sys_role.route("/get_role_permission", methods=["POST"])
def getRolePermission():
    return SysRoleService.getRolePermission(request)


# 根据角色ID修改角色信息(带权限)
@route_sys_role.route("/update_role", methods=["POST"])
def updateRole():
    return SysRoleService.updateRole(request)


# 根据角色ID修改角色信息(逻辑删除)
@route_sys_role.route("/delete_role", methods=["POST"])
def deleteRole():
    return SysRoleService.deleteRole(request)
