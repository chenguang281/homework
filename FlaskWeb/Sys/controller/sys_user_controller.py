#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from Sys.service.SysUserService import SysUserService

route_sys_user = Blueprint("sys_user", __name__)


# 用户登录
@route_sys_user.route("/login", methods=["POST"])
def getUser():
    return SysUserService.login(request)


# 登录获取权限,获得所有菜单
@route_sys_user.route("/get_permission", methods=["POST"])
def getPermission():
    return SysUserService.getPermission(request)


# 获取权限(前端鉴权用)
@route_sys_user.route("/get_permission_url", methods=["POST"])
def getPermissionURL():
    return SysUserService.getPermissionURL(request)


# 获得用户列表
@route_sys_user.route("/get_user_list", methods=["POST"])
def getUserList():
    return SysUserService.getUserList(request)


# 逻辑删除用户
@route_sys_user.route("/del_user", methods=["POST"])
def delUser():
    return SysUserService.delUser(request)


# 检查用户名是否存在
@route_sys_user.route("/check_user", methods=["POST"])
def checkUser():
    return SysUserService.checkUser(request)


# 添加用户(带角色)
@route_sys_user.route("/add_user", methods=["POST"])
def addUser():
    return SysUserService.addUser(request)


# 修改用户(带角色)
@route_sys_user.route("/update_user", methods=["POST"])
def updateUser():
    return SysUserService.updateUser(request)


# 安全退出登录
@route_sys_user.route("/logOut", methods=["POST"])
def logOut():
    token = request.headers.get("authorization")
    if token:
        return SysUserService.logOut(token)
    else:
        return jsonify({'data': '', 'msg': '退出失败！', 'code': 500})
